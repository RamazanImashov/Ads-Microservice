
from typing import Sequence, Optional

from fastapi import HTTPException, Header, Request

from ..grpc_clients.grpc_client import get_user, verify_token

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .model import AdvertisementModel

from .schema import AdvertisementSchema, CreateAdvertisementSchema, GetAdvertisementSchema


async def get_all_advertisements(
        session: AsyncSession
) -> Sequence[AdvertisementModel]:
    stmt = select(AdvertisementModel).order_by(AdvertisementModel.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_id_advertisement(
        ads_id: int,
        session: AsyncSession
) -> Sequence[AdvertisementModel]:
    stmt = select(AdvertisementModel).where(AdvertisementModel.id == ads_id)
    result = await session.scalars(stmt)
    return result.first()


async def create_advertisements(
        request: Request,
        session: AsyncSession,
        advertisement_create: CreateAdvertisementSchema,
) -> AdvertisementModel:
    # Получаем заголовок Authorization
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing")

    try:
        # Предполагаем формат "Bearer <token>"
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    # Проверяем токен через gRPC и получаем данные пользователя
    user_data = verify_token(token=token)
    if not user_data or not user_data.is_valid:
        raise HTTPException(status_code=403, detail="User not authorized or Token invalid")

    # Используем user_id из токена
    user_id = user_data.id
    user = get_user(user_id)
    if not user.is_valid:
        raise HTTPException(status_code=400, detail="Invalid user")

    user_id = user.id

    # Создаем рекламу, добавляя user_id к данным из запроса
    advertisement = AdvertisementModel(
        **advertisement_create.model_dump(),
        user_id=user_id,
    )
    session.add(advertisement)
    await session.commit()
    await session.refresh(advertisement)
    return advertisement


# async def create_advertisements(
#         session: AsyncSession,
#         advertisement_create: AdvertisementSchema,
#         authorization: str = Header(...),
# ) -> AdvertisementModel:
#     token = authorization.split(" ")[1]
#     user_data = verify_token(token=token)
#     if not user_data:
#         raise HTTPException(status_code=403, detail="User not authorized or Token invalid")
#     user = get_user(advertisement_create.user_id)
#     if not user.is_valid:
#         raise HTTPException(status_code=400, detail="Invalid user")
#     advertisement = AdvertisementModel(**advertisement_create.model_dump())
#     session.add(advertisement)
#     await session.commit()
#     return advertisement


