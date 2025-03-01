import pulsar
from pulsar.schema import AvroSchema

from anonimizador.modulos.anonimizador.infraestructura.schemas.v1.comandos import (
    ComandoValidarAnonimizado,
    ComandoValidarAnonimizadoPayload,
)
from anonimizador.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        print("===========MENSAJE===========")
        print(mensaje)
        print("===========MENSAJE===========")

        print("===========TOPICO===========")
        print(topico)
        print("===========TOPICO===========")

        print("===========SCHEMA===========")
        print(schema)
        print("===========SCHEMA===========")

        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando(self, comando, topico):

        print("===========COMANDO===========")
        print(comando)
        print("===========COMANDO===========")
        payload = ComandoValidarAnonimizadoPayload(id=comando.id, url=comando.url, token_paciente=comando.token_paciente)
        comando_integracion = ComandoValidarAnonimizado(data=payload)

        print("===========PAYLOAD===========")
        print(payload)
        print("===========PAYLOAD===========")

        print("===========COMANDO INTEGRACION===========")
        print(comando_integracion)
        print("===========COMANDO INTEGRACION===========")

        self._publicar_mensaje(
            comando_integracion, topico, AvroSchema(ComandoValidarAnonimizado)
        )
