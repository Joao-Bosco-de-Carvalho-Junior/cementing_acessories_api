from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Table
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

association_table = Table(
    "wells_use_accessories",
    Base.metadata,
    Column("well_id", ForeignKey("well.id"), primary_key=True),
    Column("accessory_id", ForeignKey("accessory.pk_accessory"), primary_key=True),
    Column("comment", String(4000)),
    Column("anomaly", Boolean, default=True),
)
