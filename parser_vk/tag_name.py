from database import connect_to_database


connection = connect_to_database.connection


# Функция для генераций списка новостей
def generation_list_news(tag_name: list, news_list: list) -> str:
    """
    :param tag_name: Список хэштегов
    :param news_list: Список названий мероприятий
    :return: Возвращаем сгенерированную строку
    """
    list_gen = ['👇Ниже список мероприятий👇']
    for elem, tag in zip(news_list, tag_name):
        list_gen.append(f'{news_list.index(elem) + 1}.{elem}: {tag}')
    return '\n'.join(list_gen)


# Функция для генераций списка хэштегов новостей из базы данных админа
def list_hash_database() -> list:
    with connection.cursor() as cursor:
        cursor.execute("SELECT hash FROM hash_post;")
        return cursor.fetchone()[0].split(',')


# Функция для возвращения списка названий мероприятий
def list_name_new() -> list:
    with connection.cursor() as cursor:
        cursor.execute("SELECT post FROM hash_post;")
        return cursor.fetchone()[0].split(',')


# Функция для добавления в базу данных хэштега и группы
def delete_add_hash_post_to_database(hash: list, news: list, key: str) -> None:
    """
    :param key: Параметр для удаления или добавления в базу
    :param hash: Список хэштегов
    :param news: Список названий мероприятий
    :return: Обновляем базу данных с хэштегами и их названиями
    """
    list_hash, list_name = list_hash_database(), list_name_new()
    if key == 'добавить':
        list_hash.append(hash), list_name.append(news)
    elif key == 'удалить':
        list_hash.remove(hash), list_name.remove(news)
    list_hash, list_name = ','.join(list_hash), ','.join(list_name)
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE hash_post SET hash = '{list_hash}', post = '{list_name}'")
        connection.commit()

