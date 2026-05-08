from abc import ABC, abstractmethod
from datetime import datetime


class Logger:

    ARCHIVO_LOG = "logs.txt"

    @staticmethod
    def registrar(mensaje):

        with open(
            Logger.ARCHIVO_LOG,
            "a",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                f"[{datetime.now()}] {mensaje}\n"
            )


class SistemaError(Exception):
    pass


class ClienteError(SistemaError):
    pass


class ServicioError(SistemaError):
    pass


class ReservaError(SistemaError):
    pass


class Persona(ABC):

    def __init__(
        self,
        nombre,
        identificacion
    ):

        self.nombre = nombre
        self.identificacion = identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass


class Cliente(Persona):

    def __init__(
        self,
        nombre,
        identificacion,
        correo,
        telefono
    ):

        super().__init__(
            nombre,
            identificacion
        )

        if "@" not in correo:
            raise ClienteError(
                "Correo inválido"
            )

        self.correo = correo
        self.telefono = telefono

    def mostrar_informacion(self):

        return (
            f"{self.nombre} "
            f"{self.correo}"
        )


class Servicio(ABC):

    def __init__(
        self,
        codigo,
        nombre,
        tarifa_base
    ):

        if tarifa_base <= 0:

            raise ServicioError(
                "Tarifa inválida"
            )

        self.codigo = codigo
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(
        self,
        duracion
    ):
        pass


class ReservaSala(Servicio):

    def __init__(
        self,
        codigo,
        nombre,
        tarifa_base,
        capacidad
    ):

        super().__init__(
            codigo,
            nombre,
            tarifa_base
        )

        self.capacidad = capacidad

    def calcular_costo(
        self,
        duracion
    ):

        return (
            self.tarifa_base
            * duracion
        )


class Reserva:

    def __init__(
        self,
        cliente,
        servicio,
        duracion
    ):

        if duracion <= 0:

            raise ReservaError(
                "Duración inválida"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

    def procesar(self):

        return self.servicio.calcular_costo(
            self.duracion
        )


class SistemaSoftwareFJ:

    def __init__(self):

        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(
        self,
        cliente
    ):

        self.clientes.append(cliente)

        Logger.registrar(
            f"Cliente registrado "
            f"{cliente.nombre}"
        )

    def registrar_servicio(
        self,
        servicio
    ):

        self.servicios.append(servicio)

        Logger.registrar(
            f"Servicio registrado "
            f"{servicio.nombre}"
        )

    def crear_reserva(
        self,
        cliente,
        servicio,
        duracion
    ):

        reserva = Reserva(
            cliente,
            servicio,
            duracion
        )

        self.reservas.append(
            reserva
        )

        Logger.registrar(
            "Reserva creada"
        )

        return reserva


def main():

    sistema = SistemaSoftwareFJ()

    try:

        cliente = Cliente(
            "Carlos",
            "1010",
            "carlos@gmail.com",
            "312456789"
        )

        sistema.registrar_cliente(
            cliente
        )

        sala = ReservaSala(
            "S01",
            "Sala VIP",
            100000,
            20
        )

        sistema.registrar_servicio(
            sala
        )

        reserva = sistema.crear_reserva(
            cliente,
            sala,
            3
        )

        costo = reserva.procesar()

        print(
            f"Costo total: {costo}"
        )

    except Exception as e:

        print(
            f"ERROR: {e}"
        )


if __name__ == "__main__":

    main()