from functools import wraps
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Updater,
    MessageHandler,
    Filters,
    JobQueue,
)
from telegram.ext import CallbackQueryHandler
from key_board import (
    key_board_start,
    back_key,
    generation_key_board,
    keyboard_sub_unsub,
    key_board_count,
    keyboard_frequency,
    # key_board_help
)
from database.tools import Database
from database.admin_tools import Admin
from parser_vk.parser_vk_function import get_posts_vk
from tag_name import *
import answer_options
from validators import *
import os
from loguru import logger
from hash_function import *


# Подключение клавиатур и базы данных админа
db = Database()
db_admin = Admin()
key_board_starting = InlineKeyboardMarkup(key_board_start)
back_key = InlineKeyboardMarkup(back_key)
keyboard_sub_unsub = InlineKeyboardMarkup(keyboard_sub_unsub)
key_board_count = ReplyKeyboardMarkup(key_board_count, one_time_keyboard=True)
# key_board_help = ReplyKeyboardMarkup(key_board_help)
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
    id_user = hash_word(str(update.effective_user.id))
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
            text="👇 Ниже вы можете настроить бота, а также начать собирать новости 👇\n"
            "📝 Выбрать количество показывающихся постов: /count\n"
            "🔀 Выбор мероприятия: /choice\n"
            "🕔 Выбор частоты отправки новостей: /frequency\n"
            "📋 Показать список подписанных новостей : /view\n"
            "🔐 Войти как администратор: /admin\n"
            "📬 Начать сбор постов с новостями: /start_parser",
            reply_markup=key_board_starting,
        )

    if variant in list_hash_database():
        context.user_data["HASH"] = variant
        query.edit_message_text(variant, reply_markup=keyboard_sub_unsub)
        logger.info(f'Получил {context.user_data["HASH"]}')

    if variant == "back":
        query.edit_message_text(
            generation_list_news(
                tag_name=list_hash_database(), news_list=list_name_new()
            ),
            reply_markup=InlineKeyboardMarkup(
                generation_key_board(list_hash_database())
            ),
        )

    # Если пользователь нажал подписаться
    if variant == "subscribe":

        if not db.checked_hash_tag(
            tag_hash=context.user_data["HASH"], id_users=id_user
        ):
            db.add_hash_tag(context.user_data["HASH"], id_user)
            query.edit_message_text(answer_options.get_answer_subscribe())
        else:
            query.edit_message_text("Вы уже подписаны на это мероприятие 😉")

    # Если пользователь нажал отписаться
    if variant == "unsubscribe":
        if db.checked_hash_tag(tag_hash=context.user_data["HASH"], id_users=id_user):
            db.delete_hash_tag(context.user_data["HASH"], user_id=id_user)
            query.edit_message_text(answer_options.get_answer_unsubcribe())
        else:
            query.edit_message_text("Извините, вы не были подписаны на эти новости 😑")

    # Если пользователь выбирал частоту
    if variant in ["one_day", "one_three_day", "one_week"]:
        db.update_freq_day(callback_freq=variant, id_user=id_user)
        query.edit_message_text(text=answer_options.get_answer_freq())


@log_error
def helping(update: Updater, _):
    """
    Функция для предоставления справки по пользованию ботом
    """
    update.message.reply_text(
        "👇 Ниже вы можете настроить бота, а также начать собирать новости 👇\n"
        "📝 Выбрать количество показывающихся постов: /count\n"
        "🔀 Выбор мероприятия: /choice\n"
        "🕔 Выбор частоты отправки новостей: /frequency\n"
        "📋 Показать список подписанных новостей : /view\n"
        "🔐 Войти как администратор: /admin\n"
        "📬 Начать сбор постов с новостями: /start_parser",
        reply_markup=key_board_starting
    )


@log_error
def start(update: Updater, context):
    # Функция приветствия пользователя

    context.bot.send_photo(chat_id=update.effective_user.id,
                           photo='https://st3.depositphotos.com/29688696/31993/v/1600/depositphotos_319933748-stock-illustration-chat-bot-say-hi-robots.jpg')
    update.message.reply_text(
        "Приветствую тебя, я бот-парсер,\n"
        "который собирает новости из групп вк\n"
        "Для того чтобы настроить меня и получать новости нажми /help"
    )
    id_hash = hash_word(str(update.effective_user.id))
    if db.user_exists(id_hash) is None:
        db.add_users(id_hash)
    else:
        update.message.reply_text("Вы уже были зарегестрированы 😄")


