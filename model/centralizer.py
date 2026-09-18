from sqlalchemy import Column, String, Float, ForeignKey
from  model.accessory import Accessory


class Centralizer(Accessory):
    __tablename__ = 'centralizer'

    material_number = Column(
        ForeignKey("accessory.pk_accessory"),
        primary_key=True,
    )
    restoring_force = Column(Float)
    running_force = Column(Float)
    type = Column(String(140), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "centralizer",
    }

    def __init__(self, restoring_force:float, running_force:float, type:str):
        """
        Cria um Centralizer

        Arguments:
            restoring_force: a força de restauração do centralizador.
            running_force: a força de descida do centralizador.
            type: o tipo do centralizador.
        """
        self.restoring_force = restoring_force
        self.running_force = running_force
        self.type = type
