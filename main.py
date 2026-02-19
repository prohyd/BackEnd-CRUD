from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from DB.models import MoviesForAPICreate,MoviesForAPIResponse
from DB.EnginePostgresql import get_bd
from DB.worker import create_movie,get_movie,get_cursor_movie,delete_movie,update_movie
from configFile.config_log import setup_logging
from loguru import logger
import uvicorn
setup_logging()

app = FastAPI()



@app.get("/cinema/{cinema_id}", response_model=MoviesForAPIResponse)
def getCinema(movie_id_input: int, db: Session = Depends(get_bd)):
    logger.info("GET /cinema/{} запрос получен", movie_id_input)

    cinema = get_movie(db, movie_id_input)

    logger.info("Кинотеатр id={} успешно найден", movie_id_input)
    return cinema


@app.get("/cinema/", response_model=list[MoviesForAPIResponse])
def getCursor(skip: int, limit: int, db: Session = Depends(get_bd)):
    logger.info("GET /cinema/ запрос: skip={}, limit={}", skip, limit)

    movies = get_cursor_movie(db, skip, limit)

    logger.info("Найдено {} кинотеатров", len(movies))
    return movies


@app.post("/cinema/", response_model=MoviesForAPIResponse)
def CreateCinema(movie_create: MoviesForAPICreate, db: Session = Depends(get_bd)):
    logger.info(
        "POST /cinema/ создание кинотеатра: name={}, rating={}",
        movie_create.name_movie,
        movie_create.rating
    )

    cinema = create_movie(
        db,
        movie_create.name_movie,
        movie_create.rating,
        movie_create.description
    )

    logger.success("Кинотеатр успешно создан: id={}", cinema.idcinema)
    return cinema


@app.put("/cinema/{cinema_id}", response_model=MoviesForAPIResponse)
def UpdateCinema(movie_id_input: int, columns: str, new_value, db: Session = Depends(get_bd)):
    logger.info(
        "PUT /cinema/{} обновление: поле={}, новое значение={}",
        movie_id_input,
        columns,
        new_value
    )

    updated = update_movie(db, movie_id_input, columns, new_value)

    logger.success("Кинотеатр id={} успешно обновлён", movie_id_input)
    return updated


@app.delete("/cinema/{cinema_id}")
def DeleteCinema(movie_id_input: int, db: Session = Depends(get_bd)):
    logger.info("DELETE /cinema/{} удаление", movie_id_input)

    deleted = delete_movie(db, movie_id_input)

    logger.success("Кинотеатр id={} успешно удалён", movie_id_input)
    return {"status": "deleted", "cinema_id": movie_id_input}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)