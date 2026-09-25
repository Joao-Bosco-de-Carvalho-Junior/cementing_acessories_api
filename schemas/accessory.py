# arquivo responsável por unificar os schemas de acessórios específicos
# (como centralizadores, sapatas, etc.) e definir os schemas
# de acessórios genéricos, que são utilizados em endpoints que não
# precisam de informações específicas de cada tipo de acessório.

from typing import List

from model.accessory import Accessory
from model.centralizer import Centralizer
from schemas.centralizer import (
    CentralizerDelSchema,
    CentralizerSchema,
    CentralizerSearchSchema,
    CentralizerListSchema,
    CentralizerUpdateSchema,
    CentralizerViewSchema,
    update_centralizer,
    show_centralizer,
)

AccessoryCreateSchema = CentralizerSchema

# quando houver mais tipos de acessórios, será necessário criar um Union de schemas

#AccessoryCreate = Annotated[
#    Union[CentralizerCreateSchema, ShoeCreateSchema],
#    Field(discriminator="accessory_type"),
#]
AccessoryUpdateSchema = CentralizerUpdateSchema
AccessorySearchSchema = CentralizerSearchSchema
AccessoryListSchema = CentralizerListSchema
AccessoryViewSchema = CentralizerViewSchema
AccessoryDelSchema = CentralizerDelSchema

def show_accessories(accessories: List[Accessory]):
    """ Retorna uma representação do acessório seguindo o schema definido em
        AccessoryBaseListSchema + List do acessório específico.
    """
    result = []
    for accessory in accessories:
        accessory_data = {
            "id": accessory.id,
            "accessory_type": accessory.accessory_type,
            "name": accessory.name,
            "manufacturer": accessory.manufacturer,
            "casing_size": accessory.casing_size,
            "last_update_date": accessory.last_update_date,
        }
        # aqui identificamos o tipo de acessório e chamamos a função
        # específica para adicionar os campos específicos do tipo de acessório
        # depois, refatorar para chamar função em dicionário de funções,
        # para não precisar ficar adicionando elifs
        if isinstance(accessory, Centralizer):
            update_centralizer(accessory, accessory_data)
        result.append(accessory_data)

    return {"accessories": result}

def show_accessory(accessory: Accessory):
    """ Retorna uma representação do acessório seguindo o schema definido em
        AccessoryBaseViewSchema + View do acessório específico.
    """

    result = {
        "id": accessory.id,
        "accessory_type": accessory.accessory_type,
        "name": accessory.name,
        "manufacturer": accessory.manufacturer,
        "outer_diameter": accessory.outer_diameter,
        "casing_size": accessory.casing_size,
        "external_use_cases": accessory.external_use_cases,
        "registration_date": accessory.registration_date,
        "last_update_date": accessory.last_update_date,
        # aqui estamos retornando os usuários e poços associados ao
        # acessório, com seus respectivos relacionamentos
        "users":[{"name": link.user.name if link.user else None, 
                  "approval": link.approval, 
                  "comment": link.comment} for link in accessory.users],
        "wells":[{"name": link.well.name if link.well else None, 
                  "anomaly": link.anomaly, 
                  "comment": link.comment} for link in accessory.wells]
    }
    # aqui identificamos o tipo de acessório e chamamos a função
    # específica para adicionar os campos específicos do tipo de acessório
    # depois, refatorar para chamar função em dicionário de funções,
    # para não precisar ficar adicionando elifs
    if isinstance(accessory, Centralizer):
        result.update(show_centralizer(accessory))

    return result

