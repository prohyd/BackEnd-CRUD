from pydantic import BaseModel,ValidationError,field_validator,Field,ConfigDict
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from loguru import logger

Base = declarative_base()

class Movies(Base):
    __tablename__ = 'movies'

    id_movie = Column(Integer,primary_key=True)
    name_movie = Column(String(50),nullable=False)
    rating = Column(Numeric(5,2),nullable=False)
    description = Column(String(300),nullable=False)

class MoviesForAPI(BaseModel):
    name_movie:str = Field(max_length=50)
    rating:float = Field(ge = 0, le = 100)
    description:str = Field(max_length=300)

class MoviesForAPICreate(MoviesForAPI):
    pass

class MoviesForAPIResponse(MoviesForAPI):
    id_movie: int
    model_config = ConfigDict(from_atribute=True)