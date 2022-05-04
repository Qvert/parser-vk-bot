from functools import wraps
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
    JobQueue,
)
from telegram.ext import CallbackQueryHandler
from key_board import (
    key_board_start,
    back_key,
    key_board_choice,
    keyboard_sub_unsub,
    key_board_count,
    keyboard_frequency,
)
from parser_vk import get_posts_vk
from database.tools import *
from database import admin_tools
from tag_name import tag_names_dict
import answer_options
from loguru import logger
from flask import Flask, request

server = Flask(__name__)

# Подключение клавиатур и базы данных админа
db = admin_tools.Admin()
key_board_starting = InlineKeyboardMarkup(key_board_start)
back_key = InlineKeyboardMarkup(back_key)
key_board_choice = InlineKeyboardMarkup(key_board_choice)
keyboard_sub_unsub = InlineKeyboardMarkup(keyboard_sub_unsub)
key_board_count = ReplyKeyboardMarkup(key_board_count, one_time_keyboard=True)
keyboard_frequency = InlineKeyboardMarkup(keyboard_frequency)


# Функция декоратор для отлова ошибок
def log_error(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка: {e}")
            raise e

    return inner


@log_error
def button(update, context):
    id_user = update.effective_user.id
    query = update.callback_query
    variant = query.data
    query.answer()

    if variant == "cintanc":
        query.edit_message_text(
            text="Привет! Если у вас возникли какие-либо вопросы, то вот наши\n"
            "контакты:\n"
            "Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n"
            "Сайт с мероприятиями https://www.научим.online",
            reply_markup=back_key,
        )
    if variant == "exit":
        query.edit_message_text(
            text="Выбрать количество показывающихся постов: /count\n"
            "Выбор мероприятия: /choice\n"
            "Выбор частоты отправки новостей: /frequency\n"
            "Показать список подписанных новостей : /view\n"
            "Войти как администратор: /admin\n"
            "Начать сбор постов с новостями: /start_parser",
            reply_markup=key_board_starting,
        )

    if variant in tag_names_dict.keys():
        context.user_data["HASH"] = variant
        query.edit_message_text(variant, reply_markup=keyboard_sub_unsub)
        logger.info(f'Получил {context.user_data["HASH"]}')

    if variant == "back":
        query.edit_message_text(
            "👇Ниже список мероприятий👇\n"
            "1.Международный конкурс детских инженерных команд: #TechnoCom\n"
            "2.Международный фестиваль информационных технологий «ITфест»: #IT_fest_2022\n"
            "3.Международный аэрокосмический фестиваль: #IASF2022\n"
            "4.Всероссийский фестиваль общекультурных компетенций: #ФестивальОКК\n"
            "5.Всероссийский фестиваль нейротехнологий «Нейрофест»: #Нейрофест\n"
            "6.Всероссийский конкурс по микробиологии «Невидимый мир: #НевидимыйМир\n"
            "7.Всероссийский конкурс научноисследовательских работ: #КонкурсНИР",
            reply_markup=key_board_choice,
        )

    # Если пользователь нажал подписаться
    if variant == "subscribe":
        if not checked_hash_tag(tag_hash=context.user_data["HASH"], id_users=id_user):
            add_hash_tag(context.user_data["HASH"], id_user)
            query.edit_message_text(answer_options.get_answer_subscribe())
        else:
            query.edit_message_text("Вы уже подписаны на это мероприятие 😉")

    # Если пользователь нажал отписаться
    if variant == "unsubscribe":
        if checked_hash_tag(tag_hash=context.user_data["HASH"], id_users=id_user):
            delete_hash_tag(context.user_data["HASH"], user_id=id_user)
            query.edit_message_text(answer_options.get_answer_unsubcribe())
        else:
            query.edit_message_text("Извините, вы не были подписаны на эти новости 😑")

    # Если пользователь выбирал частоту
    if variant in ["one_day", "one_three_day", "one_week"]:
        update_freq_day(callback_freq=variant, id_user=update.effective_user.id)
        query.edit_message_text(text=answer_options.get_answer_freq())


@log_error
def helping(update: Updater, context: CallbackContext):
    """
    Функция для предоставления справки по пользованию ботом
    """
    update.message.reply_text(
        "Выбрать количество показывающихся постов: /count\n"
        "Выбор мероприятия: /choice\n"
        "Выбор частоты отправки новостей: /frequency\n"
        "Показать список подписанных новостей : /view\n"
        "Войти как администратор: /admin\n"
        "Начать сбор постов с новостями: /start_parser",
        reply_markup=key_board_starting,
    )


@log_error
def start(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "Приветствую тебя 😋, я бот-парсер, который соберёт\n"
        "новости из групп вк. Для того чтобы узнать\n"
        "как мной пользоваться нажми /help\n"
    )
    if user_exists(id_user := update.effective_user.id) is None:
        add_users(id_user)
    else:
        update.message.reply_text("Вы уже были зарегестрированы 😄")


@log_error
def answer_count(update: Updater, context: CallbackContext):
    id_user = update.effective_user.id
    if update.message.text in "12345678910":
        update_count_posts(count=update.message.text, id_user=id_user)
        update.message.reply_text(
            "Я принял ваш ответ😁😁😁\n", reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"Записал количество постов {(count := get_count_posts(id_user))}")


@log_error
def count(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "Выберите количество получаемых постов из новостей группы вк 👇👇👇",
        reply_markup=key_board_count,
    )


@log_error
def choice(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "👇Ниже список мероприятий👇\n"
        "1.Международный конкурс детских инженерных команд: #TechnoCom\n"
        "2.Международный фестиваль информационных технологий «ITфест»: #IT_fest_2022\n"
        "3.Международный аэрокосмический фестиваль: #IASF2022\n"
        "4.Всероссийский фестиваль общекультурных компетенций: #ФестивальОКК\n"
        "5.Всероссийский фестиваль нейротехнологий «Нейрофест»: #Нейрофест\n"
        "6.Всероссийский конкурс по микробиологии «Невидимый мир: #НевидимыйМир\n"
        "7.Всероссийский конкурс научноисследовательских работ: #КонкурсНИР",
        reply_markup=key_board_choice,
    )


@log_error
def frequency(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "Выберите частоту отправки сообщений", reply_markup=keyboard_frequency
    )


@log_error
def view_fag(update, context):
    if get_spisok_hash_tag(update.message.chat_id) is not None:
        update.message.reply_text(
            f"Вы подписаны на следующие хэштеги групп👇\n"
            f'{", ".join(get_spisok_hash_tag(update.message.chat_id))}\n'
        )
    else:
        update.message.reply_text("Вы не подписаны ни на какие новости 😧")


@log_error
def message_parse(context):
    id_users = context.job.context

    if not get_count_posts(id_users)[0]:
        update_count_posts(count=1, id_user=id_users)

    if not if_hash_tag_in_db(id_users):
        context.bot.send_message(
            chat_id=context.job.context,
            text="Извините, но вы не подписаны ни на какие новости😮😮😮\n"
            "Если желаете подписаться то нажмите /choice",
        )
    else:
        count = get_count_posts(id_users)  # Количество постов показываемых ботом
        spisok_tag = get_spisok_hash_tag(
            id_users
        )  # Список хэштегов которые нужно выводить

        logger.info(
            f"Информация перед парсингом посты: {count[0]} список хэш: {spisok_tag}"
        )
        for elem in spisok_tag:
            dict_posts = get_posts_vk(tag_names_dict[elem], count)
            context.bot.send_message(
                chat_id=context.job.context,
                text=f"👇👇👇 Ниже новости постов хэштега {elem} 👇👇",
            )

            # Выводим новостные посты групп
            for news in [elem["text"] for elem in dict_posts["items"]][::-1]:
                context.bot.send_message(chat_id=context.job.context, text=news)


@log_error
def got_parse_mod(update, context):
    # Функция запуска парсера по времени
    dict_freg_day = {
        "one_three_day": 259200,
        "one_week": 604800,
        "one_day": 86400
    }

    var = get_freq_day_seconds(update.message.chat_id)[0]

    if var in dict_freg_day.keys():
        update.message.reply_text(
            "Отлично, ожидайте новости в то время которое выбрали)"
        )
        context.job_queue.run_repeating(
            callback=message_parse,
            interval=dict_freg_day[var],
            context=update.message.chat_id,
        )


@log_error
def registration(update, context):
    # Функция регистраций администратора
    if db.is_admin_is_db(admin_id=update.effective_user.id):
        update.message.reply_text(
            'Извините, но вы не зарегестрированы как администратор\n'
            'Предлагаю вам пройти регистрацию'
        )
    else:
        pass


@log_error
def password(update, context):
    # Функция проверки временного пароля для входа

    if update.message.text == "секрет":
        update.message.reply_text(
            'Уникальный ключ подходит 😉'
        )
        return registration(update=update, context=context)
    else:
        update.message.reply_text(
            '😮 Прошу прощения, но ключ неверный 😮'
        )


@log_error
def admin(update, context):
    # Функция приветствия будущего админа
    update.message.reply_text(
        "😑 Вы хотите войти как администратор. 😑\n"
        "Для этого введите пожалуйста пароль,\n"
        "который был выдан вам для безопасности от других пользователей."
    )


update = Updater(token=config.BOT_TOKEN, use_context=True)
dis = update.dispatcher
job_queue = JobQueue()
job_queue.set_dispatcher(dis)

dis.add_handler(CommandHandler("admin", admin))
dis.add_handler(CommandHandler("help", helping))
dis.add_handler(CommandHandler("start", start))
dis.add_handler(CommandHandler("count", count))
dis.add_handler(CommandHandler("choice", choice))
dis.add_handler(CommandHandler("frequency", frequency))
dis.add_handler(CommandHandler("start_parser", got_parse_mod, pass_job_queue=True))
dis.add_handler(CommandHandler("view", view_fag))
dis.add_handler(MessageHandler(Filters.text, password))
dis.add_handler(MessageHandler(Filters.text, answer_count))
dis.add_handler(CallbackQueryHandler(callback=button, pass_chat_data=True))


update.start_polling()
job_queue.start()
update.idle()


if __name__ == "__main__":
    update.remove_webhook()
    update.set_webhook(url=config.API_URL)
    server.run(host="0.0.0.0", port=5000)
