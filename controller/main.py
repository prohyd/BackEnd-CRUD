from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from model.models_for_cinema import MoviesForAPICreate, MoviesForAPIResponse
from repository.create_connection_to_bd import get_bd
from repository.worker import create_movie, get_movie, get_cursor_movie, delete_movie, update_movie
from controller.config_log import setup_logging
from loguru import logger
import uvicorn

setup_logging()

app = FastAPI()


@app.get("/cinema/{movie_id}", response_model=MoviesForAPIResponse)
def getCinema(movie_id: int, db: Session = Depends(get_bd)):
    logger.info("GET /cinema/{} запрос получен", movie_id)

    cinema = get_movie(db, movie_id)
    if cinema is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.info("Кинотеатр id={} успешно найден", movie_id)
    return cinema


@app.get("/cinema/", response_model=list[MoviesForAPIResponse])
def getCursor(skip: int = 0, limit: int = 20, db: Session = Depends(get_bd)):
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

    logger.success("Кинотеатр успешно создан: id={}", cinema.id_movie)
    return cinema


@app.put("/cinema/{movie_id}", response_model=MoviesForAPIResponse)
def UpdateCinema(movie_id: int, columns: str, new_value: str, db: Session = Depends(get_bd)):
    logger.info(
        "PUT /cinema/{} обновление: поле={}, новое значение={}",
        movie_id,
        columns,
        new_value
    )

    updated = update_movie(db, movie_id, columns, new_value)
    if updated is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    if updated is False:
        raise HTTPException(status_code=400, detail="Invalid column for update")

    logger.success("Кинотеатр id={} успешно обновлён", movie_id)
    return updated


@app.delete("/cinema/{movie_id}")
def DeleteCinema(movie_id: int, db: Session = Depends(get_bd)):
    logger.info("DELETE /cinema/{} удаление", movie_id)

    deleted = delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.success("Кинотеатр id={} успешно удалён", movie_id)
    return {"status": "deleted", "cinema_id": movie_id}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