@log_error
def answer_count(update: Updater, _):
    id_user = hash_word(str(update.effective_user.id))
    if update.message.text in "12345678910":
        db.update_count_posts(count=update.message.text, id_user=id_user)
        update.message.reply_text(
            "Я принял ваш ответ😁😁😁\n", reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"Записал количество постов {(db.get_count_posts(id_user))}")


@log_error
def count(update: Updater, _):
    update.message.reply_text(
        "Выберите количество получаемых постов из новостей группы вк 👇👇👇",
        reply_markup=key_board_count,
    )


@log_error
def choice(update: Updater, _):
    update.message.reply_text(
        generation_list_news(tag_name=list_hash_database(), news_list=list_name_new()),
        reply_markup=InlineKeyboardMarkup(generation_key_board(list_hash_database())),
    )


@log_error
def frequency(update: Updater, _):
    update.message.reply_text(
        "Выберите частоту отправки сообщений", reply_markup=keyboard_frequency
    )


@log_error
def view_fag(update, _):
    id_user = hash_word(str(update.message.chat_id))
    if db.get_spisok_hash_tag(id_user) is not None:
        update.message.reply_text(
            f"Вы подписаны на следующие хэштеги групп👇\n"
            f'{", ".join(db.get_spisok_hash_tag(id_user))}\n'
        )
    else:
        update.message.reply_text("Вы не подписаны ни на какие новости 😧")


@log_error
def message_parse(context):
    id_users = hash_word(str(context.job.context))

    if not db.get_count_posts(id_users):
        db.update_count_posts(count=1, id_user=id_users)

    if not db.if_hash_tag_in_db(id_users):
        context.bot.send_message(
            chat_id=context.job.context,
            text="Извините, но вы не подписаны ни на какие новости😮😮😮\n"
            "Если желаете подписаться то нажмите /choice",
        )
    else:
        count = db.get_count_posts(id_users)  # Количество постов показываемых ботом
        list_tag = db.get_spisok_hash_tag(
            id_users
        )  # Список хэштегов которые нужно выводить

        logger.info(f"Информация перед парсингом посты: {count} список хэш: {list_tag}")
        for elem in list_tag:
            dict_posts = get_posts_vk(elem, count)
            context.bot.send_message(
                chat_id=context.job.context,
                text=f"👇👇 Ниже новости постов хэштега {elem} 👇👇",
            )

            # Выводим новостные посты групп
            for news in [elem["text"] for elem in dict_posts["items"]][::-1]:
                context.bot.send_message(chat_id=context.job.context, text=news)


@log_error
def got_parse_mod(update, context):
    # Функция запуска парсера по времени
    # 259200 604800 86400
    dict_freg_day = {"one_three_day": 259200, "one_week": 604800, "one_day": 60}

    var = db.get_freq_day_seconds(id_user := hash_word(str(update.message.chat_id)))[0]

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
def registration_new_admin_nickname(update, _):
    # Функция для регистраций никнейма нового администратора
    nickname = update.message.text
    id_user = hash_word(str(update.effective_user.id))
    db_admin.add_nickname_admin(admin_id=id_user, nickname=hash_word(nickname))
    update.message.reply_text("Ваш никнейм успешно сохранён")
    update.message.reply_text("👇 Теперь вы можете использовать следующие функций 👇")
    update.message.reply_text(
        "Расширение списка новостных групп и хэштегов: /add_news\n"
        "Удаление хэштега и названия мероприятия: /delete_news"
    )
    return ConversationHandler.END


@log_error
def registration_new_admin(update, _):
    # Функция регистраций нового администратора
    id_user = hash_word(str(update.effective_user.id))
    answer = check_new_password(update.message.text, admin_id=id_user)
    if answer[0] == 0:
        update.message.reply_text(answer[1])
        update.message.reply_text(
            "Теперь придумайте себе никнейм и введите его пожалуйста"
        )
        return "REGISTRATION_NEW_ADMIN_NICKNAME"

    else:
        update.message.reply_text(answer)
        return "REGISTRATION_NEW_ADMIN"


