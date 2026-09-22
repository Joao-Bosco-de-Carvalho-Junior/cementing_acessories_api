from typing import Optional

from pydantic import BaseModel


class WellUseAccessorySchema(BaseModel):
    """ Define como deve ser a estrutura que representa o uso do poço 
        sobre o acessório.
    """
    comment: Optional[str] = "Nada a declarar"
    anomaly: bool = False


class WellUseAccessoryCreateSchema(WellUseAccessorySchema):
    """Define os dados necessários para associar um acessório a um poço."""
    well_id: int = 1
    accessory_id: int = 1