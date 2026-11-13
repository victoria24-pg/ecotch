class Persona:
    """Clase base que representa una persona."""
    def __init__(self, rut:str, nombre: str, correo: str):
        self.rut = rut  # RUT siempre como texto (string)
        self.nombre = nombre
        self.correo = correo