@log_error
def password(update, context):
    # Функция проверки временного пароля для входа
    logger.debug("Перенаправил на password")
    if update.message.text == os.environ['SECRET_KEY']:
        update.message.reply_text("Уникальный ключ подходит 😉")
        update.message.reply_text(
            "Извините, но вы не зарегистрированы как администратор\n"
            "Предлагаю вам пройти регистрацию"
        )
        update.message.reply_text(
            "Для начала создайте и введите пароль, которым вы будете пользоваться"
        )
        return "REGISTRATION_NEW_ADMIN"
    elif update.message.text.lower() == "стоп":
        return commands_admins(update=update, context=context)
    else:
        update.message.reply_text("😮 Прошу прощения, но ключ неверный 😮")
        return "PASSWORD"


@log_error
def password_check_if_admin(update, context):
    # Функция проверки авторизаций для админа который был зарегестрирован
    try:
        text_check = update.message.text.split()
        logger.info(f"Пароль и никнейм введёный пользователем {text_check}")
        id_user = hash_word(str(update.effective_user.id))
        db_password_nickname = db_admin.get_password_nickname_admin(admin_id=id_user)
        logger.info(f"Пароль и никнейм из базы {db_password_nickname}")

        # Проверка что пароль и никнейм совпадают с базой данных
        if check_word(
            hashed_password=db_password_nickname[0], user_password=text_check[0]
        ) and check_word(
            hashed_password=db_password_nickname[1], user_password=text_check[1]
        ):
            update.message.reply_text(f"Приветствую вас {text_check[1]}")
            update.message.reply_text(
                "Расширение списка новостных групп и хэштегов: /add_news\n"
                "Удаление хэштега и названия мероприятия: /delete_news"
            )
            return ConversationHandler.END

        elif update.message.text.lower() == "стоп":
            return commands_admins(update=update, context=context)
        else:
            update.message.reply_text(
                "Простите, но вы неправильно ввели данные. Проверьте пожалуйста."
            )
            return "PASSWORD_CHECK_IF_ADMIN"
    except Exception as _er:
        logger.error(_er)


@log_error
def admin(update, _):
    # Функция приветствия будущего админа
    id_user = hash_word(str(update.effective_user.id))

    if db_admin.is_admin_is_db(admin_id=id_user):
        update.message.reply_text(
            "😑 Вы хотите войти как администратор. 😑\n"
            "Для начала введите пожалуйста пароль,\n"
            "который был выдан вам для безопасности от других пользователей."
        )
        return "PASSWORD"

    else:
        update.message.reply_text(
            "👨‍💻 Вы уже являетесь администратором. 👨‍💻\n"
            "Для проверки, пожалуйста авторизуйтесь.\n"
            "Введите через пробел сначала пароль, потом ваш никнейм"
        )
        return "PASSWORD_CHECK_IF_ADMIN"


@log_error
def commands_admins(update, context):
    # Функция для остановки выполнения
    update.message.reply_text("Вас понял, отменил действие")
    return ConversationHandler.END


@log_error
def add_news(update, _):
    update.message.reply_text("Для начала введите название мероприятия или группы ")
    return "ADD_NEWS"


@log_error
def add_news_word(update, context):
    # Функция добавление название мероприятия
    text_news = update.message.text
    if check_correct_news(text_news):
        context.user_data["NEWS"] = text_news

        update.message.reply_text(
            "Отлично, теперь введите хэштег или короткое название группы, откуда будем собирать новости"
        )
        return "ADD_HASH"
    else:
        update.message.reply_text(
            "Простите, но название должно содержать только русские буквы"
        )
        return "ADD_NEWS"


