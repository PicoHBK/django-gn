# Backend — Configuración de TTL del job de generación (15 min)

> Complemento de `BACKEND_generate_async_spec.md`. Aquí se fija el **TTL** del
> estado/resultado del job y se explica **qué afecta y qué NO afecta** ponerlo
> en 15 minutos, además de los casos límite que hay que cubrir.

---

## 0. Contexto de uso — IMPORTANTE (léelo primero)

Este servicio lo usa **un solo usuario**, y **siempre de forma secuencial**:
nunca se lanzan dos generaciones a la vez (como mucho el mismo usuario en 2
dispositivos, pero jamás generando en paralelo).

Consecuencias para el backend — **NO hace falta** (evita complejidad innecesaria):

- ❌ **Sin locks ni control de concurrencia.** No habrá generaciones simultáneas.
- ❌ **Sin optimización de memoria.** Guardar la imagen en **base64 dentro de
  Redis está perfectamente bien**; no hace falta almacenamiento de objetos ni
  URLs. Como mucho hay 1 job vivo a la vez.
- ❌ **El `423` (ocupado) es prácticamente irrelevante.** Puedes dejarlo o no.
- ✅ Como el uso es tan ligero, puedes subir el TTL a 30-60 min sin coste alguno
  si quieres margen (ver sección 1).

Lo que **sí** hay que respetar aunque sea un solo usuario (no depende del número
de usuarios, sino de la robustez del flujo): las secciones **1** (TTL) y sobre
todo la **3** (job inexistente → `200 { "status": "failed" }`, nunca `404`).

---

## 1. Decisión: TTL = 15 minutos

El resultado de cada job (`{ status, images, tier, uses_left, code, error }`)
debe persistir en Redis/DB durante **15 minutos (900 segundos)** desde que se
crea/actualiza.

**Por qué 15 min:**
- La generación tarda 10-60s.
- En móvil el usuario bloquea la pantalla y vuelve más tarde. 15 min cubre de
  sobra el caso "lo dejo generando y vuelvo en unos minutos".
- Si más adelante quieres cubrir "lo dejo y vuelvo en media hora", sube a 30-60 min.

```python
TTL = 900  # segundos = 15 minutos
cache.set(f"job:{job_id}", data, timeout=TTL)
```

> Importante: refrescar el `timeout` en **cada escritura** de estado
> (`pending` → `processing` → `completed`), para que los 15 min se cuenten desde
> el final de la generación y no desde el encolado.

---

## 2. ¿Poner 15 min afecta a otras cosas?

**Resumen: no afecta a la lógica de negocio.** No cambia el consumo de códigos,
ni la concurrencia, ni colisiona entre usuarios (cada job tiene su `job_id`
único). Los únicos puntos a vigilar:

### 2.1. Memoria (el único impacto real)
Mantener el resultado 15 min significa que ocupa espacio durante ese tiempo.

- Si guardas la imagen en **base64 dentro de Redis**, cada job puede pesar cientos
  de KB o varios MB.
- **En este servicio (1 usuario, secuencial) esto es irrelevante:** como mucho hay
  1 job vivo a la vez, así que base64 en Redis es la opción correcta y más simple.
  El TTL de 15 min hace que expire solo; la memoria está acotada.
- **Solo si algún día escalas a muchos usuarios simultáneos** valdría la pena
  guardar la imagen en disco / almacenamiento de objetos / DB y dejar en el cache
  únicamente la **URL o referencia**. Hoy no hace falta (ver Sección 0).

### 2.2. Consumo de código / usos — NO se ve afectado
El TTL solo controla cuánto vive el **resultado** para que el cliente lo recoja.
No cambia cuándo se descuenta el uso. Mantén la regla: **descontar el uso al
completar con éxito** (no al encolar). Si el job falla o se cancela, no se cobra.

### 2.3. Re-consulta tras completado — inofensivo
Cuando el job llega a `completed`, el resultado sigue en cache hasta 15 min. El
frontend lo recoge una vez, muestra la imagen y limpia su `localStorage`. Que el
resultado siga cacheado un rato más no causa problemas (a lo sumo, si el usuario
recargara, volvería a leer el mismo resultado, lo cual es correcto).

### 2.4. Colisiones entre generaciones — no hay
Cada generación crea un `job_id` nuevo. Un usuario que genera varias veces tiene
varias entradas independientes. Sin colisión.

---

## 3. Caso límite CRÍTICO: usuario vuelve DESPUÉS del TTL

Si el usuario vuelve pasados los 15 min, el job ya expiró y no existe en cache.
El frontend hará `GET generate/status/{job_id}/` sobre un id desconocido.

**El backend DEBE responder así:**

```json
HTTP 200
{ "status": "failed", "error": "Job not found or expired" }
```

⚠️ **NO devolver `404` (ni otro `4xx/5xx`) en este caso.**

Motivo: el frontend trata los errores HTTP/red del polling como **transitorios**
y **reintenta automáticamente** (para sobrevivir a cortes de red mientras la
pantalla está bloqueada). Si devuelves `404`, el frontend reintentaría en bucle
para siempre y la UI se quedaría **colgada en "generando"**.

En cambio, con `200 { "status": "failed", ... }` el frontend corta el polling,
limpia el estado y muestra el error limpiamente.

> Regla general del endpoint de estado: **mientras puedas, responde siempre `200`
> con un `status` válido** (`pending` / `processing` / `completed` / `failed`).
> Reserva los códigos de error HTTP solo para fallos reales del servidor.

---

## 4. Resumen de tiempos

| Momento en que el usuario vuelve | Resultado |
|----------------------------------|-----------|
| Durante la generación (0-60s)    | Sigue en `processing`, luego `completed`. ✅ |
| Después de generar, < 15 min     | `completed` con la imagen. ✅ Se recupera. |
| Después de 15 min                | Expirado → `200 { status: "failed" }` → error limpio. ❌ imagen perdida (esperado). |

---

## 5. Checklist

- [ ] TTL del estado del job = **900s (15 min)**, refrescado en cada actualización de estado.
- [ ] Estado en Redis/DB (no en memoria del proceso), para sobrevivir a reinicios.
- [ ] Imagen en base64 dentro de Redis está bien (1 usuario). URL/referencia solo si escalas a muchos usuarios.
- [ ] Job inexistente/expirado → **`200 { "status": "failed", "error": "..." }`**, nunca `404`.
- [ ] El uso/código se descuenta al **completar con éxito**, no al encolar.
