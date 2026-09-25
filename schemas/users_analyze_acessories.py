from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserAnalyzeAccessorySchema(BaseModel):
    """ Define como deve ser a estrutura que representa a análise do usuário 
        sobre o acessório.
    """
    comment: Optional[str] = "Nada a declarar"
    approval: bool = True

class UserAnalyzeAccessoryCreateSchema(UserAnalyzeAccessorySchema):
    """Define os dados necessários para análise de um acessório por um usuário."""
    user_id: int = 1
    accessory_id: int = 1