@log_error
def add_news_hash(update, context):
    # Функция добавления хэштега
    news_hash = update.message.text
    logger.info("Получен хэштег")
    if check_correct_hash(news_hash):
        delete_add_hash_post_to_database(
            hash=news_hash, news=context.user_data["NEWS"], key="добавить"
        )
        update.message.reply_text("Отлично, список групп успешно расширен)\n")
        update.message.reply_text(
            "Расширение списка новостных групп и хэштегов: /add_news\n"
            "Удаление хэштега и названия мероприятия: /delete_news"
        )
        return ConversationHandler.END
    else:
        update.message.reply_text("Пожалуйста, введите коректно хэштег")
        return "ADD_HASH"


@log_error
def delete_news(update, _):
    # Функция для удаления хэштега и названия группы
    update.message.reply_text("Введите название группы")
    update.message.reply_text("👇Ниже список мероприятий👇")
    update.message.reply_text(
        '.\n'.join(list_name_new())
    )
    return "DELETE_POST"


@log_error
def delete_post(update, context):
    # Функция для получения названия поста для удаления
    post = update.message.text
    if post not in list_name_new():
        update.message.reply_text("Проверьте правильность написания!!!")
        return "DELETE_POST"
    else:
        context.user_data["NEWS"] = post
        update.message.reply_text("Теперь введите хэштег группы")
        update.message.reply_text("👇Ниже список хэштегов👇")
        update.message.reply_text(
            '.\n'.join(list_hash_database())
        )
        return "DELETE_HASH"


@log_error
def delete_hash(update, context):
    # Функция для удаления хэштега и названия группы
    hash = update.message.text
    if hash not in list_hash_database():
        update.message.text("Неправильно набран хэштег!!!")
        return "DELETE_HASH"
    else:
        delete_add_hash_post_to_database(
            hash=hash, news=context.user_data["NEWS"], key="удалить"
        )
        update.message.reply_text("Список успешно изменён")
        update.message.reply_text(
            "Расширение списка новостных групп и хэштегов: /add_news\n"
            "Удаление хэштега и названия мероприятия: /delete_news"
        )
        return ConversationHandler.END


def main():
    update = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
    dis = update.dispatcher
    job_queue = JobQueue()
    job_queue.set_dispatcher(dis)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("admin", admin)],
        states={
            "PASSWORD": [
                MessageHandler(Filters.text, password)
            ],
            "REGISTRATION_NEW_ADMIN": [
                MessageHandler(Filters.text, registration_new_admin)
            ],
            "REGISTRATION_NEW_ADMIN_NICKNAME": [
                MessageHandler(Filters.text, registration_new_admin_nickname)
            ],
            "PASSWORD_CHECK_IF_ADMIN": [
                MessageHandler(Filters.text, password_check_if_admin)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, commands_admins)],
    )

    conv_handler_add_hash_post = ConversationHandler(
        entry_points=[CommandHandler('add_news', add_news)],
        states={
            "ADD_NEWS": [
                MessageHandler(Filters.text, add_news_word)
            ],
            "ADD_HASH": [
                MessageHandler(Filters.text, add_news_hash)
            ],
        },
        fallbacks=[MessageHandler(Filters.text, commands_admins)]
    )

    conv_handler_delete_hash_post = ConversationHandler(
        entry_points=[CommandHandler('delete_news', delete_news)],
        states={
            "DELETE_POST": [
                MessageHandler(Filters.text, delete_post)
            ],
            "DELETE_HASH": [
                MessageHandler(Filters.text, delete_hash)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, commands_admins)]
    )
    dis.add_handler(conv_handler)
    dis.add_handler(conv_handler_add_hash_post)
    dis.add_handler(conv_handler_delete_hash_post)
    dis.add_handler(CommandHandler("admin", admin))
    dis.add_handler(CommandHandler("help", helping))
    dis.add_handler(CommandHandler("start", start))
    dis.add_handler(CommandHandler("count", count))
    dis.add_handler(CommandHandler("choice", choice))
    dis.add_handler(CommandHandler("frequency", frequency))
    dis.add_handler(CommandHandler("start_parser", got_parse_mod, pass_job_queue=True))
    dis.add_handler(CommandHandler("view", view_fag))

    dis.add_handler(MessageHandler(Filters.text, answer_count))
    dis.add_handler(CallbackQueryHandler(callback=button, pass_chat_data=True))

    update.start_polling()
    job_queue.start()
    update.idle()


if __name__ == "__main__":
    main()
