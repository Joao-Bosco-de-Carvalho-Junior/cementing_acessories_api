from typing import Optional

from pydantic import BaseModel


class WellUseAccessorySchema(BaseModel):
    comment: Optional[str] = "Nada a declarar"
    anomaly: bool = False