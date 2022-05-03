import sqlite3
from loguru import logger


class Database:
    def __init__(self, db_file):
        """
        :param db_file: Название базы данных
        """
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id: int) -> bool:
        """
        :param user_id: Айдишник пользователя в телеграмм
        :return: Возвращает значени True или False в заваисимости от того есть ли user в базе данных
        """
        with self.connection:
            result = self.cursor.execute(
                """SELECT id_users FROM users WHERE id_users = ?""", (user_id,)
            ).fetchone()
            return result

    def add_users(self, user_id: int):
        """
        :param user_id: Айдишник пользователя
        :return: Добавляет пользователя в базу данных
        """
        with self.connection:
            self.cursor.execute("""INSERT INTO users(id_users) VALUES(?)""", (user_id,))
            logger.info(f"Добавил пользователя {user_id} в базу")

    def checked_hash_tag(self, tag_hash: str, id_users: int):
        """
        :param tag_hash: Хэштег постов
        :param id_users: Айдишник пользователя
        :return: Возвращает True или False если хэштег найден
        """
        with self.connection:
            logger.info(f"Хэштег {tag_hash} получен с {id_users}")
            check = self.cursor.execute(
                """SELECT hash_tag FROM users WHERE id_users = ?""", (id_users,)
            ).fetchall()
            check = check[0][0]
            logger.debug(f"check = {check}")

            if not check:
                return False

            elif len(check.split(",")) == 1:
                if check == tag_hash:
                    return True

            else:
                for elem in check.split(","):
                    if elem == tag_hash:
                        return True
        return False

    def add_hash_tag(self, tag_hash: list, id_users: int):
        """
        :param tag_hash: Хэштег, который нужно добавить
        :return: Добавляет хэштег в базу, тоесть подписывается на рассылку из этой группы
        """
        with self.connection:
            spisok = list()
            spisok_hash = self.cursor.execute(
                """SELECT hash_tag FROM users WHERE id_users = ?""", (id_users,)
            ).fetchall()
            for elem in list(spisok_hash):
                spisok.append(elem[0])
            spisok = [el for el in spisok if el]
            spisok.append(tag_hash)
            stroka_spis = ",".join(spisok)
            self.cursor.execute(
                f"""UPDATE users SET hash_tag = ? WHERE id_users = ?""",
                (stroka_spis, id_users),
            )

    def delete_hash_tag(self, tag_hash: str, user_id: int):
        """
        :param user_id: Айдишник
        :param tag_hash: Хэштег, который выбрал пользователь
        :return: Удаляем (отписываемся) от новостей группы
        """
        with self.connection:
            spisok_hash_tag = self.cursor.execute(
                """SELECT hash_tag FROM users WHERE id_users = ?""", (user_id,)
            ).fetchall()
            elements = spisok_hash_tag[0][0].split(",")

            del elements[elements.index(tag_hash)]

            spisok_hash_tag = ",".join(elements)

            self.cursor.execute(
                """UPDATE users SET hash_tag = ? WHERE id_users = ?""",
                (spisok_hash_tag, user_id),
            )

    def get_spisok_hash_tag(self, user_id: int) -> list:
        """
        :param user_id: Айди пользователя
        :return: Возвращаем список хэштегов, по которым будем парсить
        """
        with self.connection:
            spisok_hash_tag = self.cursor.execute(
                """SELECT hash_tag FROM users WHERE id_users = ?""", (user_id,)
            ).fetchall()
            return spisok_hash_tag[0][0].split(",")

    def if_hash_tag_in_db(self, id_users: int) -> bool:
        """
        :param id_users: Номер пользователя
        :return: Возвращаем True или False в зависимости от того, подписан ли хоть на что-то пользователь
        """
        with self.connection:
            hash_tags = self.cursor.execute(
                """SELECT hash_tag FROM users WHERE id_users = ?""", (id_users,)
            ).fetchall()
            check = hash_tags[0][0]
            logger.info(f'Получен хэштег "{check}"')
            if check == "":
                return False
        return True

    def update_count_posts(self, count: int, id_user: int):
        """
        :param id_user: Айдишник пользователя
        :param count: Количество показываемых постов
        :return: Обновляет поле в базе данных
        """
        with self.connection:
            self.cursor.execute(
                """UPDATE users SET count_posts = ? WHERE id_users = ?""",
                (count, id_user),
            ).fetchone()
            logger.info("Изменил количество постов")

    def get_count_posts(self, id_user: int):
        """
        :param id_user: Айдишник пользователя
        :return: Получает посты пользователя если они есть
        """
        with self.connection:
            count_posts = self.cursor.execute(
                """SELECT count_posts FROM users WHERE id_users = ?""", (id_user,)
            ).fetchone()
            return count_posts

    def update_freq_day(self, callback_freq: str, id_user: int):
        """
        :param id_user: Айдишник пользователя
        :return: Заносим в базу данных частоту отправки
        """
        with self.connection:
            self.cursor.execute(
                """UPDATE users SET frequency_day = ? WHERE id_users = ?""",
                (callback_freq, id_user),
            )
            logger.info("Запись успешно добавлена")

    def get_freq_day_seconds(self, id_user: int):
        """
        :param id_user: Айдишник пользователя
        :return: Получаем частоту отправки новостей
        """
        with self.connection:
            return self.cursor.execute(
                """SELECT frequency_day FROM users WHERE id_users = ?""", (id_user,)
            ).fetchone()
