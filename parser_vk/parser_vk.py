import vk
import config

session = vk.Session(access_token=config.ACCES_TOKEN)
vk_api = vk.API(session)


def get_posts_vk(owner_id: str, count: int) -> str:
    """
    :param owner_id: Айдишник группы для парсера.
    :param count: количество выводимых записей.
    :return: Собранные текста.
    """
    mas = vk_api.wall.get(owner_id=owner_id, v=5.92, count=count)
    return mas











