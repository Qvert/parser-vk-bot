import psycopg2
from parser_vk import config

# Подключение к базе данных
connection = psycopg2.connect(config.DATABASEP_URL, sslmode="require")
