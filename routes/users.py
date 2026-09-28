from flask_openapi3 import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import (
    Accessory,
    Session,
    User,
    users_analyze_accessories as users_analyze_accessories_table,
)
from schemas.error import ErrorSchema
from schemas.user import (
    UserDelSchema,
    UserListSchema,
    UserSchema,
    UserSearchSchema,
    UserUpdateSchema,
    UserWithAccessoriesSchema,
    UserWithIDSchema,
    show_users,
    show_user,
)
from schemas.users_analyze_acessories import UserAnalyzeAccessoryCreateSchema

user_tag = Tag(
    name="Usuário",
    description="Adição, visualização e remoção de usuários à base",
)
api = APIBlueprint("users", __name__, abp_tags=[user_tag])


@api.post(
    "/user",
    responses={"200": UserWithIDSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_user(form: UserSchema):
    user = User(name=form.name)
    session = Session()
    try:
        session.add(user)
        session.commit()
        return {"id": user.id, "name": user.name}, 200
    except IntegrityError:
        session.rollback()
        return {"message": "Usuário de mesmo nome já salvo na base :/"}, 409
    except Exception:
        session.rollback()
        return {"message": "Não foi possível salvar novo usuário :/"}, 400


@api.patch(
    "/user",
    responses={
        "200": UserWithAccessoriesSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def update_user(form: UserUpdateSchema):
    session = Session()
    user = session.get(User, form.id)

    if not user:
        return {"message": "Usuário não encontrado na base :/"}, 404

    try:
        user.name = form.name
        session.commit()
        return show_user(user), 200
    except IntegrityError:
        session.rollback()
        return {"message": "Usuário de mesmo nome já salvo na base :/"}, 409
    except Exception:
        session.rollback()
        return {"message": "Não foi possível atualizar o usuário :/"}, 400


@api.get("/users", tags=[user_tag], responses={"200": UserListSchema})
def get_users():
    session = Session()
    return show_users(session.query(User).all()), 200


@api.get(
    "/user",
    responses={"200": UserWithAccessoriesSchema, "404": ErrorSchema},
)
def get_user(query: UserSearchSchema):
    session = Session()
    user = session.query(User).filter_by(id=query.id).first()

    if not user:
        return {"message": "Usuário não encontrado na base :/"}, 404
    return show_user(user), 200


@api.delete("/user", responses={"200": UserDelSchema, "404": ErrorSchema})
def del_user(query: UserSearchSchema):
    session = Session()
    user = session.query(User).filter_by(id=query.id).first()

    if not user:
        return {"message": "Usuário não encontrado na base :/"}, 404

    session.delete(user)
    session.commit()
    return {"message": "Usuário removido", "id": query.id}, 200


@api.post(
    "/user/accessory",
    responses={
        "201": UserAnalyzeAccessoryCreateSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def user_analyze_accessory(form: UserAnalyzeAccessoryCreateSchema):
    session = Session()
    user = session.get(User, form.user_id)
    accessory = session.get(Accessory, form.accessory_id)

    # quando tiver auth/aut, acho que não faz sentido esta verificação,
    # pois usuário deverá estar logado antes.
    if not user:
        return {"message": "Usuário não encontrado na base :/"}, 404

    if not accessory:
        return {"message": "Acessório não encontrado na base :/"}, 404

    try:
        association = users_analyze_accessories_table.insert().values(
            user_id=user.id,
            accessory_id=accessory.id,
            comment=form.comment,
            approval=form.approval,
        )
        session.execute(association)
        session.commit()
        return {
            "user_id": user.id,
            "accessory_id": accessory.id,
            "comment": form.comment,
            "approval": form.approval,
        }, 201
    except IntegrityError:
        session.rollback()
        return {"message": "Acessório já foi analizado por esta pessoa :/"}, 409
    except Exception:
        session.rollback()
        return {"message": "Não foi possível registrar análise do acessório :/"}, 400