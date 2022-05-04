import psycopg2
from loguru import logger
from parser_vk import config


class Admin:
    def __init__(self):
        self.connection = psycopg2.connect(config.DATABASEP_URL, sslmode='require')
        self.cursor = self.connection.cursor()

    def is_admin_is_db(self, admin_id) -> True | False:
        """
        :param admin_id: Айди админимстратора
        :return: Возвращаем True или False в зависимости от того, есть ли админ в базе
        """
        with self.connection:
            self.cursor.execute("SELECT admin_id FROM admins;")
            logger.debug('Вернул проверку админа')
            return self.cursor.fetchone() is None


