
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Request

from .schema import AdvertisementSchema, CreateAdvertisementSchema, GetAdvertisementSchema

from .model import AdvertisementModel

from sqlalchemy.ext.asyncio import AsyncSession

from src.helper import db_helper

from .crud import get_all_advertisements, create_advertisements, get_id_advertisement

router = APIRouter(
    prefix="/ad",
    tags=["Ad"]
)


@router.get("/ads/", response_model=GetAdvertisementSchema)
async def get_ads(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    ads = await get_all_advertisements(session=session)
    return ads


@router.get("/ads/{ads_id}/", response_model=GetAdvertisementSchema)
async def get_ads_id(
        ads_id: int,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ]
):
    ads = await get_id_advertisement(ads_id=ads_id, session=session)
    return ads


@router.post("/ads/")
async def create_ads(
        request: Request,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        advertisement_create: CreateAdvertisementSchema
):
    ads = await create_advertisements(
        request=request,
        session=session,
        advertisement_create=advertisement_create
    )
    return {"message": "Advertisement created successfully", "ad": ads}

