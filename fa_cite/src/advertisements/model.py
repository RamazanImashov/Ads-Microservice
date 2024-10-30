from uuid import uuid4
from sqlalchemy import UniqueConstraint
from sqlalchemy import Integer, String, Float, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from src.helper.database import Base
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


class AdvertisementModel(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # foo: Mapped[int]
    # bar: Mapped[int]
    #
    # __table_args__ = (
    #     UniqueConstraint("foo", "bar"),
    # )

    # @classmethod
    # async def create(cls, db: AsyncSession, id=None, **kwargs):
    #     if not id:
    #         id = uuid4().hex
    #
    #     transaction = cls(id=id, **kwargs)
    #     db.add(transaction)
    #     await db.commit()
    #     await db.refresh(transaction)
    #     return transaction
    #
    # @classmethod
    # async def get(cls, db: AsyncSession, id: str):
    #     try:
    #         transaction = await db.get(cls, id)
    #     except NoResultFound:
    #         return None
    #     return transaction
    #
    # @classmethod
    # async def get_all(cls, db: AsyncSession):
    #     return (await db.execute(select(cls))).scalars().all()
