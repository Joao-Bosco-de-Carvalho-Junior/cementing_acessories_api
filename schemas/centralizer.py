from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List, Literal

from model.centralizer import Centralizer
from schemas.accessory_base import (
    AccessoryBaseCreateSchema,
    AccessoryBaseUpdateSchema,
    AccessoryBaseSearchSchema,
    AccessoryBaseListSchema,
    AccessoryBaseViewSchema,
    AccessoryBaseDelSchema,
)


class CentralizerSchema(AccessoryBaseCreateSchema):
    """ Define como um novo centralizador a ser inserido deve ser representado
    """
    accessory_type: Literal["centralizer"] = "centralizer"
    restoring_force: Optional[float] = 1250
    running_force: Optional[float] = 1000
    well_id: float = 13.5
    type: str = "Flexível"


class CentralizerUpdateSchema(AccessoryBaseUpdateSchema):
    """Define os campos comuns e específicos na atualização de um centralizador."""
    restoring_force: Optional[float] = None
    running_force: Optional[float] = None
    well_id: Optional[float] = None
    type: Optional[str] = None

    @field_validator("restoring_force", 
                     "running_force", 
                     "well_id",
                     "outer_diameter",
                     "casing_size", 
                     "type",
                     "external_use_cases",
                     "manufacturer",
                     "name",
                     mode="before")
    @classmethod
    def convert_null_string_to_none(cls, value):
        return None if value == "null" else value


class CentralizerSearchSchema(AccessoryBaseSearchSchema):
    """ Define como deve ser a estrutura que representa a busca.
    """
    pass
    # desejo filtrar pelos campos abaixo, mas acho que isso deve ser feito pelo front
    # e passar apenas o ID do acessório, então não vou implementar por enquanto.
    #type: Optional[str] = "Flexível"
    #well_id: Optional[float] = 13.5

class CentralizerBaseListSchema(AccessoryBaseListSchema):
    """ Define os campos específicos que serão retornados na listagem de centralizadores.
    """
    type: str = "Flexível"
    well_id: float = 13.5


class CentralizerListSchema(BaseModel):
    """ Define como uma listagem de acessórios será retornada.
    """
    acessories:List[CentralizerBaseListSchema]


class CentralizerViewSchema(AccessoryBaseViewSchema):
    """ Define como um centralizador será retornado: acessório + centralizador.
    """
    restoring_force: float = 1250
    running_force: float = 1000
    well_id: float = 13.5
    type: str = "Flexível"


class CentralizerDelSchema(AccessoryBaseDelSchema):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    # não vejo necessidade de adicionar campos específicos para centralizador
    pass

def update_centralizer(centralizer: Centralizer, result):
    """ Atualiza o dicionário result com os campos específicos do centralizador
        seguindo o schema definido em CentralizerBaseListSchema.
    """
    result.update({
        "type": centralizer.type,
        "well_id": centralizer.well_id,
    })

# não estou usando esta função, mas deixei aqui para referência futura,
# caso seja necessário retornar uma listagem de centralizadores.
# parece que o update_centralizer já resolve na listagem de acessórios.
#def show_centralizers(centralizers: List[Centralizer]):
#    """ Retorna uma representação do centralizador seguindo o schema definido em
#        CentralizerListSchema.
#    """
#    result = []
#    for centralizer in centralizers:
#        update_centralizer(centralizer, result)
#
#    return {"centralizers": result}

def show_centralizer(centralizer: Centralizer):
    """ Retorna uma representação do centralizador seguindo o schema definido em
        CentralizerViewSchema.
    """
    return {
        "type": centralizer.type,
        "well_id": centralizer.well_id,
        "restoring_force": centralizer.restoring_force,
        "running_force": centralizer.running_force,
    }
