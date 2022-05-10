from telegram import InlineKeyboardButton

# Контактная информация
key_board_start = [
    [
        InlineKeyboardButton("Контактная информация", callback_data="cintanc"),
    ]
]

# Клавиатура возвращающая назад
back_key = [[InlineKeyboardButton("<-- Вернуться", callback_data="exit")]]


# Клавиатура для подписки и отписки на мероприятие
keyboard_sub_unsub = [
    [
        InlineKeyboardButton("Подписаться", callback_data="subscribe"),
        InlineKeyboardButton("Отписаться", callback_data="unsubscribe"),
    ],
    [InlineKeyboardButton("<-- Вернуться", callback_data="back")],
]

# Клавиатура для выбора количества показываемых постов
key_board_count = [["1", "2", "3", "4", "5"], ["6", "7", "8", "9", "10"]]

# Клавиатура для помощи
key_board_help = [['/count', '/choice', '/frequency'], ['/view', '/admin', '/start_parser']]

# Клавиатура для выбора частоты отправки постов новостей
keyboard_frequency = [
    [
        InlineKeyboardButton("Раз в день", callback_data="one_day"),
        InlineKeyboardButton("Раз в три дня", callback_data="one_three_day"),
        InlineKeyboardButton("Раз в неделю", callback_data="one_week"),
    ]
]


# Функция для генераций клавиатуры в зависимости от количества хэштегов
def generation_key_board(list_hash: list) -> list:
    """
    :param list_hash: Список хэштегов
    :return: Возвращаем сгенерированную клавиатуру
    """
    key_board_choice = []
    for elem in list_hash:
        key_board_choice.append([InlineKeyboardButton(elem, callback_data=elem)])
    return key_board_choice
