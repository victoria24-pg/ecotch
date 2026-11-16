import logging
import random
import time
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class ErrorApiNoRecuperable(Exception):
    """Error 4xx o falla de configuración que no debe reintentarse."""

class ClienteApiSeguro:
    def __init__(self, max_intentos: int = 3, timeout: tuple = (3, 10)):
        self.max_intentos = max_intentos
        self.timeout = timeout

    def _renovar_token(self, token_actual: str) -> str:
        # Simulación controlada de renovación ante 401
        logging.info("Detectado código 401. Intentando renovar credencial una vez...")
        return token_actual

    def get_json(self, url: str, token: str, params: dict | None = None, reintento_401: bool = True) -> dict:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        for intento in range(1, self.max_intentos + 1):
            try:
                # TLS siempre activo por defecto (prohibido verify=False)
                resp = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout,
                )

                if resp.status_code == 200:
                    return resp.json()

                if resp.status_code == 401 and reintento_401:
                    nuevo_token = self._renovar_token(token)
                    return self.get_json(url, nuevo_token, params=params, reintento_401=False)

                if resp.status_code in (401, 403, 404):
                    raise ErrorApiNoRecuperable(
                        f"El servicio externo rechazó la solicitud (HTTP {resp.status_code})."
                    )

                if resp.status_code == 429:
                    espera = int(resp.headers.get("Retry-After", 2 ** intento))
                    logging.warning(f"Cuota excedida (429). Esperando {espera}s (intento {intento}/{self.max_intentos}).")
                    time.sleep(espera)
                    continue

                if 500 <= resp.status_code <= 503:
                    raise requests.exceptions.HTTPError(f"Fallo temporal del servidor ({resp.status_code})")

                raise ErrorApiNoRecuperable(f"Respuesta HTTP inesperada ({resp.status_code}).")

            except requests.exceptions.ConnectionError as err:
                logging.error("Sin conexión de red al intentar contactar la API.")
                raise ConnectionError("No hay conexión con el servicio externo.") from err

            except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as err:
                if intento == self.max_intentos:
                    logging.error(f"Se agotaron los {self.max_intentos} reintentos.")
                    raise
                espera = (2 ** (intento - 1)) + random.uniform(0.1, 0.5)
                logging.warning(f"Fallo temporal ({err}). Reintentando en {espera:.2f}s...")
                time.sleep(espera)

        raise RuntimeError("No se pudo obtener respuesta válida del servicio externo.")
