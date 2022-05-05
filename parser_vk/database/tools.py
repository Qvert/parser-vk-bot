from loguru import logger
import connect_to_database

connection = connect_to_database.connection


def user_exists(user_id: int) -> True | False:
    """
    :param user_id: Айдишник пользователя
    :return: Возвращает значени True или False в заваисимости от того есть ли user в базе данных
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id};")
        return cursor.fetchone()


def add_users(user_id: int) -> None:
    """
    :param user_id: Айдишник пользователя
    :return: Добавляет пользователя в базу данных
    """
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO users(user_id, hashtags, counts, frequency) VALUES({user_id}, '', 1, 'one_day');"
        )
        connection.commit()
        logger.info(f"Добавил пользователя {user_id} в базу")


def checked_hash_tag(tag_hash: str, id_users: int) -> True | False:
    """
    :param tag_hash: Хэштег постов
    :param id_users: Айдишник пользователя
    :return: Возвращает True или False если хэштег найден
    """
    with connection.cursor() as cursor:
        logger.info(f"Хэштег {tag_hash} получен с {id_users}")
        cursor.execute(f"SELECT hashtags FROM users WHERE user_id = {id_users};")
        check_word = cursor.fetchone()[0]
        logger.debug(f"check = {check_word}")

        if check_word is None:
            return False

        elif len(check_word.split(",")) == 1:
            if check_word == tag_hash:
                return True

        else:
            for elem in check_word.split(","):
                if elem == tag_hash:
                    return True
    return False


def add_hash_tag(tag_hash: str, id_users: int) -> None:
    """
    :param id_users: Айди пользователя
    :param tag_hash: Хэштег, который нужно добавить
    :return: Добавляет хэштег в базу, тоесть подписывается на рассылку из этой группы
    """
    with connection.cursor() as cursor:
        spisok_word = list()
        cursor.execute(f"SELECT hashtags FROM users WHERE user_id = {id_users};")
        spisok_hash = cursor.fetchone()
        if spisok_hash is not None:
            for elem in list(spisok_hash):
                spisok_word.append(elem)
        else:
            spisok_word.append(tag_hash)
        spisok_word = [el for el in spisok_word if el]
        spisok_word.append(tag_hash)
        stroka_spis = ",".join(spisok_word)
        cursor.execute(
            f"UPDATE users SET hashtags = '{stroka_spis}' WHERE user_id = {id_users};"
        )
        connection.commit()
        logger.info(f"Добавил {tag_hash} пользователю под id: {id_users}")


def delete_hash_tag(tag_hash: str, user_id: int) -> None:
    """
    :param user_id: Айдишник
    :param tag_hash: Хэштег, который выбрал пользователь
    :return: Удаляем (отписываемся) от новостей группы
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT hashtags FROM users WHERE user_id = {user_id};")
        spisok_hash_tag = cursor.fetchone()
        logger.info(f"Хэштеги с базы данных {spisok_hash_tag}")
        elements = spisok_hash_tag[0].split(",")
        logger.debug(f"Список хэштегов перед удалением {elements}")

        del elements[elements.index(tag_hash)]

        spisok_hash_tag = ",".join(elements)

        cursor.execute(
            f"UPDATE users SET hashtags = '{spisok_hash_tag}' WHERE user_id = {user_id}"
        )
        connection.commit()


def get_spisok_hash_tag(user_id: int) -> list:
    """
    :param user_id: Айди пользователя
    :return: Возвращаем список хэштегов, по которым будем парсить
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT hashtags FROM users WHERE user_id = {user_id}")
        hashtags = cursor.fetchone()
        logger.debug(f"Полученные хэштеги {hashtags}")
        return hashtags[0].split(",")


def if_hash_tag_in_db(id_users: int) -> True | False:
    """
    :param id_users: Номер пользователя
    :return: Возвращаем True или False в зависимости от того, подписан ли хоть на что-то пользователь
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT hash_tag FROM users WHERE user_id = {id_users}")
        check = list(cursor.fetchone())
        logger.info(f'Получен хэштег "{check}"')
        if check == "":
            return False
    return True


def update_count_posts(count: int, id_user: int) -> None:
    """
    :param id_user: Айдишник пользователя
    :param count: Количество показываемых постов
    :return: Обновляет поле в базе данных
    """
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE users SET counts = {count} WHERE user_id = {id_user}")
        logger.info("Изменил количество постов")
        connection.commit()


def get_count_posts(id_user: int) -> int:
    """
    :param id_user: Айдишник пользователя
    :return: Получает посты пользователя если они есть
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT counts FROM users WHERE user_id = {id_user}")
        return cursor.fetchone()


def update_freq_day(callback_freq: str, id_user: int) -> None:
    """
    :param id_user: Айдишник пользователя
    :return: Заносим в базу данных частоту отправки
    """
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE users SET frequency = '{callback_freq}' WHERE user_id = {id_user}"
        )
        logger.info("Запись успешно добавлена")
        connection.commit()


def get_freq_day_seconds(id_user: int) -> str:
    """
    :param id_user: Айдишник пользователя
    :return: Получаем частоту отправки новостей
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT frequency FROM users WHERE user_id = {id_user}")
        return cursor.fetchone()
