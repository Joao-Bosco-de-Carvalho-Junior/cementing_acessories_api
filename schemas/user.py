from pydantic import BaseModel

from schemas.users_analyze_acessories import UserAnalyzeAccessorySchema

class UserSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    name: str = "JBCJ"


class UserSearchSchema(BaseModel):
    """Define como um usuário deve ser identificado em uma consulta."""
    name: str = "JBCJ"


class UserUpdateSchema(BaseModel):
    """Define os dados necessários para atualizar um usuário."""
    current_name: str = "JBCJ"
    name: str


class UserListSchema(BaseModel):
    """Define a representação da lista de usuários."""
    users: list[UserSchema]

class AccessoryInUserSchema(BaseModel):
    """ Define como um acessório deve ser representado dentro de um usuário.
    """
    accessory_id: int
    name: str
    manufacturer: str
    relationship: UserAnalyzeAccessorySchema

class UserWithAccessoriesSchema(BaseModel):
    """ Define como um novo usuário e seus acessórios devem ser representados
    """
    name: str = "JBCJ"
    accessories: list[AccessoryInUserSchema] = []

class UserDelSchema(BaseModel):
    """Define a confirmação da remoção de um usuário.
    """
    message: str
    name: str

def show_user(user):
    """Retorna um usuário e os acessórios associados a ele."""
    return {
        "name": user.name,
        "accessories": [
            {
                "accessory_id": link.accessory.material_number,
                "name": link.accessory.name,
                "manufacturer": link.accessory.manufacturer,
            }
            for link in user.accessories
        ],
    }


def show_users(users):
    """Retorna uma lista de usuários sem carregar relacionamentos."""
    return {"users": [{"name": user.name} for user in users]}