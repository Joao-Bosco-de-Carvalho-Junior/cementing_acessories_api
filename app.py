from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info 
from flask_openapi3.models.tag import Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import (
    Session,
    Accessory,
    Centralizer,
    User,
    Well,
    wells_use_accessories as wells_use_accessories_table,
    users_analyze_accessories as users_analyze_accessories_table,
)
from logger import logger
from schemas import *
from flask_cors import CORS

from schemas.accessory import show_accessories, show_accessory
from schemas.well import show_wells, show_well
from schemas.wells_use_accessories import WellUseAccessoryCreateSchema
from schemas.users_analyze_acessories import UserAnalyzeAccessoryCreateSchema
from schemas.user import show_users, show_user

info = Info(title="Cementing Accessories API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# dicionário de mapeamento de tipos de acessório para suas classes correspondentes
ACCESSORY_MODELS = {
    "centralizer": Centralizer,
    #"shoe": Shoe,
}

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
accessory_tag = Tag(name="Acessório", description="Adição, visualização e remoção de acessórios à base")
centralizer_tag = Tag(name="Centralizador", description="Adição, visualização e remoção de centralizadores à base")
user_tag = Tag(name="Usuário", description="Adição, visualização e remoção de usuários à base")
well_tag = Tag(name="Poço", description="Adição, visualização e remoção de poços à base")

@app.get('/', tags=[home_tag])
def home():
    """ Redireciona à documentação API (no caso, apenas Swagger no momento)
    """
    return redirect('/openapi/swagger')


@app.post('/acessory', tags=[accessory_tag],
          responses={"200": AccessoryViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_accessory(form: AccessoryCreateSchema):
    """Adiciona um novo Acessório à base de dados
    """

    # obtém a classe do modelo de acessório correspondente ao tipo informado
    model_class = ACCESSORY_MODELS[form.accessory_type]

    #desempacotando os dados do formulário para criar uma instância do modelo de acessório
    accessory = model_class(**form.model_dump(exclude={"accessory_type"}))
    logger.debug(f"Adicionando acessório de nome: '{accessory.name}'")
    # criando conexão com a base
    session = Session()
    try:
        # adicionando acessório
        session.add(accessory)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado acessório de nome: '{accessory.name}'")
        return show_accessory(accessory), 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Acessório de mesmo Número de Material já salvo na base :/"
        logger.warning(f"Erro ao adicionar acessório '{accessory.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar acessório '{accessory.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.patch('/accessory/', tags=[accessory_tag],
           responses={"200": AccessoryViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_accessory(form: AccessoryUpdateSchema):
    """Atualiza um Acessório à base de dados
    """
    # criando conexão com a base
    session = Session()
    accessory = session.query(Accessory).filter(Accessory.material_number == form.material_number).first()

    if not accessory:
        error_msg = "Acessório não encontrado na base :/"
        logger.warning(f"Erro ao atualizar acessório #{form.material_number}, {error_msg}")
        return {"message": error_msg}, 404

    logger.debug(f"Atualizando acessório de nome: '{accessory.name}'")
    try:
        # atualizando acessório
        accessory_data = form.model_dump(
            exclude={"material_number", "accessory_type"},
            exclude_unset=True,
            exclude_none=True,
        )
        for field, value in accessory_data.items():
            setattr(accessory, field, value)

        # efetivando o camando de atualização do item na tabela
        session.commit()
        logger.debug(f"Atualizado acessório de nome: '{accessory.name}'")
        return show_accessory(accessory), 200

    except Exception as e:
        session.rollback()
        # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar o item :/"
        logger.warning(f"Erro ao atualizar acessório '{accessory.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/accessories', tags=[accessory_tag],
         responses={"200": AccessoryListSchema, "404": ErrorSchema})
def get_accessories():
    """Faz a busca por todos os Acessório cadastrados

    Retorna uma representação da listagem de acessórios.
    """
    logger.debug(f"Coletando acessórios cadastrados na base")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    # Poder separar por tipo?
    accessories = session.query(Accessory).all()

    if not accessories:
        # se não há acessórios cadastrados
        return {"accessories": []}, 200
    else:
        logger.debug(f"%d acessórios encontrados" % len(accessories))
        # retorna a representação de acessório
        print(accessories)
        return show_accessories(accessories), 200


@app.get('/accessory', tags=[accessory_tag],
         responses={"200": AccessoryViewSchema, "404": ErrorSchema})
def get_accessory(query: AccessorySearchSchema):
    """Faz a busca por um Acessório a partir do id do acessório

    Retorna uma representação dos acessórios e comentários associados.
    """
    acessory_material_number = query.material_number
    logger.debug(f"Coletando dados sobre acessório #{acessory_material_number}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    acessory = session.query(Accessory).filter(Accessory.material_number == acessory_material_number).first()

    if not acessory:
        # se o acessório não foi encontrado
        error_msg = "Acessório não encontrado na base :/"
        logger.warning(f"Erro ao buscar acessório '{acessory_material_number}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Acessório encontrado: '{acessory.name}'")
        # retorna a representação de acessório
        return show_accessory(acessory), 200


@app.delete('/accessory', tags=[accessory_tag],
            responses={"200": AccessoryDelSchema, "404": ErrorSchema})
def del_accessory(query: AccessorySearchSchema):
    """Deleta um Acessório a partir do id de acessório informado

    Retorna uma mensagem de confirmação da remoção.
    """
    acessory_material_number = query.material_number
    print(acessory_material_number)
    logger.debug(f"Deletando dados sobre acessório #{acessory_material_number}")
    # criando conexão com a base
    session = Session()
    # Carrega a instância para que o SQLAlchemy remova também a subclasse.
    accessory = session.get(Accessory, acessory_material_number)

    if accessory:
        session.delete(accessory)
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado acessório #{acessory_material_number}")
        return {"message": "Acessório removido", "id": acessory_material_number}
    else:
        # se o acessório não foi encontrado
        error_msg = "Acessório não encontrado na base :/"
        logger.warning(f"Erro ao deletar acessório #'{acessory_material_number}', {error_msg}")
        return {"message": error_msg}, 404

@app.post('/well', tags=[well_tag],
             responses={"200": WellSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_well(form: WellSchema):
    """Adiciona um novo Poço à base de dados
    """
    well = Well(**form.model_dump())
    logger.debug(f"Adicionando poço de nome: '{well.name}'")
    # criando conexão com a base
    session = Session()
    try:
        # adicionando poço
        session.add(well)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado poço de nome: '{well.name}'")
        return {"name": well.name}, 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Poço de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar poço '{well.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar poço '{well.name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/wells', tags=[well_tag],
         responses={"200": WellListSchema, "404": ErrorSchema})
def get_wells():
    """Faz a busca por todos os Poços cadastrados

    Retorna uma representação da listagem de poços.
    """
    logger.debug(f"Coletando poços cadastrados na base")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    # Poder separar por tipo?
    wells = session.query(Well).all()

    if not wells:
        # se não há poços cadastrados
        return {"wells": []}, 200
    else:
        logger.debug(f"%d poços encontrados" % len(wells))
        # retorna a representação de poço
        print(wells)
        return show_wells(wells), 200


@app.get('/well', tags=[well_tag],
         responses={"200": WellWithAccessoriesSchema, "404": ErrorSchema})
def get_well(query: WellSchema):
    """Faz a busca por um Poço a partir do nome do poço

    Retorna uma representação do poço e seus acessórios associados.
    """
    well_name = query.name
    logger.debug(f"Coletando dados sobre poço '{well_name}'")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    well = session.query(Well).filter(Well.name == well_name).first()

    if not well:
        # se o poço não foi encontrado
        error_msg = "Poço não encontrado na base :/"
        logger.warning(f"Erro ao buscar poço '{well_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Poço encontrado: '{well.name}'")
        # retorna a representação do poço
        return show_well(well), 200


@app.delete('/well', tags=[well_tag],
            responses={"200": WellSchema, "404": ErrorSchema})
def del_well(query: WellSchema):
    """Deleta um Poço a partir do nome do poço informado

    Retorna uma mensagem de confirmação da remoção.
    """
    well_name = query.name
    logger.debug(f"Deletando dados sobre poço '{well_name}'")
    # criando conexão com a base
    session = Session()
    # Carrega a instância.
    well = session.query(Well).filter(Well.name == well_name).first()

    if well:
        session.delete(well)
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado poço '{well_name}'")
        return {"message": "Poço removido", "name": well_name}
    else:
        # se o poço não foi encontrado
        error_msg = "Poço não encontrado na base :/"
        logger.warning(f"Erro ao deletar poço '{well_name}', {error_msg}")
        return {"message": error_msg}, 404

@app.post('/well/accessory', tags=[well_tag],
          responses={"201": WellUseAccessoryCreateSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_accessory_to_well(form: WellUseAccessoryCreateSchema):
    """Associa um acessório a um poço, registrando comentário e anomalia."""
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
            accessory_id=accessory.material_number,
            comment=form.comment,
            anomaly=form.anomaly,
        )
        session.execute(association)
        session.commit()
        return {
            "well_name": well.name,
            "accessory_id": accessory.material_number,
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

@app.post('/user', tags=[user_tag],
          responses={"200": UserSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Adiciona um novo usuário à base de dados."""
    user = User(name=form.name)
    session = Session()
    try:
        session.add(user)
        session.commit()
        return {"name": user.name}, 200
    except IntegrityError:
        session.rollback()
        return {"message": "Usuário de mesmo nome já salvo na base :/"}, 409
    except Exception:
        session.rollback()
        return {"message": "Não foi possível salvar novo usuário :/"}, 400


@app.patch('/user', tags=[user_tag],
           responses={"200": UserWithAccessoriesSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_user(form: UserUpdateSchema):
    """Atualiza o nome de um usuário."""
    session = Session()
    user = session.query(User).filter_by(name=form.current_name).first()

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


@app.get('/users', tags=[user_tag],
         responses={"200": UserListSchema})
def get_users():
    """Retorna todos os usuários cadastrados."""
    session = Session()
    return show_users(session.query(User).all()), 200


@app.get('/user', tags=[user_tag],
         responses={"200": UserWithAccessoriesSchema, "404": ErrorSchema})
def get_user(query: UserSearchSchema):
    """Retorna um usuário pelo nome."""
    session = Session()
    user = session.query(User).filter_by(name=query.name).first()

    if not user:
        return {"message": "Usuário não encontrado na base :/"}, 404
    return show_user(user), 200


@app.delete('/user', tags=[user_tag],
            responses={"200": UserDelSchema, "404": ErrorSchema})
def del_user(query: UserSearchSchema):
    """Remove um usuário pelo nome."""
    session = Session()
    user = session.query(User).filter_by(name=query.name).first()

    if not user:
        return {"message": "Usuário não encontrado na base :/"}, 404

    session.delete(user)
    session.commit()
    return {"message": "Usuário removido", "name": query.name}, 200

@app.post('/user/accessory', tags=[user_tag],
          responses={"201": UserAnalyzeAccessoryCreateSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def user_analyze_accessory(form: UserAnalyzeAccessoryCreateSchema):
    """Registra análise de acessório, registrando se foi aprovado, comentários e data.
    """
    session = Session()
    user = session.query(User).filter_by(name=form.user_name).first()
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
            accessory_id=accessory.material_number,
            comment=form.comment,
            approval=form.approval,
        )
        session.execute(association)
        session.commit()
        return {
            "user_name": user.name,
            "accessory_id": accessory.material_number,
            "comment": form.comment,
            "approval": form.approval,
        }, 201

    except IntegrityError:
        session.rollback()
        return {"message": "Acessório já foi analizado por esta pessoa :/"}, 409

    except Exception:
        session.rollback()
        return {"message": "Não foi possível registrar análise do acessório :/"}, 400