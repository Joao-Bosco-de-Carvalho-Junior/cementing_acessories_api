from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from  model import Base

class Well(Base):
    """
    Classe que representa um poço do sistema.
    """
    __tablename__ = 'well'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), unique=True, nullable=False)
    # relacionamento com o objeto de associação wells_use_accessories, que
    # expõe o acessório junto com o comentário e a anomalia da relação
    accessories = relationship(
        "WellUseAccessory",
        back_populates="well",
        passive_deletes=True,
    )

    def __init__(self, name:str):
        """
        Cria um poço

        Arguments:
            name: nome do poço.
        """
        self.name = name