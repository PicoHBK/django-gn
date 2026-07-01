# Especificación backend — Generación asíncrona (`generate/concatenate-prompts/`)

> Documento para el agente/dev del **backend**. Describe el cambio que hay que
> hacer en el endpoint de generación para que el frontend funcione en móvil.
> El frontend **ya está adaptado** a este contrato.

---

## 1. El problema que estamos resolviendo

El endpoint `POST generate/concatenate-prompts/` genera una imagen y tarda
**entre 10 y 60 segundos** en responder. Hoy es **síncrono**: el frontend hace
el POST y se queda esperando la respuesta con la imagen.

En móvil esto rompe: si el usuario **bloquea la pantalla** mientras genera, el
navegador suspende el JavaScript y **mata la conexión TCP** de esa petición. El
backend termina la imagen, pero el frontend nunca recibe la respuesta →
se queda "generando" para siempre y **la imagen se pierde**.

**Solución:** desacoplar la generación de la respuesta HTTP. El POST solo
**encola** un job y responde al instante con un `job_id`. El frontend obtiene el
resultado haciendo **polling** de un endpoint de estado. Como el `job_id` se
persiste en el cliente, aunque el móvil se bloquee o se recargue la página, al
volver el frontend reanuda el polling y **recoge la imagen ya generada**.

---

## 2. Contrato de la API (lo que el frontend espera)

Hay que pasar de **1 endpoint síncrono** a **3 endpoints**.

### 2.1. `POST generate/concatenate-prompts/` — Encolar generación

- **Payload:** exactamente el mismo de antes (no cambia). Campos que envía el
  frontend: `character`, `image`, `skin`, `pose`, `emotion`, `code`, `special`
  (array de strings), `clip_skip` (number), etc.
- **Comportamiento nuevo:** hacer las **validaciones rápidas de forma síncrona**
  (código válido, tier suficiente, disponibilidad) y luego **encolar** el trabajo
  pesado en un worker. Responder **de inmediato**, sin esperar a la generación.

**Respuesta OK (202 Accepted):**
```json
{ "job_id": "abc123" }
```

**Errores síncronos (se mantienen igual que antes):**

| Código | Significado | Qué hace el frontend |
|--------|-------------|----------------------|
| `406`  | Código inválido / agotado | Limpia el código introducido |
| `423`  | Servicio ocupado / bloqueado | Reintenta el POST automáticamente a los 2s |
| `4xx/5xx` con `{ "error": "..." }` | Otro error (tier insuficiente, "AI is unavailable", etc.) | Muestra el `error` en un toast |

> El tier y los usos restantes **NO** se devuelven aquí. Se devuelven al final,
> junto con el resultado (ver estado `completed`).

---

### 2.2. `GET generate/status/{job_id}/` — Consultar estado (polling)

El frontend llama a este endpoint cada **3 segundos** mientras el job no haya
terminado, y también inmediatamente cada vez que la pestaña vuelve a estar
visible (al desbloquear el móvil).

Debe devolver **200 OK** siempre (mientras el job exista), con uno de estos
cuerpos según el estado:

**En curso:**
```json
{ "status": "pending" }
```
```json
{ "status": "processing" }
```

**Terminado con éxito:**
```json
{
  "status": "completed",
  "images": ["<base64 o URL de la imagen>"],
  "tier": "premium",
  "uses_left": 3,
  "code": "MOMO"
}
```
> `images` es un array; el frontend usa `images[0]`. `tier`, `uses_left` y `code`
> son los que antes venían en la respuesta síncrona.

**Terminado con error:**
```json
{ "status": "failed", "error": "AI is unavailable" }
```

**Requisitos importantes:**
- Los valores de `status` deben ser **exactamente** `pending`, `processing`,
  `completed`, `failed`.
- Mientras el job esté vivo, responder `200`. (Si el job no existe / expiró,
  ver sección 4.)
- El frontend **tolera errores de red transitorios** en este endpoint (reintenta
  solo), así que un corte puntual no rompe nada. Pero un `4xx/5xx` persistente
  dejaría el polling reintentando; lo ideal es responder `200` con el estado real.

---

### 2.3. `POST generate/cancel/{job_id}/` — Cancelar (opcional, recomendado)

El frontend lo llama **best-effort** cuando el usuario pulsa "Cancel". Sirve para
**no gastar el uso/código** si el usuario aborta.

- Cancelar el job si aún está en cola / en proceso.
- La respuesta no la usa el frontend (ignora éxito o fallo). Devolver `200` o
  `204` está bien.

---

## 3. Cómo se comporta el frontend (para que encaje el diseño)

- **Persistencia:** al recibir el `job_id`, el frontend lo guarda en
  `localStorage` junto con el `startTime`. Por eso el estado del job **debe vivir
  fuera del proceso** (Redis / base de datos), no en memoria: el cliente puede
  desaparecer y volver minutos después, incluso tras recargar.
- **Polling:** cada 3s (`refetchInterval`), con reintento ante fallos de red, y
  refetch inmediato al recuperar foco/visibilidad.
- **Fin:** cuando llega `completed` o `failed`, el frontend deja de sondear,
  limpia el `localStorage` y muestra la imagen o el error.

---

## 4. Detalles de implementación recomendados (backend)

