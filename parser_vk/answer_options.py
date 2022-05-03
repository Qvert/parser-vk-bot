import random


def get_answer_freq():
    spisok_ans = [
        'Изменение успешно внесены)',
        'Изменения вступили в силу😁',
        'Ваш ответ принят😁'
    ]
    return random.choice(spisok_ans)


def get_answer_subscribe():
    spisok_answer = [
        'Теперь вы подписаны на эти новости 😉😉😉',
        'Подписка успешно оформлена)))',
        'Вы успешно подписаны на новости 😊😊😊'
    ]
    return random.choice(spisok_answer)


def get_answer_unsubcribe():
    spisok_answer = [
        'Вы отписаны от новостей этой группы(',
        'Отписка произошла успешно 🙃',
        'Вы успешно отписались от новостей этой группы'
    ]
    return random.choice(spisok_answer)


