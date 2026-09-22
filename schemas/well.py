from typing import List

from pydantic import BaseModel

from schemas.wells_use_accessories import WellUseAccessorySchema
from model.well import Well


class WellSchema(BaseModel):
    """ Define como um novo poço a ser inserido deve ser representado
    """
    name: str = "7-RO-203H-RJS"

class AccessoryInWellSchema(BaseModel):
    """ Define como um acessório deve ser representado dentro de um poço.
    """
    accessory_id: int
    name: str
    manufacturer: str
    relationship: WellUseAccessorySchema

class WellWithAccessoriesSchema(BaseModel):
    """ Define como um novo poço e seus acessórios devem ser representados
    """
    name: str = "7-RO-203H-RJS"
    accessories: list[AccessoryInWellSchema] = []

class WellListSchema(BaseModel):
    """ Define como uma lista de poços deve ser representada
    """
    wells: List[WellSchema] = []

def show_wells(wells: List[Well]):
    """ Retorna uma representação do poço seguindo o schema definido em
        WellListSchema.
    """
    result = []
    for well in wells:
        well_data = {
            "name": well.name,
        }
        result.append(well_data)

    return {"wells": result}

def show_well(well: Well):
    """ Retorna uma representação do poço seguindo o schema definido em
        WellWithAccessoriesSchema.
    """
    well_data = {
        "name": well.name,
        "accessories":[{"name": link.accessory.name, 
                  "anomaly": link.anomaly, 
                  "comment": link.comment} for link in well.accessories],
    }
    return well_data