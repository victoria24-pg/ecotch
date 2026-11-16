from getpass import getpass
from seguridad import (
    cargar_configuracion,
    validar_usuario,
    validar_ciudad,
    validar_moneda,
    parsear_clima_seguro,
    parsear_moneda_seguro,
)
from cliente_api import ClienteApiSeguro
from repositorio_db import RepositorioEcoTech
from modelos import Empleado, InformeProyectoClima, InformeNominaInternacional

def consultar_clima_con_respaldo(cliente: ClienteApiSeguro, repo: RepositorioEcoTech, config: dict, ciudad: str) -> tuple[dict | None, str]:
    try:
        # PLAN A: Datos frescos desde la API
        raw = cliente.get_json(config["BASE_URL_CLIMA"], config["API_TOKEN_CLIMA"], params={"q": ciudad})
        datos = parsear_clima_seguro(raw)
        repo.guardar_clima_idempotente(ciudad, datos)
        return datos, "API EN VIVO (Plan A)"
    except Exception:
        # PLAN B: Respaldo desde SQLite local
        cache = repo.obtener_ultimo_clima(ciudad)
        if cache:
            return cache, f"CACHÉ LOCAL del {cache['actualizado_en']} (Plan B)"
        # PLAN C: Sin red ni respaldo previo
        return None, "SERVICIO NO DISPONIBLE (Plan C)"

def consultar_moneda_con_respaldo(cliente: ClienteApiSeguro, repo: RepositorioEcoTech, config: dict, moneda: str) -> tuple[float | None, str]:
    try:
        # PLAN A
        raw = cliente.get_json(config["BASE_URL_MONEDA"], config["API_TOKEN_MONEDA"], params={"moneda": moneda})
        valor = parsear_moneda_seguro(raw)
        repo.guardar_indicador_idempotente(moneda, valor)
        return valor, "API EN VIVO (Plan A)"
    except Exception:
        # PLAN B
        cache = repo.obtener_ultimo_indicador(moneda)
        if cache:
            return cache["tipo_cambio"], f"CACHÉ LOCAL del {cache['actualizado_en']} (Plan B)"
        # PLAN C
        return None, "SERVICIO NO DISPONIBLE (Plan C)"

def ejecutar_sistema():
    config = cargar_configuracion()
    repo = RepositorioEcoTech(config["DB_PATH"])
    cliente = ClienteApiSeguro()

    # Usuario administrador inicial (idempotente, almacenado con hash bcrypt + salt)
    repo.registrar_usuario_idempotente("admin_ecotech", "EcoTech2026#")

    print("=== SISTEMA DE GESTIÓN OPERATIVA Y FINANCIERA - ECOTECH SOLUTIONS ===")
    usuario = input("Usuario: ").strip()
    clave = getpass("Contraseña: ")

    if not validar_usuario(usuario) or not repo.autenticar_usuario(usuario, clave):
        print("Acceso denegado: credenciales inválidas.")
        repo.cerrar()
        return

    ciudad = input("Ciudad del proyecto sostenible (ej. Santiago): ").strip()
    moneda = input("Moneda de pago internacional (ej. USD, EUR): ").strip().upper()

    if not validar_ciudad(ciudad) or not validar_moneda(moneda):
        print("Error de validación: formato de ciudad o código de moneda inválido.")
        repo.cerrar()
        return

    clima, origen_clima = consultar_clima_con_respaldo(cliente, repo, config, ciudad)
    tipo_cambio, origen_moneda = consultar_moneda_con_respaldo(cliente, repo, config, moneda)

    informes = []
    if clima:
        informes.append(InformeProyectoClima("Planta Solar Norte", ciudad, clima, origen_clima))
    else:
        print(f"[Aviso Clima] {origen_clima}: No hay datos locales previos para {ciudad}.")

    if tipo_cambio:
        empleado = Empleado("18.456.789-2", "Camila Rojas", "2025-03-01", 1800000)
        monto = empleado.calcular_pago_internacional(tipo_cambio)
        informes.append(InformeNominaInternacional("Pago Internacional", empleado, moneda, monto, origen_moneda))
    else:
        print(f"[Aviso Divisas] {origen_moneda}: No hay registros locales previos para {moneda}.")

    print("\n=== RESULTADOS DEL SISTEMA ===")
    for inf in informes:
        print(inf.exportar())

    repo.cerrar()

if __name__ == "__main__":
    ejecutar_sistema()
