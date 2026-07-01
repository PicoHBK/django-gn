# Frontend — Cómo consumir la generación de imágenes

> Guía para el **frontend**. Describe cómo hablar con el endpoint de generación
> ahora que es **asíncrono** (job + polling) y **a prueba de móvil**.
> El backend ya está implementado con este contrato.

---

## 1. Idea general (léelo antes que nada)

Generar una imagen tarda **10–60 s**. No se hace en una sola petición: se **encola**
y luego se **sondea** el resultado.

```
1. POST  concatenate-prompts/   → encola y responde al instante { job_id }
2. GET   status/{job_id}/        → se llama cada 3 s hasta que termina
3. POST  cancel/{job_id}/        → opcional, si el usuario cancela
```

**La imagen NUNCA viene en la respuesta del POST.** El POST solo confirma que se
encoló. La imagen llega en el `GET status/` cuando el estado es `completed`.

### ⚠️ Regla de oro (esto es lo que arregla el bug de móvil)

**El `job_id` lo genera el FRONTEND, se guarda en `localStorage` ANTES de mandar el
POST, y el polling arranca con ese id SIN depender de la respuesta del POST.**

Por qué: en móvil, si la pantalla se apaga durante el POST, el navegador mata la
conexión y **la respuesta se pierde**. Si dependieras de que el servidor te
devuelva el `job_id`, te quedarías sin id → sin poder sondear → "generando" para
siempre. Como el `job_id` lo creas tú, ya lo tienes pase lo que pase y siempre
puedes recuperar la imagen sondeando `status/{job_id}/`.

---

## 2. Endpoints

### 2.1. `POST generate/concatenate-prompts/` — Encolar

**Body:** el payload de siempre **+ un campo `job_id` que generas tú**.

```json
{
  "job_id": "3f9c0b1e6d4a4f...",   // UUID generado por el frontend
  "code": "MOMO",
  "character": "...",
  "skin": "...",
  "pose": "...",
  "emotion": "...",
  "image": "...",
  "clip_skip": 2,
  "additionalSpecial": ["...", "..."]
}
```

**Respuesta OK — `202 Accepted`:**
```json
{ "job_id": "3f9c0b1e6d4a4f..." }
```

**Idempotente:** si reenvías el POST con un `job_id` que ya existe, el backend
**no regenera**; devuelve `202 { job_id }` otra vez. Reintentar es seguro.

**Errores síncronos:**

| Código | Significado | Qué hace el frontend |
|--------|-------------|----------------------|
| `406`  | Código inválido / agotado | Limpiar el código introducido |
| `423`  | Ocupado (ya hay una generación en curso) | Reintentar el POST solo, a los ~2 s |
| `4xx/5xx` con `{ "error": "..." }` | Tier insuficiente, recurso no encontrado, "AI unavailable", etc. | Mostrar `error` en un toast |

> El `tier` y los usos restantes **NO** vienen aquí. Llegan al final, con el
> resultado (estado `completed`).

---

### 2.2. `GET generate/status/{job_id}/` — Sondear (polling)

Llamar **cada 3 s** mientras el job no haya terminado, y también **de inmediato
cada vez que la pestaña vuelve a ser visible** (al desbloquear el móvil).

**Siempre responde `200`** con uno de estos cuerpos:

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
  "images": ["<base64 de la imagen>"],
  "tier": "premium",
  "uses_left": 3,
  "code": "MOMO"
}
```
> `images` es un array; usar `images[0]`. `tier`, `uses_left` y `code` son los que
> antes venían en la respuesta síncrona.

**Terminado con error / job inexistente o expirado:**
```json
{ "status": "failed", "error": "..." }
```

**Cómo tratarlo:**
- `pending` / `processing` → seguir sondeando.
- `completed` → mostrar `images[0]`, guardar tier/uses_left/code, **parar el
  polling** y **limpiar `localStorage`**.
- `failed` → mostrar `error`, **parar el polling** y **limpiar `localStorage`**.
- Un fallo de red puntual en este GET es **transitorio**: reintentar solo, no
  romper. (El backend devuelve `200 { status: "failed" }` incluso para un job que
  no existe, justo para que el reintento no se quede en bucle.)

---

### 2.3. `POST generate/cancel/{job_id}/` — Cancelar (opcional)

Llamar **best-effort** cuando el usuario pulsa "Cancelar", para no gastar el uso
del código si aborta. La respuesta (`204`) no se usa; ignorar éxito o fallo.

---

## 3. Flujo recomendado en el frontend

```js
// --- Al pulsar "Generar" ---
const job_id = crypto.randomUUID();
// 1) Persistir ANTES de la petición
localStorage.setItem("gen_job", JSON.stringify({ job_id, startTime: Date.now() }));

// 2) Encolar (si la respuesta se pierde, da igual: ya tenemos job_id)
try {
  await api.post("generate/concatenate-prompts/", { job_id, ...payload });
} catch (e) {
  // 423 -> reintentar en 2s; 406 -> limpiar code; otro -> toast(e.error)
}

// 3) Arrancar el polling con NUESTRO job_id, pase lo que pase con el POST
startPolling(job_id);


// --- Polling ---
async function pollOnce(job_id) {
  const { status, images, error, tier, uses_left, code } =
    await api.get(`generate/status/${job_id}/`);   // reintentar solo si falla la red

  if (status === "completed") {
    showImage(images[0], { tier, uses_left, code });
    localStorage.removeItem("gen_job");
    return stop();
  }
  if (status === "failed") {
    toast(error);
    localStorage.removeItem("gen_job");
    return stop();
  }
  // pending | processing -> seguir (cada 3s + refetch al volver a foco)
}


// --- Al arrancar la app / recuperar visibilidad ---
// Si hay un gen_job guardado, reanudar el polling: recoge la imagen aunque
// el móvil se haya bloqueado o la página se haya recargado.
const saved = JSON.parse(localStorage.getItem("gen_job") || "null");
if (saved?.job_id) startPolling(saved.job_id);
```

**Puntos clave:**
- **Persistir `{ job_id, startTime }` en `localStorage` antes del POST.**
- **Polling cada 3 s** + refetch inmediato al recuperar foco/visibilidad.
- **Reintentar** ante fallos de red del GET (son transitorios).
- Al llegar `completed` o `failed`: parar, limpiar `localStorage`, mostrar
  imagen o error.

---

## 4. Notas

- El resultado vive en el servidor **15 min** (TTL). Si el usuario vuelve después
  de ese tiempo, `status/` devolverá `200 { status: "failed", error: "..." }` y
  se mostrará el error limpiamente (la imagen ya expiró).
- Solo hay **una generación a la vez** (uso de un solo usuario, secuencial). Si se
  intenta otra mientras hay una en curso, el POST responde `423`.
