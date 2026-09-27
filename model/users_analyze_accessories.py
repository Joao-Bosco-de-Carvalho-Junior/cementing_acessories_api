from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from model.base import Base
from datetime import datetime

# tabela de associação entre usuários e acessórios, 
# que é uma relação muitos-para-muitos
# esta tabela é necessária para poder armazenar informações adicionais
# sobre a relação, como comentários e aprovação, que não são propriamente 
# atributos do usuário ou do acessório, mas sim da relação entre eles.
# user_id é anulável (com ON DELETE SET NULL) para que
# a análise seja preservada mesmo depois que o usuário
# associado a ela seja removido.
# Se usuário removido, desejo que outros usuários ainda possam ver a análise.
# Se acessório removido, a análise será removida em cascata devido ao ON DELETE CASCADE.
# Não faz sentido manter a análise se o acessório não existir mais.

association_table = Table(
    "users_analyze_accessories",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
    Column("accessory_id", ForeignKey("accessory.pk_accessory", ondelete="CASCADE")),
    Column("comment", String(4000)),
    Column("approval", Boolean, default=True),
    Column("approval_date", DateTime, default=datetime.now)
)


class UserAnalyzeAccessory(Base):
    """
    Objeto de associação mapeado sobre a tabela users_analyze_accessories,
    usado para acessar o usuário/acessório junto com o comentário e a
    aprovação registrados na relação entre eles.
    """
    __table__ = association_table

    user = relationship("User", back_populates="accessories")
    accessory = relationship("Accessory", back_populates="users")
