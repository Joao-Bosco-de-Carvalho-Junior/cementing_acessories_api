from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table #DateTime
from sqlalchemy.orm import relationship
from model.base import Base
#from datetime import datetime

# tabela de associação entre poços e acessórios, 
# que é uma relação muitos-para-muitos
# esta tabela é necessária para poder armazenar informações adicionais
# sobre a relação, como comentários e anomalia, que não são propriamente 
# atributos do poço ou do acessório, mas sim da relação entre eles.

association_table = Table(
    "wells_use_accessories",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("well_id", ForeignKey("well.id", ondelete="CASCADE")),
    Column("accessory_id", ForeignKey("accessory.pk_accessory", ondelete="CASCADE")),
    Column("comment", String(4000)),
    Column("anomaly", Boolean, default=False),
)


class WellUseAccessory(Base):
    """
    Objeto de associação mapeado sobre a tabela wells_use_accessories,
    usado para acessar o poço/acessório junto com o comentário e a
    anomalia registrados na relação entre eles.
    """
    __table__ = association_table

    well = relationship("Well", back_populates="accessories")
    accessory = relationship("Accessory", back_populates="wells")
