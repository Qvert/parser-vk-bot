from loguru import logger
from . import connect_to_database


connection = connect_to_database.connection


class Admin:
    def __init__(self):
        self.connection = connect_to_database.connection

    def is_admin_is_db(self, admin_id: int) -> True | False:
        """
        :param admin_id: Айди админимстратора
        :return: Возвращаем True или False в зависимости от того, есть ли админ в базе
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT admin_id FROM admins WHERE admin_id = {admin_id};")
            logger.debug("Вернул проверку админа")
            return cursor.fetchone()

    def get_password_admin(self, admin_id: int) -> None:
        """
        :param admin_id: Айди администратора
        :return: Возвращает пароль для входа
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT admin_password FROM admins WHERE admin_id = {admin_id};"
            )
            logger.info(f"Вернул пароль {cursor.fetchone()}")
            return cursor.fetchone()

    def get_nickname_admin(self, admin_id: int) -> None:
        """
        :param admin_id: Айди администратора
        :return: Возвращает его никнейм
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT admin_nickname FROM admins WHERE admin_id = {admin_id};"
            )
            logger.info(f"Вернул никнейм {cursor.fetchone()}")
            return cursor.fetchone()

    def add_password_admin_to_base(self, admin_id: int, password: str) -> None:
        """
        :param password: Пароль, придуманный администратором при регистраций
        :param admin_id: Айди администратора
        :return: Добавляет пароль в базу данных
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE admins SET admin_password = '{password}' WHERE admin_id = {admin_id}"
            )
            logger.debug(f"Добавил в базу данных пароль {password} от {admin_id}")
            self.connection.commit()

    def add_nickname_admin(self, admin_id: int, nickname: str) -> None:
        """
        :param admin_id: Айди администратора
        :param nickname: Никнейм, придуманный при регистраций
        :return: Добавляем никнейм в базу данных
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE admins SET admin_nickname = '{nickname}' WHERE admin_id = {admin_id}"
            )
            logger.debug("Добавил никнейм в базу данных")
            self.connection.commit()

    def add_admins_to_database(self, user_id: int) -> None:
        """
        :param user_id: айди будущего админа
        :return: добавляем админа в базу данных
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                f'INSERT INTO admins(admin_id, admin_password, admin_nickname, admin_hash, admin_post)'
                f' VALUES({user_id}, '', '', '', '');'
            )
            logger.info('Закинул admin_id в базу')
            self.connection.commit()
