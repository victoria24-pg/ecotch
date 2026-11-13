class RegistroTiempo:
    """Registra las horas trabajadas."""
    def __init__(self, id_registro: str, fecha: str, horas: float, descripcion: str):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion