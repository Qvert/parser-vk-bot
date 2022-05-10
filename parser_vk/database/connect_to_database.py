import psycopg2
from parser_vk import config
import os

# Подключение к базе данных
connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode="require")
