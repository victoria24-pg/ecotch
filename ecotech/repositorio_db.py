import sqlite3
from datetime import datetime, timezone
from seguridad import hashear_password, verificar_password

class RepositorioEcoTech:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._inicializar_tablas()

    def _inicializar_tablas(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clima_proyectos (
                ciudad TEXT NOT NULL,
                fecha TEXT NOT NULL,
                temperatura REAL NOT NULL,
                humedad INTEGER NOT NULL,
                estado TEXT NOT NULL,
                actualizado_en TEXT NOT NULL,
                PRIMARY KEY (ciudad, fecha)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS indicadores_economicos (
                moneda TEXT NOT NULL,
                fecha TEXT NOT NULL,
                tipo_cambio REAL NOT NULL,
                actualizado_en TEXT NOT NULL,
                PRIMARY KEY (moneda, fecha)
            )
        """)
        self.conn.commit()

    def registrar_usuario_idempotente(self, username: str, password_plano: str):
        pwd_hash = hashear_password(password_plano)
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO usuarios (username, password_hash) VALUES (?, ?)",
            (username.strip(), pwd_hash),
        )
        self.conn.commit()

    def autenticar_usuario(self, username: str, password_plano: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT password_hash FROM usuarios WHERE username = ?", (username.strip(),))
        fila = cur.fetchone()
        if not fila:
            return False
        return verificar_password(password_plano, fila[0])

    def guardar_clima_idempotente(self, ciudad: str, datos: dict):
        hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ahora = datetime.now(timezone.utc).isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO clima_proyectos (ciudad, fecha, temperatura, humedad, estado, actualizado_en)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(ciudad, fecha) DO UPDATE SET
                temperatura = excluded.temperatura,
                humedad = excluded.humedad,
                estado = excluded.estado,
                actualizado_en = excluded.actualizado_en
        """, (ciudad.upper(), hoy, datos["temperatura"], datos["humedad"], datos["estado"], ahora))
        self.conn.commit()

    def obtener_ultimo_clima(self, ciudad: str) -> dict | None:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT temperatura, humedad, estado, actualizado_en
            FROM clima_proyectos
            WHERE ciudad = ?
            ORDER BY fecha DESC LIMIT 1
        """, (ciudad.upper(),))
        fila = cur.fetchone()
        if not fila:
            return None
        return {
            "temperatura": fila[0],
            "humedad": fila[1],
            "estado": fila[2],
            "actualizado_en": fila[3],
        }

    def guardar_indicador_idempotente(self, moneda: str, tipo_cambio: float):
        hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ahora = datetime.now(timezone.utc).isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO indicadores_economicos (moneda, fecha, tipo_cambio, actualizado_en)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(moneda, fecha) DO UPDATE SET
                tipo_cambio = excluded.tipo_cambio,
                actualizado_en = excluded.actualizado_en
        """, (moneda.upper(), hoy, tipo_cambio, ahora))
        self.conn.commit()

    def obtener_ultimo_indicador(self, moneda: str) -> dict | None:
        cur = self.conn.cursor()
