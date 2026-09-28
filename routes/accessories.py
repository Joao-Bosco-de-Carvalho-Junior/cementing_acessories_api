from flask_openapi3 import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import Accessory, Centralizer, Session
from schemas.accessory import (
    AccessoryCreateSchema,
    AccessoryDelSchema,
    AccessoryListSchema,
    AccessorySearchSchema,
    AccessoryUpdateSchema,
    AccessoryViewSchema,
    show_accessories,
    show_accessory,
)
from schemas.error import ErrorSchema


accessory_tag = Tag(
    name="Acessório",
    description="Adição, atualização, visualização e remoção de acessórios à base",
)

api = APIBlueprint("accessories", __name__, abp_tags=[accessory_tag])

# dicionário de mapeamento de tipos de acessório para suas classes correspondentes
ACCESSORY_MODELS = {
    "centralizer": Centralizer,
    #"shoe": Shoe,
}


@api.post(
    "/accessory",
    responses={"200": AccessoryViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_accessory(form: AccessoryCreateSchema):
    # obtém a classe do modelo de acessório correspondente ao tipo informado
    model_class = ACCESSORY_MODELS[form.accessory_type]
    #desempacotando os dados do formulário para criar uma instância do modelo de acessório
    accessory = model_class(**form.model_dump(exclude={"accessory_type"}))
    logger.debug(f"Adicionando acessório de nome: '{accessory.name}'")
    session = Session()
    try:
        session.add(accessory)
        session.commit()
        logger.debug(f"Adicionado acessório de nome: '{accessory.name}'")
        return show_accessory(accessory), 200
    except IntegrityError:
        session.rollback()
        error_msg = "Acessório de mesmo Número de Material já salvo na base :/"
        logger.warning(f"Erro ao adicionar acessório '{accessory.name}', {error_msg}")
        return {"message": error_msg}, 409
    except Exception:
        session.rollback()
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar acessório '{accessory.name}', {error_msg}")
        return {"message": error_msg}, 400


@api.patch(
    "/accessory/",
    responses={"200": AccessoryViewSchema, "404": ErrorSchema, "400": ErrorSchema},
)
def update_accessory(form: AccessoryUpdateSchema):
    session = Session()
    accessory = session.query(Accessory).filter(Accessory.id == form.id).first()

    if not accessory:
        error_msg = "Acessório não encontrado na base :/"
        logger.warning(f"Erro ao atualizar acessório #{form.id}, {error_msg}")
        return {"message": error_msg}, 404

    logger.debug(f"Atualizando acessório de nome: '{accessory.name}'")
    try:
        accessory_data = form.model_dump(
            exclude={"id", "accessory_type"},
            exclude_unset=True,
            exclude_none=True,
        )
        for field, value in accessory_data.items():
            setattr(accessory, field, value)
        session.commit()
        logger.debug(f"Atualizado acessório de nome: '{accessory.name}'")
        return show_accessory(accessory), 200
    except Exception:
        session.rollback()
        error_msg = "Não foi possível atualizar o item :/"
        logger.warning(f"Erro ao atualizar acessório '{accessory.name}', {error_msg}")
        return {"message": error_msg}, 400


@api.get(
    "/accessories",
    responses={"200": AccessoryListSchema, "404": ErrorSchema},
)
def get_accessories():
    logger.debug("Coletando acessórios cadastrados na base")
    session = Session()
    accessories = session.query(Accessory).all()

    if not accessories:
        return {"accessories": []}, 200

    logger.debug("%d acessórios encontrados" % len(accessories))
    return show_accessories(accessories), 200


@api.get(
    "/accessory",
    responses={"200": AccessoryViewSchema, "404": ErrorSchema},
)
def get_accessory(query: AccessorySearchSchema):
    accessory_id = query.id
    logger.debug(f"Coletando dados sobre acessório #{accessory_id}")
    session = Session()
    accessory = session.query(Accessory).filter(Accessory.id == accessory_id).first()

    if not accessory:
        error_msg = "Acessório não encontrado na base :/"
        logger.warning(f"Erro ao buscar acessório '{accessory_id}', {error_msg}")
        return {"message": error_msg}, 404

    logger.debug(f"Acessório encontrado: '{accessory.name}'")
    return show_accessory(accessory), 200


@api.delete(
    "/accessory",
    responses={"200": AccessoryDelSchema, "404": ErrorSchema},
)
def del_accessory(query: AccessorySearchSchema):
    accessory_id = query.id
    logger.debug(f"Deletando dados sobre acessório #{accessory_id}")
    session = Session()
    accessory = session.get(Accessory, accessory_id)

    if accessory:
        session.delete(accessory)
        session.commit()
        logger.debug(f"Deletado acessório #{accessory_id}")
        return {"message": "Acessório removido", "id": accessory_id}

    error_msg = "Acessório não encontrado na base :/"
    logger.warning(f"Erro ao deletar acessório #'{accessory_id}', {error_msg}")
    return {"message": error_msg}, 404