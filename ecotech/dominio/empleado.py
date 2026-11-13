from dominio.persona import Persona

class Empleado(Persona):
    """Representa un empleado. Hereda de Persona."""
    def __init__(self, rut: str, nombre: str, correo: str, fecha_ingreso: str, sueldo_base: float):
        super().__init__(rut, nombre, correo)
        self.fecha_ingreso = fecha_ingreso
        self.sueldo_base = sueldo_base
        self.registros = []      # Lista vacía para cardinalidad 1..*
        self.departamento = None # Puede ser None para cardinalidad 0..1

    def registrar_hora(self, registro):
        self.registros.append(registro)

    def total_horas(self) -> float:
        return sum(reg.horas for reg in self.registros)