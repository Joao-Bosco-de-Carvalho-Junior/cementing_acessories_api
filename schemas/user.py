from pydantic import BaseModel

from schemas.users_analyze_acessories import UserAnalyzeAccessorySchema

class UserSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    name: str = "JBCJ"

class UserWithIDSchema(BaseModel):
    """ Define como um usuário com ID deve ser representado
    """
    id: int = 1
    name: str = "JBCJ"


class UserSearchSchema(BaseModel):
    """Define como um usuário deve ser identificado em uma consulta."""
    id: int = 1


class UserUpdateSchema(BaseModel):
    """Define os dados necessários para atualizar um usuário."""
    id: int = 1
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
    id: int = 1
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
        "id": user.id,
        "name": user.name,
        "accessories": [
            {
                "accessory_id": link.accessory.id,
                "name": link.accessory.name,
                "manufacturer": link.accessory.manufacturer,
                "approval": link.approval,
                "comment": link.comment,
            }
            for link in user.accessories
        ],
    }


def show_users(users):
    """Retorna uma lista de usuários sem carregar relacionamentos."""
    return {"users": [{"id": user.id, "name": user.name} for user in users]}