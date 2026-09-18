from sqlalchemy import Column, String, Integer

from  model import Base

class Well(Base):
    __tablename__ = 'well'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), unique=True, nullable=False)
    accessories = relationship("Accessory", secondary="wells_use_accessories", back_populates="wells")

    def __init__(self, name:str):
        """
        Cria um poço

        Arguments:
            name: nome do poço.
        """
        self.name = name