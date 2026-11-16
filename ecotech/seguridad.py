import os
import re
import bcrypt
from dotenv import load_dotenv

def cargar_configuracion() -> dict:
    load_dotenv()
    claves_requeridas = [
        "API_TOKEN_CLIMA",
        "BASE_URL_CLIMA",
        "API_TOKEN_MONEDA",
        "BASE_URL_MONEDA",
    ]
    config = {clave: os.environ.get(clave, "").strip() for clave in claves_requeridas}
    faltantes = [k for k, v in config.items() if not v]
    if faltantes:
        raise SystemExit(
            f"Error de configuración: Faltan variables críticas en .env ({', '.join(faltantes)})."
        )
    config["DB_PATH"] = os.environ.get("DB_PATH", "ecotech_local.db").strip()
    return config

def hashear_password(password_plano: str) -> str:
    if not isinstance(password_plano, str) or len(password_plano) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    sal = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password_plano.encode("utf-8"), sal).decode("utf-8")

def verificar_password(intento_pwd: str, hash_guardado: str) -> bool:
    if not intento_pwd or not hash_guardado:
        return False
    return bcrypt.checkpw(intento_pwd.encode("utf-8"), hash_guardado.encode("utf-8"))

def validar_usuario(username: str) -> bool:
    return isinstance(username, str) and bool(re.match(r"^[a-zA-Z0-9_]{4,20}$", username.strip()))

def validar_ciudad(ciudad: str) -> bool:
    return isinstance(ciudad, str) and bool(re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-]{2,40}$", ciudad.strip()))

def validar_moneda(moneda: str) -> bool:
    return isinstance(moneda, str) and bool(re.match(r"^[A-Z]{3}$", moneda.strip()))

def parsear_clima_seguro(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Estructura de respuesta climática inválida.")
    main_data = payload.get("main") if isinstance(payload.get("main"), dict) else {}
    weather_list = payload.get("weather") if isinstance(payload.get("weather"), list) else [{}]
    primer_clima = weather_list[0] if weather_list and isinstance(weather_list[0], dict) else {}

    temp = main_data.get("temp")
    humedad = main_data.get("humidity")
    if temp is None or humedad is None:
        raise ValueError("La API de clima no entregó temperatura o humedad válidas.")

    return {
        "temperatura": float(temp),
        "humedad": int(humedad),
        "estado": str(primer_clima.get("description", "Sin descripción")).strip(),
    }

def parsear_moneda_seguro(payload: dict) -> float:
    if not isinstance(payload, dict):
        raise ValueError("Estructura de respuesta económica inválida.")
    valor = payload.get("valor") or payload.get("rate")
    if valor is None or float(valor) <= 0:
        raise ValueError("La API económica devolvió un tipo de cambio inválido.")
    return float(valor)
