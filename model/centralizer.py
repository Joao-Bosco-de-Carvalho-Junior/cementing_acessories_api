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
    well_id = Column(Float, nullable=False)
    type = Column(String(140), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "Centralizador",
    }

    def __init__(
        self,
        name: str,
        manufacturer: str,
        outer_diameter: float,
        casing_size: float,
        restoring_force: float,
        running_force: float,
        type: str,
        external_use_cases: str = None,
        well_id: float,
    ):
        super().__init__(
            name=name,
            manufacturer=manufacturer,
            outer_diameter=outer_diameter,
            casing_size=casing_size,
            external_use_cases=external_use_cases,
        )
        self.restoring_force = restoring_force
        self.running_force = running_force
        self.type = type
        self.well_id = well_id
