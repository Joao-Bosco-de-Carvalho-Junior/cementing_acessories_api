from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, Union
from model.accessory import Accessory
from model.centralizer import Centralizer
from schemas.centralizer import CentralizerDelSchema, CentralizerSchema, CentralizerSearchSchema, CentralizerListSchema, CentralizerViewSchema, show_centralizer


class AccessoryBaseCreateSchema(BaseModel):
    """ Define como um novo acessório a ser inserido deve ser representado
    """
    name: str = "Centralizador 10 3/4 x 13 1/2"
    manufacturer: str = "Fabricante"
    outer_diameter: float = 10.95
    casing_size: float = 10.75
    external_use_cases: Optional[str] = "Poço da Shell, sem arraste, perfil bom"

AccesoryCreateSchema = Annotated[
    Union[CentralizerSchema],
    Field(discriminator="accessory_type"),
]

class AccessoryBaseSearchSchema(BaseModel):
    """ Define como um novo acessório a ser inserido deve ser representado
    """
    material_number: Optional[int] = 1
    name: Optional[str] = "Centralizador 10 3/4 x 13 1/2"
    manufacturer: Optional[str] = "Fabricante"
    casing_size: Optional[float] = 10.75


AccesorySearchSchema = Annotated[
    Union[CentralizerSearchSchema],
    Field(discriminator="accessory_type"),
]

class AccessoryBaseListSchema(BaseModel):
    """ Define como um novo acessório a ser inserido deve ser representado
    """
    material_number: int = 1
    accesory_type: str = "Centralizer"
    name: str = "Centralizador 10 3/4 x 13 1/2"
    manufacturer: str = "Fabricante"
    casing_size: float = 10.75
    last_update_date: datetime = datetime.now()


AccesoryListSchema = Annotated[
    Union[CentralizerListSchema],
    Field(discriminator="accessory_type"),
]

class UserInAccessorySchema(BaseModel):
    user_id: int
    name: str
    relationship: UserAnalyzeAccessorySchema

class WellInAccessorySchema(BaseModel):
    well_id: int
    name: str
    relationship: WellUseAccessorySchema

class AccessoryBaseViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    material_number: int = 1
    accesory_type: str = "Centralizer"
    name: str = "Centralizador 10 3/4 x 13 1/2"
    manufacturer: str = "Fabricante"
    outer_diameter: float = 10.95
    casing_size: float = 10.75
    external_use_cases: Optional[str] = "Poço da Shell, sem arraste, perfil bom"
    registration_date: datetime = datetime.now()
    last_update_date: datetime = datetime.now()
    users: list[UserInAccessorySchema] = []
    wells: list[WellInAccessorySchema] = []

AccesoryViewSchema = Annotated[
    Union[CentralizerViewSchema],
    Field(discriminator="accessory_type"),
]

class AccessoryBaseDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    accessory_type: str
    name: str
    material_number: int
    manufacturer: str

AccesoryDelSchema = Annotated[
    Union[CentralizerDelSchema],
    Field(discriminator="accessory_type"),
]

def show_accessories(accessories: List[Accessory]):
    """ Retorna uma representação do acessório seguindo o schema definido em
        AccessoryBaseListSchema.
    """
    result = []
    for accessory in accessories:
        result.append({
            "material_number": accessory.material_number,
            "accessory_type": accessory.accessory_type,
            "name": accessory.name,
            "manufacturer": accessory.manufacturer,
            "casing_size": accessory.casing_size,
            "last_update_date": accessory.last_update_date,
        })
        if isinstance(accessory, Centralizer):
            append_centralizer(accessory, result)

    return {"accessories": result}

def show_accessory(accessory: Accessory):
    """ Retorna uma representação do acessório seguindo o schema definido em
        AccessoryBaseViewSchema.
    """

    result = {
        "material_number": accessory.material_number,
        "accessory_type": accessory.accessory_type,
        "name": accessory.name,
        "manufacturer": accessory.manufacturer,
        "outer_diameter": accessory.outer_diameter,
        "casing_size": accessory.casing_size,
        "external_use_cases": accessory.external_use_cases,
        "registration_date": accessory.registration_date,
        "last_update_date": accessory.last_update_date,
        "users":[{"name": user.name, "approval": user.relationship.approval, "comment": user.relationship.comment} for user in accessory.users],
        "wells":[{"name": well.name, "anomaly": well.relationship.anomaly, "comment": well.relationship.comment} for well in accessory.wells]
    }

    if isinstance(accessory, Centralizer):
        result.append(show_centralizer(accessory))

    return result

