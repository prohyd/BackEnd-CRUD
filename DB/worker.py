from sqlalchemy import select
from loguru import logger
from DB.models import Movies


def create_movie(bd, name: str, rait: float, description: str):
    logger.info("Создание кинотеатра: name={}, rating={}", name, rait)

    movie_add = Movies(
        name_movie=name,
        rating=rait,
        description=description
    )

    bd.add(movie_add)
    bd.commit()
    bd.refresh(movie_add)

    logger.success("Кинотеатр создан успешно: id={}", movie_add.id_movie)
    return movie_add


def get_movie(bd, movie_id_input: int):
    logger.debug("Поиск кинотеатра по id={}", movie_id_input)

    sql_command = select(Movies).where(Movies.id_movie == movie_id_input)
    result = bd.execute(sql_command)

    cinema_obj = result.scalar_one_or_none()

    if cinema_obj is None:
        logger.warning("Кинотеатр id={} не найден", movie_id_input)
    else:
        logger.info("Кинотеатр id={} найден", movie_id_input)

    return cinema_obj


def update_movie(bd, movie_id_input: int, update_columns: str, new_value):
    logger.info(
        "Обновление кинотеатра id={} поле={} значение={}",
        movie_id_input,
        update_columns,
        new_value
    )

    movie_update = get_movie(bd, movie_id_input)

    if movie_update is None:
        logger.warning("Обновление невозможно: кинотеатр id={} не найден", movie_id_input)
        return False

    if not hasattr(movie_update, update_columns):
        logger.error(
            "Ошибка обновления: поле '{}' не существует в модели cinema",
            update_columns
        )
        return False

    setattr(movie_update, update_columns, new_value)

    bd.commit()
    bd.refresh(movie_update)

    logger.success("Кинотеатр id={} успешно обновлён", movie_id_input)
    return movie_update


def delete_movie(bd, movie_id_input: int):
    logger.info("Удаление кинотеатра id={}", movie_id_input)

    movie_del = get_movie(bd, movie_id_input)

    bd.delete(movie_del)
    bd.commit()

    logger.success("Кинотеатр id={} успешно удалён", movie_id_input)
    return True

def get_cursor_movie(bd, skip: int, limit: int):
    logger.debug("Получение списка кинотеатров: skip={}, limit={}", skip, limit)

    sql_command = (
        select(Movies)
        .offset(skip)
        .limit(limit)
    )

    result = bd.execute(sql_command)
    cinemas = result.scalars().all()

    logger.info("Получено {} кинотеатров", len(cinemas))
    return cinemas
