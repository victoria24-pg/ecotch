from abc import ABC, abstractmethod

class Persona:
    def __init__(self, rut: str, nombre: str):
        self.rut = rut
        self.nombre = nombre

class Empleado(Persona):
    def __init__(self, rut: str, nombre: str, fecha_ingreso: str, sueldo_base_clp: float):
        super().__init__(rut, nombre)
        self.fecha_ingreso = fecha_ingreso
        self._sueldo_base_clp = 0.0
        self.sueldo_base_clp = sueldo_base_clp

    @property
    def sueldo_base_clp(self) -> float:
        return self._sueldo_base_clp

    @sueldo_base_clp.setter
    def sueldo_base_clp(self, valor: float):
        if valor < 0:
            raise ValueError("El sueldo base no puede ser negativo.")
        self._sueldo_base_clp = valor

    def calcular_pago_internacional(self, tipo_cambio: float) -> float:
        if tipo_cambio <= 0:
            raise ValueError("El tipo de cambio debe ser mayor a cero.")
        return round(self._sueldo_base_clp / tipo_cambio, 2)

class Informe(ABC):
    def __init__(self, titulo: str):
        self.titulo = titulo

    @abstractmethod
    def exportar(self) -> str:
        pass

class InformeProyectoClima(Informe):
    def __init__(self, titulo: str, ciudad: str, clima: dict, origen: str):
        super().__init__(titulo)
        self.ciudad = ciudad
        self.clima = clima
        self.origen = origen

    def exportar(self) -> str:
        alerta = "REPROGRAMAR ACTIVIDADES EXTERNAS" if self.clima["humedad"] > 85 else "CONDICIONES APTAS"
        return (
            f"[PROYECTO - {self.origen}] {self.titulo} ({self.ciudad}): "
            f"{self.clima['temperatura']}°C, {self.clima['estado']}, "
            f"Humedad {self.clima['humedad']}% -> {alerta}"
        )

class InformeNominaInternacional(Informe):
    def __init__(self, titulo: str, empleado: Empleado, moneda: str, monto_extranjero: float, origen: str):
        super().__init__(titulo)
        self.empleado = empleado
        self.moneda = moneda
        self.monto_extranjero = monto_extranjero
        self.origen = origen

    def exportar(self) -> str:
        return (
            f"[NÓMINA - {self.origen}] {self.empleado.nombre} ({self.empleado.rut}): "
            f"${self.empleado.sueldo_base_clp:,.0f} CLP -> {self.monto_extranjero:,.2f} {self.moneda}"
        )
