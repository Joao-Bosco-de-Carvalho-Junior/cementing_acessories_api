from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), unique=True, nullable=False)
    email = Column(String(140), unique=True, nullable=False)
    password = Column(String(140), nullable=False)
    accessories = relationship("Accessory", secondary="users_analyze_accessories", back_populates="users")
    

    def __init__(self, name:str, email:str, password:str):
        """
        Cria um usuário

        Arguments:
            name: nome do usuário.
            email: email do usuário.
            password: senha do usuário.
        """
        self.name = name
        self.email = email
        self.password = password