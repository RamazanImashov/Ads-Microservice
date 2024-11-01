from pydantic import BaseModel


class GetAdvertisementSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    user_id: int


class AdvertisementSchema(BaseModel):
    title: str
    description: str
    price: float
    user_id: int


class CreateAdvertisementSchema(BaseModel):
    title: str
    description: str
    price: float
