from dataclasses import dataclass, field
from validador_anonimizador.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ImagenMedicaDTO(DTO):
    id: str = field(default=None)
    url: str = field(default=None)
    validated: bool = field(default=False)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
