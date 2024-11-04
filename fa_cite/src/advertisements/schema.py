from pydantic import BaseModel, ConfigDict


class GetAdvertisementSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class AdvertisementSchema(BaseModel):
    title: str
    description: str
    price: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class CreateAdvertisementSchema(BaseModel):
    title: str
    description: str
    price: float

    model_config = ConfigDict(from_attributes=True)
