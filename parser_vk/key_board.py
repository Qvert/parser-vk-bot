from telegram import InlineKeyboardButton

# Контактная информация
key_board_start = [
    [
        InlineKeyboardButton("Контактная информация", callback_data="cintanc"),
    ]
]

# Клавиатура возвращающая назад
back_key = [[InlineKeyboardButton("<-- Вернуться", callback_data="exit")]]

# Клавиатура для выбора мероприятия
key_board_choice = [
    [
        InlineKeyboardButton("#TechnoCom", callback_data="#TechnoCom"),
        InlineKeyboardButton("#IT-fest_2022", callback_data="#IT_fest_2022"),
    ],
    [
        InlineKeyboardButton("#IASF2022", callback_data="#IASF2022"),
        InlineKeyboardButton("#ФестивальОКК", callback_data="#ФестивальОКК"),
    ],
    [
        InlineKeyboardButton("#Нейрофест", callback_data="#Нейрофест"),
        InlineKeyboardButton("#НевидимыйМир", callback_data="#НевидимыйМир"),
    ],
    [InlineKeyboardButton("#КонкурсНИР", callback_data="#КонкурсНИР")],
]

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

# Клавиатура для выбора частоты отправки постов новостей
keyboard_frequency = [
    [
        InlineKeyboardButton("Раз в день", callback_data="one_day"),
        InlineKeyboardButton("Раз в три дня", callback_data="one_three_day"),
        InlineKeyboardButton("Раз в неделю", callback_data="one_week"),
    ]
]
