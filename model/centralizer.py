from sqlalchemy import Column, String, Float, ForeignKey
from  model.accessory import Accessory


class Centralizer(Accessory):
    """
    Classe que representa um centralizador, que é um tipo de acessório.
    """
    __tablename__ = 'centralizer'

    # chave primária do centralizador, que é o número de material do acessório
    # que é uma chave estrangeira para a tabela accessory
    # ou seja, adequado ao projeto conceitual de herança (as-is-a) do
    # modelo relacional, onde o centralizador é um acessório
    id = Column(
        ForeignKey("accessory.pk_accessory"),
        primary_key=True,
    )
    restoring_force = Column(Float)
    running_force = Column(Float)
    well_id = Column(Float, nullable=False)
    type = Column(String(140), nullable=False)
    # aqui definimos o tipo de acessório (polimorfismo) como "centralizer", 
    # que é usado pelo SQLAlchemy para instanciar a classe correta
    __mapper_args__ = {
        "polymorphic_identity": "centralizer",
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
        well_id: float,
        external_use_cases: str
    ):
        """
        Cria um Centralizador

        Arguments:
            name: nome do centralizador.
            manufacturer: fabricante do centralizador.
            outer_diameter: diâmetro externo do centralizador.
            casing_size: tamanho do revestimento associado ao centralizador.
            restoring_force: força de restauração do centralizador.
            running_force: força de descida do centralizador.
            type: tipo do centralizador.
            well_id: ID do poço associado ao centralizador.
            external_use_cases: casos de uso externos do centralizador.

        """
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
