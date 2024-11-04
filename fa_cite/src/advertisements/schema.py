from pydantic import BaseModel, ConfigDict


class GetAdvertisementSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    user_id: int

    class Config:
        orm_mode = True


class AdvertisementSchema(BaseModel):
    title: str
    description: str
    price: float
    user_id: int

    class Config:
        orm_mode = True


class CreateAdvertisementSchema(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
