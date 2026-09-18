from typing import List

from pydantic import BaseModel

from schemas.accessory import AccessorySearchSchema
from schemas.users_analyze_acessories import UserAnalyzeAccessorySchema


class UserSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    name: str = "João Bosco de Carvalho Júnior"

class AccessoryInUserSchema(BaseModel):
    accessory_id: int
    name: str
    manufacturer: str
    relationship: UserAnalyzeAccessorySchema

class UserWithAccessoriesSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    name: str = "João Bosco de Carvalho Júnior"
    accessories: list[AccessoryInUserSchema] = []
