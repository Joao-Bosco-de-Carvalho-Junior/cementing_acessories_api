from typing import List

from pydantic import BaseModel

from schemas.accessory import AccessorySearchSchema
from schemas.wells_use_accessories import WellUseAccessorySchema


class WellSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    name: str = "7-RO-203H-RJS"

class AccessoryInWellSchema(BaseModel):
    accessory_id: int
    name: str
    manufacturer: str
    relationship: WellUseAccessorySchema

class WellWithAccessoriesSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    name: str = "7-RO-203H-RJS"
    accessories: list[AccessoryInWellSchema] = []
