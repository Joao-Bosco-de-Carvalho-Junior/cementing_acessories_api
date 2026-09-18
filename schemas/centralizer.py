from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List, Annotated, Literal

from model.centralizer import Centralizer
from schemas.accessory import AccessoryBaseCreateSchema, AccessoryBaseSearchSchema, AccessoryBaseListSchema, AccessoryBaseViewSchema, AccessoryBaseDelSchema


class CentralizerSchema(AccessoryBaseCreateSchema):
    accessory_type: Literal["centralizer"] = "centralizer"
    restoring_force: Optional[float] = 1250
    running_force: Optional[float] = 1000
    well_id: float = 13.5
    type: str = "Flexível"


class CentralizerSearchSchema(AccessoryBaseSearchSchema):
    """ Define como deve ser a estrutura que representa a busca.
    """
    type: Optional[str] = "Flexível"
    well_id: Optional[float] = 13.5

class CentralizerBaseListSchema(AccessoryBaseListSchema):
    """ Define como um novo acessório a ser inserido deve ser representado
    """
    type: str = "Flexível"
    well_id: float = 13.5


class CentralizerListSchema(BaseModel):
    """ Define como uma listagem de acessórios será retornada.
    """
    acessories:List[CentralizerBaseListSchema]


class CentralizerViewSchema(AccessoryBaseViewSchema):
    """ Define como um produto será retornado: produto + comentários.
    """
    restoring_force: float = 1250
    running_force: float = 1000
    well_id: float = 13.5
    type: str = "Flexível"


class CentralizerDelSchema(AccessoryBaseDelSchema):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    pass

def append_centralizer(centralizer: Centralizer, result):
    """ Retorna uma representação do centralizador seguindo o schema definido em
        CentralizerViewSchema.
    """
    result.append({
        "type": centralizer.type,
        "well_id": centralizer.well_id,
    })

def show_centralizers(centralizers: List[Centralizer]):
    """ Retorna uma representação do centralizador seguindo o schema definido em
        CentralizerListSchema.
    """
    result = []
    for centralizer in centralizers:
        append_centralizer(centralizer, result)

    return {"centralizers": result}

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
