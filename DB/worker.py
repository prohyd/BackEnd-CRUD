from sqlalchemy import select
from loguru import logger
from DB.models import cinema


def Create(bd, name: str, rait: float, description: str):
    logger.info("Создание кинотеатра: name={}, rating={}", name, rait)

    CinemaAdd = cinema(
        namecinema=name,
        raiting=rait,
        description=description
    )

    bd.add(CinemaAdd)
    bd.commit()
    bd.refresh(CinemaAdd)

    logger.success("Кинотеатр создан успешно: id={}", CinemaAdd.idcinema)
    return CinemaAdd


def GetCinema(bd, cinemaID: int):
    logger.debug("Поиск кинотеатра по id={}", cinemaID)

    sqlcomand = select(cinema).where(cinema.idcinema == cinemaID)
    result = bd.execute(sqlcomand)

    cinema_obj = result.scalar_one_or_none()

    if cinema_obj is None:
        logger.warning("Кинотеатр id={} не найден", cinemaID)
    else:
        logger.info("Кинотеатр id={} найден", cinemaID)

    return cinema_obj


def Update(bd, cinemaID: int, updateColumns: str, newValue):
    logger.info(
        "Обновление кинотеатра id={} поле={} значение={}",
        cinemaID,
        updateColumns,
        newValue
    )

    cinemaUpd = GetCinema(bd, cinemaID)

    if cinemaUpd is None:
        logger.warning("Обновление невозможно: кинотеатр id={} не найден", cinemaID)
        return False

    if not hasattr(cinemaUpd, updateColumns):
        logger.error(
            "Ошибка обновления: поле '{}' не существует в модели cinema",
            updateColumns
        )
        return False

    setattr(cinemaUpd, updateColumns, newValue)

    bd.commit()
    bd.refresh(cinemaUpd)

    logger.success("Кинотеатр id={} успешно обновлён", cinemaID)
    return cinemaUpd


def Delete(bd, cinemaID: int):
    logger.info("Удаление кинотеатра id={}", cinemaID)

    cinemaDel = GetCinema(bd, cinemaID)

    bd.delete(cinemaDel)
    bd.commit()

    logger.success("Кинотеатр id={} успешно удалён", cinemaID)
    return True

def GetCursor(bd, skip: int, limit: int):
    logger.debug("Получение списка кинотеатров: skip={}, limit={}", skip, limit)

    sqlcomand = (
        select(cinema)
        .offset(skip)
        .limit(limit)
    )

    result = bd.execute(sqlcomand)
    cinemas = result.scalars().all()

    logger.info("Получено {} кинотеатров", len(cinemas))
    return cinemas
