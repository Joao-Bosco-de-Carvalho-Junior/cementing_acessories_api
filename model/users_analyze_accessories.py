from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Table
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

association_table = Table(
    "users_analyze_accessories",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("accessory_id", ForeignKey("accessory.pk_accessory"), primary_key=True),
    Column("comment", String(4000)),
    Column("approval", Boolean, default=True),
    Column("approval_date", DateTime, default=datetime.now())
)
