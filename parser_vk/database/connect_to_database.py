import psycopg2
import os


# Подключение к базе данных
connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode="require")
