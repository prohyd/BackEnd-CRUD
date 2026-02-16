from pydantic import BaseModel,ValidationError,field_validator,Field
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from loguru import logger

Base = declarative_base()

class cinema(Base):
    __tablename__ = 'cinema'

    idcinema = Column(Integer,primary_key=True)
    namecinema = Column(String(50),nullable=False)
    raiting = Column(Numeric(5,2),nullable=False)
    description = Column(String(300),nullable=False)

class cinemaForAPI(BaseModel):
    namecinema:str = Field(max_length=50)
    raiting:float = Field(ge = 0, le = 100)
    description:str = Field(max_length=300)
class cinemaForAPICreate(cinemaForAPI):
    pass
class cinemaForAPIResponse(cinemaForAPI):
    idcinema: int

    class Config:
        from_attributes = True