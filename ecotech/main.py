from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.registro_tiempo import RegistroTiempo

def main():
    dep = Departamento("Operaciones")
    ana = Empleado("12345678-9", "Ana Rojas", "ana@ecotech.cl", "2024-03-01", 950000)
    dep.agregar_empleado(ana)

    reg1 = RegistroTiempo("REG-01", "2026-09-15", 4.5, "Desarrollo POO")
    ana.registrar_hora(reg1)

    print(f"Departamento: {dep.nombre}")
    print(f"Empleado: {ana.nombre} (RUT: {ana.rut})")
    print(f"Horas totales: {ana.total_horas()} hrs")

if __name__ == "__main__":
    main()