- **Worker asíncrono:** ejecutar la generación pesada en Celery / RQ / Dramatiq
  o un thread/pool. El request del POST **no** debe bloquear.
- **Almacén de estado con TTL:** guardar `{ status, images?, tier?, uses_left?,
  code?, error? }` por `job_id` en Redis o DB. Sugerencia de TTL: expirar el
  resultado unos minutos después de completarse (p.ej. 10-15 min) o borrarlo tras
  ser recogido.
- **Job inexistente / expirado:** si llega un `GET status/{job_id}` para un id
  desconocido, lo más limpio es responder `404`, o bien
  `{ "status": "failed", "error": "Job not found or expired" }` con `200`. Con
  cualquiera de los dos el frontend cortará el polling y mostrará error; elige
  uno y sé consistente.
- **Idempotencia del consumo:** descontar el uso del código **cuando la
  generación termina con éxito**, no al encolar (así, si falla, no se cobra).
  Alternativamente, reservar al encolar y devolver al fallar/cancelar — a
  criterio del backend, pero que quede claro.
- **Concurrencia / 423:** si hay un límite de generaciones simultáneas, devolver
  `423` en el POST cuando esté saturado (el frontend reintenta solo a los 2s).

---

## 5. Ejemplo de flujo completo

```
Cliente                                Backend
  │  POST generate/concatenate-prompts/  │
  │─────────────────────────────────────>│  valida code/tier (rápido)
  │                                       │  encola job en worker
  │        202 { "job_id": "abc123" }     │
  │<─────────────────────────────────────│
  │  (guarda job_id en localStorage)      │  worker genera (10-60s)...
  │                                       │
  │  GET generate/status/abc123/  (cada 3s)
  │─────────────────────────────────────>│
  │        200 { "status": "processing" } │
  │<─────────────────────────────────────│
  │        ...(móvil bloqueado, no sondea)│  worker termina, guarda resultado
  │  (usuario desbloquea → refetch inmediato)
  │  GET generate/status/abc123/          │
  │─────────────────────────────────────>│
  │  200 { "status":"completed",          │
  │        "images":[...], "tier":"...",  │
  │        "uses_left":3, "code":"MOMO" }  │
  │<─────────────────────────────────────│
  │  (muestra imagen, limpia localStorage)│
```

---

## 6. Ejemplo orientativo (Django REST Framework + Celery)

> Pseudocódigo para dar la idea; adáptalo a tu stack real.

```python
# tasks.py
@shared_task
def run_generation(job_id, payload):
    cache.set(f"job:{job_id}", {"status": "processing"}, timeout=900)
    try:
        images = generate_images(payload)              # trabajo pesado 10-60s
        tier, uses_left, code = apply_code_usage(payload["code"])
        cache.set(f"job:{job_id}", {
            "status": "completed",
            "images": images,
            "tier": tier,
            "uses_left": uses_left,
            "code": code,
        }, timeout=900)
    except Exception as e:
        cache.set(f"job:{job_id}", {"status": "failed", "error": str(e)}, timeout=900)


# views.py
class ConcatenatePromptsView(APIView):
    def post(self, request):
        payload = request.data
        # validaciones rápidas y síncronas:
        if not code_is_valid(payload.get("code")):
            return Response({"error": "invalid code"}, status=406)
        if service_busy():
            return Response({"error": "busy"}, status=423)
        if not tier_is_sufficient(payload):
            return Response({"error": "AI requires a higher tier"}, status=402)

        job_id = uuid4().hex
        cache.set(f"job:{job_id}", {"status": "pending"}, timeout=900)
        run_generation.delay(job_id, payload)
        return Response({"job_id": job_id}, status=202)


class GenerationStatusView(APIView):
    def get(self, request, job_id):
        data = cache.get(f"job:{job_id}")
        if data is None:
            return Response({"status": "failed", "error": "Job not found or expired"}, status=200)
        return Response(data, status=200)


class GenerationCancelView(APIView):
    def post(self, request, job_id):
        cache.delete(f"job:{job_id}")   # + revocar la task si tu broker lo permite
        return Response(status=204)


# urls.py
urlpatterns = [
    path("generate/concatenate-prompts/", ConcatenatePromptsView.as_view()),
    path("generate/status/<str:job_id>/", GenerationStatusView.as_view()),
    path("generate/cancel/<str:job_id>/", GenerationCancelView.as_view()),
]
```

---

## 7. Checklist para el backend

- [ ] `POST generate/concatenate-prompts/` valida rápido y devuelve `202 { job_id }`.
- [ ] Se mantienen los códigos `406` (código) y `423` (ocupado) en el POST.
- [ ] El trabajo pesado corre en un worker, no bloquea el request.
- [ ] `GET generate/status/{job_id}/` devuelve `pending`/`processing`/`completed`/`failed`.
- [ ] `completed` incluye `images`, `tier`, `uses_left`, `code`.
- [ ] `failed` incluye `error`.
- [ ] Estado persistido en Redis/DB con TTL (sobrevive a que el cliente se vaya y vuelva).
- [ ] (Opcional) `POST generate/cancel/{job_id}/` cancela y no cobra el uso.
- [ ] El uso/código se descuenta al completar con éxito (no al encolar).
```
