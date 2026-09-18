from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserAnalyzeAccessorySchema(BaseModel):
    comment: Optional[str] = "Nada a declarar"
    approval: bool = True
    approval_date: Optional[datetime] = None