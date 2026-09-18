from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Accessory(Base):
    __tablename__ = 'accessory'

    material_number = Column("pk_accessory", Integer, primary_key=True)
    accessory_type = Column(String(50), nullable=False)
    name = Column(String(140), unique=True, nullable=False)
    manufacturer = Column(String(140), nullable=False)
    outer_diameter = Column(Float, nullable=False)
    casing_size = Column(Float, nullable=False)
    external_use_cases = Column(String(4000))
    registration_date = Column(DateTime, default=datetime.now())
    last_update_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    users = relationship("User", secondary="users_analyze_accessories", back_populates="accessories")
    wells = relationship("Well", secondary="wells_use_accessories", back_populates="accessories")
    __mapper_args__ = {
        "polymorphic_on": accessory_type,
        "polymorphic_identity": "accessory",
    }

    def __init__(self, name:str, manufacturer:str, outer_diameter:float, casing_size:float, external_use_cases:str = None, registration_date:Union[DateTime, None] = None):
        """
        Cria um Acessório

        Arguments:
            name: nome do acessório.
            manufacturer: fabricante do acessório.
            outer_diameter: diâmetro externo do acessório.
            casing_size: tamanho do revestimento do acessório.
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

