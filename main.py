from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from DB.models import cinemaForAPICreate,cinemaForAPIResponse
from DB.EnginePostgresql import GetBD
from DB.worker import Create,GetCinema,GetCursor,Delete,Update
from configFile.config_log import setup_logging
from loguru import logger
import uvicorn
setup_logging()

app = FastAPI()



@app.get("/cinema/{cinema_id}", response_model=cinemaForAPIResponse)
def getCinema(cinema_id: int, db: Session = Depends(GetBD)):
    logger.info("GET /cinema/{} запрос получен", cinema_id)

    cinema = GetCinema(db, cinema_id)

    logger.info("Кинотеатр id={} успешно найден", cinema_id)
    return cinema


@app.get("/cinema/", response_model=list[cinemaForAPIResponse])
def getCursor(skip: int, limit: int, db: Session = Depends(GetBD)):
    logger.info("GET /cinema/ запрос: skip={}, limit={}", skip, limit)

    cinemas = GetCursor(db, skip, limit)

    logger.info("Найдено {} кинотеатров", len(cinemas))
    return cinemas


@app.post("/cinema/", response_model=cinemaForAPICreate)
def CreateCinema(cinemaCreate: cinemaForAPICreate, db: Session = Depends(GetBD)):
    logger.info(
        "POST /cinema/ создание кинотеатра: name={}, rating={}",
        cinemaCreate.namecinema,
        cinemaCreate.raiting
    )

    cinema = Create(
        db,
        cinemaCreate.namecinema,
        cinemaCreate.raiting,
        cinemaCreate.description
    )

    logger.success("Кинотеатр успешно создан: id={}", cinema.idcinema)
    return cinema


@app.put("/cinema/{cinema_id}", response_model=cinemaForAPIResponse)
def UpdateCinema(cinemaID: int, colums: str, newValue, db: Session = Depends(GetBD)):
    logger.info(
        "PUT /cinema/{} обновление: поле={}, новое значение={}",
        cinemaID,
        colums,
        newValue
    )

    updated = Update(db, cinemaID, colums, newValue)

    logger.success("Кинотеатр id={} успешно обновлён", cinemaID)
    return updated


@app.delete("/cinema/{cinema_id}")
def DeleteCinema(cinemaID: int, db: Session = Depends(GetBD)):
    logger.info("DELETE /cinema/{} удаление", cinemaID)

    deleted = Delete(db, cinemaID)

    logger.success("Кинотеатр id={} успешно удалён", cinemaID)
    return {"status": "deleted", "cinema_id": cinemaID}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)