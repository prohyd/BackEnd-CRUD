from pydantic import BaseModel,ValidationError,field_validator,Field,ConfigDict
from loguru import logger

class MoviesForAPI(BaseModel):
    name_movie:str = Field(max_length=50)
    rating:float = Field(ge = 0, le = 100)
    description:str = Field(max_length=300)

class MoviesForAPICreate(MoviesForAPI):
    pass

class MoviesForAPIResponse(MoviesForAPI):
    id_movie: int
    model_config = ConfigDict(from_atribute=True)
