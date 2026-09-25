from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Accessory(Base):
    """
    Classe base para os acessórios de cimentação, como centralizadores e sapatas.
    """
    __tablename__ = 'accessory'

    # chave primária do acessório, que é o número de material
    #pré definido no SAP.
    id = Column("pk_accessory", Integer, primary_key=True)
    # tipo do acessório, que pode ser "centralizer", "shoe", etc
    # este campo é usado para o mapeamento polimórfico do SQLAlchemy.
    accessory_type = Column(String(50), nullable=False)
    # o nome não é único, pois podemos ter o mesmo "tipo" mas de
    # fabricantes diferentes
    name = Column(String(140), nullable=False)
    manufacturer = Column(String(140), nullable=False)
    outer_diameter = Column(Float, nullable=False)
    casing_size = Column(Float, nullable=False)
    external_use_cases = Column(String(4000))
    registration_date = Column(DateTime, default=datetime.now)
    # o campo last_update_date é atualizado automaticamente pelo
    # campo onupdate do SQLAlchemy, que é chamado sempre que o objeto é atualizado.
    last_update_date = Column(DateTime, 
                              default=datetime.now, 
                              onupdate=datetime.now)
    # relacionamento com o objeto de associação users_analyze_accessories,
    # que expõe o usuário junto com o comentário e a aprovação da relação
    # (o back_populates é usado para definir o relacionamento inverso na classe User)
    users = relationship("UserAnalyzeAccessory", 
                         back_populates="accessory",
                         passive_deletes=True,
                         )
    # relacionamento com o objeto de associação wells_use_accessories,
    # que expõe o poço junto com o comentário e a anomalia da relação
    # (o back_populates é usado para definir o relacionamento inverso na classe Well)
    wells = relationship(
        "WellUseAccessory",
        back_populates="accessory",
        passive_deletes=True,
    )
    # o campo __mapper_args__ é usado para definir o mapeamento polimórfico do SQLAlchemy
    # que é cadastrado na tabela accessory, e que é usado para instanciar a classe correta
    __mapper_args__ = {
        "polymorphic_on": accessory_type,
        "polymorphic_identity": "accessory",
    }

    def __init__(self, 
                 name:str, 
                 manufacturer:str, 
                 outer_diameter:float, 
                 casing_size:float, 
                 external_use_cases:str, 
                 registration_date:Union[DateTime, None] = None):
        """
        Cria um Acessório

        Arguments:
            name: nome do acessório.
            manufacturer: fabricante do acessório.
            outer_diameter: diâmetro externo do acessório.
            casing_size: tamanho do revestimento associado ao acessório.
            external_use_cases: casos de uso externos do acessório.
            registration_date: data de registro do acessório.

        """
        self.name = name
        self.manufacturer = manufacturer
        self.outer_diameter = outer_diameter
        self.casing_size = casing_size
        self.external_use_cases = external_use_cases
        self.registration_date = registration_date

        # se não for informada, será o data exata da inserção no banco
        if registration_date:
            self.registration_date = registration_date

