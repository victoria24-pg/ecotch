class Departamento:
    """Representa un departamento de la empresa."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.empleados = [] # Lista vacía

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)
        empleado.departamento = self