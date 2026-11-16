# Bitácora de Auditoría Técnica de Código Asistido por IA (ES3)

## 1. Consultas SQL dinámicas (Inyección SQL)
* **Prompt / Contexto:** Generación de funciones para guardar y consultar datos climáticos en SQLite.
* **Hallazgo inicial de IA:** La IA propuso `cursor.execute(f"SELECT * FROM clima WHERE ciudad = '{ciudad}'")`.
* **Decisión:** MODIFICADO.
* **Justificación técnica:** La interpolación de strings (`f-strings`) en SQL permite ataques de inyección SQL. Se reemplazó por consultas parametrizadas con placeholders (`?`) en `repositorio_db.py`.

## 2. Validación de certificados SSL/TLS (`verify=False`)
* **Prompt / Contexto:** Manejo de errores de conexión HTTPS con `requests`.
* **Hallazgo inicial de IA:** Sugirió `requests.get(url, verify=False)` para evitar fallos de certificado local.
* **Decisión:** DESCARTADO.
* **Justificación técnica:** Desactivar la verificación TLS expone el tráfico y los tokens `Bearer` a ataques *Man-in-the-Middle* (MitM). Se mantuvo la verificación activa por defecto.

## 3. Silenciamiento de excepciones (`except: pass`)
* **Prompt / Contexto:** Control de fallos al consultar el servicio externo de divisas.
* **Hallazgo inicial de IA:** Generó un bloque `except Exception: pass` que ocultaba el error y dejaba variables en `None`.
* **Decisión:** MODIFICADO.
* **Justificación técnica:** Ocultar excepciones impide diagnosticar caídas y provoca errores posteriores (`TypeError`). Se implementó registro en `logging` y degradación controlada hacia el Plan B (caché en SQLite) y Plan C.

## 4. Peticiones HTTP sin tiempo límite (`timeout`)
* **Prompt / Contexto:** Cliente base para consumir la API de clima.
* **Hallazgo inicial de IA:** Llamada `requests.get(url, headers=headers)` sin parámetro `timeout`.
* **Decisión:** MODIFICADO.
* **Justificación técnica:** Sin `timeout`, si el servidor externo no responde, el hilo queda bloqueado indefinidamente. Se configuró `timeout=(3, 10)` y reintentos con espera exponencial (*backoff*).

## 5. Verificación de paquetes en PyPI
* **Prompt / Contexto:** Solicitud de librerías para encriptación de contraseñas y variables de entorno.
* **Hallazgo inicial de IA:** Sugirió paquetes reales (`requests`, `python-dotenv`, `bcrypt`) junto con una librería ficticia (`secure-env-validator`).
* **Decisión:** ACEPTADO PARCIALMENTE / DESCARTADO EL PAQUETE INEXISTENTE.
* **Justificación técnica:** Se verificó en PyPI que `requests`, `python-dotenv` y `bcrypt` son librerías oficiales mantenidas, descartando dependencias inexistentes para evitar errores de instalación o riesgo de *typosquatting*.
