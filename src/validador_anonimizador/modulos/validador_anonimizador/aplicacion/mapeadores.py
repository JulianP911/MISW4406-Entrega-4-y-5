from validador_anonimizador.seedwork.aplicacion.dto import Mapeador as AppMap
from validador_anonimizador.seedwork.dominio.repositorios import Mapeador as RepMap
from validador_anonimizador.modulos.validador_anonimizador.dominio.entidades import (
    ImagenMedica,
)
from .dto import ImagenMedicaDTO


class MapeadorImagenMedicaDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ImagenMedicaDTO:
        imagen_medica_dto = ImagenMedicaDTO(
            url=externo["url"],
        )

        return imagen_medica_dto

    def dto_a_externo(self, dto: ImagenMedicaDTO) -> dict:
        return dto.__dict__


class MapeadorImagenMedica(RepMap):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def obtener_tipo(self) -> type:
        return ImagenMedica.__class__

    def entidad_a_dto(self, entidad: ImagenMedica) -> ImagenMedicaDTO:
        fecha_creacion = None
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)

        return ImagenMedicaDTO(
            entidad.id,
            entidad.url,
            entidad.validated,
            fecha_actualizacion=fecha_actualizacion,
            fecha_creacion=fecha_creacion,
        )

    def dto_a_entidad(self, dto: ImagenMedicaDTO) -> ImagenMedica:
        return ImagenMedica(
            id=dto.id,
            url=dto.url,
            validated=dto.validated,
        )
