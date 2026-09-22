# arquivo criado para definir os schemas bases de acessórios e evitar
# importações circulares entre schemas/accessory.py e schemas/centralizer.py

from datetime import datetime

from pydantic import BaseModel, field_validator
from typing import Optional

from schemas.users_analyze_acessories import UserAnalyzeAccessorySchema
from schemas.wells_use_accessories import WellUseAccessorySchema


class AccessoryBaseCreateSchema(BaseModel):
    """ Define como um novo acessório a ser inserido deve ser representado
    """
    name: str = "Centralizador 10 3/4 x 13 1/2"
    manufacturer: str = "Fabricante"
    outer_diameter: float = 10.95
    casing_size: float = 10.75
    external_use_cases: Optional[str] = "Poço da Shell, sem arraste, perfil bom"


class AccessoryBaseUpdateSchema(BaseModel):
    """Define os campos comuns aceitos na atualização de um acessório."""
    material_number: int = 1
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    outer_diameter: Optional[float] = None
    casing_size: Optional[float] = None
    external_use_cases: Optional[str] = None

    @field_validator(
        "name",
        "manufacturer",
        "outer_diameter",
        "casing_size",
        "external_use_cases",
        mode="before",
    )
    @classmethod
    def convert_null_string_to_none(cls, value):
        return None if value == "null" else value


class AccessoryBaseSearchSchema(BaseModel):
    """ Define como um acessório deve ser representado para fins de busca.
    """
    material_number: Optional[int] = 1
    # desejo filtrar pelos campos abaixo, mas acho que isso deve ser feito pelo front
    # e passar apenas o ID do acessório, então não vou implementar por enquanto.
    #name: Optional[str] = "Centralizador 10 3/4 x 13 1/2"
    #manufacturer: Optional[str] = "Fabricante"
    #casing_size: Optional[float] = 10.75


class AccessoryBaseListSchema(BaseModel):
    """ Define como uma lista de acessórios deve ser representada
    """
    material_number: int = 1
    accesory_type: str = "Centralizer"
    name: str = "Centralizador 10 3/4 x 13 1/2"
    manufacturer: str = "Fabricante"
    casing_size: float = 10.75
    last_update_date: datetime = datetime.now()


class UserInAccessorySchema(BaseModel):
    """ Define como um usuário deve ser representado dentro de um acessório.
    """
    user_id: int
    name: str
    relationship: UserAnalyzeAccessorySchema


class WellInAccessorySchema(BaseModel):
    """ Define como um poço deve ser representado dentro de um acessório.
    """
    well_id: int
    name: str
    relationship: WellUseAccessorySchema


class AccessoryBaseViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + usuários e poços associados.
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


class AccessoryBaseDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    accessory_type: str
    name: str
    material_number: int
    manufacturer: str
