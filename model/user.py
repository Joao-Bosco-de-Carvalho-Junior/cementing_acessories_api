from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base

class User(Base):
    """
    Classe que representa um usuário do sistema.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), unique=True, nullable=False)
    # implementar user authentication com email e senha
    #email = Column(String(140), unique=True, nullable=False)
    #password = Column(String(140), nullable=False)
    # relacionamento com o objeto de associação users_analyze_accessories, que
    # expõe o acessório junto com o comentário e a aprovação da relação
    accessories = relationship("UserAnalyzeAccessory", back_populates="user")
    

    def __init__(self, 
                 name:str, 
                 #email:str, 
                 #password:str
                 ):
        """
        Cria um usuário

        Arguments:
            name: nome do usuário.
        """
        self.name = name
        #self.email = email
        #self.password = password