from flask_openapi3 import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import (
    Accessory,
    Session,
    Well,
    wells_use_accessories as wells_use_accessories_table,
)
from schemas.error import ErrorSchema
from schemas.well import (
    WellListSchema,
    WellSchema,
    WellSearchSchema,
    WellWithAccessoriesSchema,
    WellWithIDSchema,
    show_wells,
    show_well,
)
from schemas.wells_use_accessories import WellUseAccessoryCreateSchema

well_tag = Tag(
    name="Poço",
    description="Adição, visualização e remoção de poços à base",
)
api = APIBlueprint("wells", __name__, abp_tags=[well_tag])


@api.post(
    "/well",
    responses={"200": WellWithIDSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_well(form: WellSchema):
    well = Well(**form.model_dump())
    logger.debug(f"Adicionando poço de nome: '{well.name}'")
    session = Session()
    try:
        session.add(well)
        session.commit()
        logger.debug(f"Adicionado poço de nome: '{well.name}'")
        return {"id": well.id, "name": well.name}, 200
    except IntegrityError:
        session.rollback()
        error_msg = "Poço de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar poço '{well.name}', {error_msg}")
        return {"message": error_msg}, 409
    except Exception:
        session.rollback()
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar poço '{well.name}', {error_msg}")
        return {"message": error_msg}, 400


@api.patch(
    "/well",
    responses={
        "200": WellWithAccessoriesSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def update_well(form: WellWithIDSchema):
    session = Session()
    well = session.get(Well, form.id)

    if not well:
        return {"message": "Poço não encontrado na base :/"}, 404

    try:
        well.name = form.name
        session.commit()
        return show_well(well), 200
    except IntegrityError:
        session.rollback()
        return {"message": "Poço de mesmo nome já salvo na base :/"}, 409
    except Exception:
        session.rollback()
        return {"message": "Não foi possível atualizar o poço :/"}, 400


@api.get("/wells", responses={"200": WellListSchema, "404": ErrorSchema})
def get_wells():
    logger.debug("Coletando poços cadastrados na base")
    session = Session()
    wells = session.query(Well).all()

    if not wells:
        return {"wells": []}, 200

    logger.debug("%d poços encontrados" % len(wells))
    return show_wells(wells), 200


@api.get(
    "/well",
    responses={"200": WellWithAccessoriesSchema, "404": ErrorSchema},
)
def get_well(query: WellSearchSchema):
    well_id = query.id
    logger.debug(f"Coletando dados sobre poço '{well_id}'")
    session = Session()
    well = session.query(Well).filter(Well.id == well_id).first()

    if not well:
        error_msg = "Poço não encontrado na base :/"
        logger.warning(f"Erro ao buscar poço '{well_id}', {error_msg}")
        return {"message": error_msg}, 404

    logger.debug(f"Poço encontrado: '{well.id}'")
    return show_well(well), 200


@api.delete("/well", responses={"200": WellSchema, "404": ErrorSchema})
def del_well(query: WellSearchSchema):
    well_id = query.id
    logger.debug(f"Deletando dados sobre poço '{well_id}'")
    session = Session()
    well = session.query(Well).filter(Well.id == well_id).first()

    if well:
        session.delete(well)
        session.commit()
        logger.debug(f"Deletado poço '{well_id}'")
        return {"message": "Poço removido", "id": well_id}

    error_msg = "Poço não encontrado na base :/"
    logger.warning(f"Erro ao deletar poço '{well_id}', {error_msg}")
    return {"message": error_msg}, 404


@api.post(
    "/well/accessory",
    responses={
        "201": WellUseAccessoryCreateSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def add_accessory_to_well(form: WellUseAccessoryCreateSchema):
    session = Session()
    well = session.get(Well, form.well_id)
    accessory = session.get(Accessory, form.accessory_id)

    if not well:
        return {"message": "Poço não encontrado na base :/"}, 404

    if not accessory:
        return {"message": "Acessório não encontrado na base :/"}, 404

    try:
        association = wells_use_accessories_table.insert().values(
            well_id=well.id,
            accessory_id=accessory.id,
            comment=form.comment,
            anomaly=form.anomaly,
        )
        session.execute(association)
        session.commit()
        return {
            "well_id": well.id,
            "accessory_id": accessory.id,
            "comment": form.comment,
            "anomaly": form.anomaly,
        }, 201
    except IntegrityError as error:
        session.rollback()
        logger.warning("Erro de integridade ao associar acessório ao poço: %s", error)
        return {"message": "Acessório já associado a este poço :/"}, 409
    except Exception as error:
        session.rollback()
        logger.exception("Erro ao associar acessório ao poço: %s", error)
        return {"message": "Não foi possível associar o acessório ao poço :/"}, 400