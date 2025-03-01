from pulsar import Client
from pulsar.schema import AvroSchema
import logging
import traceback
from saludTech_anonimizador.modulos.anonimizador.aplicacion.servicios import ServicioImagenMedica
from saludTech_anonimizador.modulos.anonimizador.aplicacion.mapeadores import (
    MapeadorImagenMedicaDTOJson,
)

from saludTech_anonimizador.modulos.anonimizador.infraestructura.schemas.v1.comandos import (
    ComandoValidarAnonimizado
)
from saludTech_anonimizador.seedwork.infraestructura import utils


def suscribirse_a_eventos(app):
    cliente = None
    try:
        cliente = Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "comandos-validar-anonimizado",
            subscription_name="saludTech_anonimizador-sub-comandos-validar",
            schema=AvroSchema(ComandoValidarAnonimizado),
        )

        while True:
            mensaje = consumidor.receive()
            print(f"Evento recibido: {mensaje.value().data}")

            consumidor.acknowledge(mensaje)
    except:
        logging.error("ERROR: Suscribiendose al tópico de eventos!")
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app):
    cliente = None
    try:
        cliente = Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            "comandos-validar-anonimizado",
            subscription_name="saludTech_comandos-validar-anonimizado",
            schema=AvroSchema(EventoImagenCargada),
        )

        while True:
            mensaje = consumidor.receive()
            print(f"Comando recibido: {mensaje.value().data}")
            consumidor.acknowledge(mensaje)
            with app.test_request_context():
                imagen_medica_dict = mensaje.value().data.__dict__
                print("===========dict===========")
                print(imagen_medica_dict)
                print("===========dict===========")

                map_imagen_medica = MapeadorImagenMedicaDTOJson()

                imagen_medica_dto = map_imagen_medica.externo_a_dto(imagen_medica_dict)

                print("===========map_imagen_medica===========")
                print(imagen_medica_dto)
                print("===========map_imagen_medica===========")

                servicio_imagen_medica = ServicioImagenMedica()
                dto_final = servicio_imagen_medica.crear_imagen_medica(imagen_medica_dto)

                print("===========dto_final===========")
                print(dto_final)
                print("===========dto_final===========")
    except:
        logging.error("ERROR: Suscribiendose al tópico de comandos!")
        traceback.print_exc()
        if cliente:
            cliente.close()
