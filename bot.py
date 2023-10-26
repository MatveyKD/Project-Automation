import telegram
import os
from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
    LabeledPrice,
    InputMediaPhoto,
)
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    PreCheckoutQueryHandler,
    ConversationHandler
)

PMS = {"pms": [{"tg_username": "Matvey256", "times": []}, {"tg_username": "Matvey256", "times": [""]}]}  # will json
ADMINS = {"admins": {}}  # will json
STUDENTS = {"students": [{"tg_username": "Matvey2566", "times": [], "level": "junior", "is_actived": True}]}  # will json


def start_conversation(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id
    print(update)
    username = update.effective_user.username
    keyboard = []
    filepath = ""
    if username in list(map(lambda x: x["tg_username"], STUDENTS["students"])):
        context.user_data["role"] = "student"
        keyboard = [
            [InlineKeyboardButton("Подать заявку", callback_data='send_query')],
            [InlineKeyboardButton("Посмотреть расписание", callback_data='get_schedule_student')],
            [InlineKeyboardButton("Изменить расписание", callback_data='change_schedule_student')],
            [InlineKeyboardButton("Отказаться от записи", callback_data='cancel_query')],
        ]
        filepath = os.path.join("static/", "greetingsStudent.jpg")
    elif username in list(map(lambda x: x["tg_username"], PMS["pms"])):
        context.user_data["role"] = "pm"
        keyboard = [
            [InlineKeyboardButton("Посмотреть расписание", callback_data='get_schedule_pm')],
            [InlineKeyboardButton("Изменить расписание", callback_data='change_schedule_pm')],
            [InlineKeyboardButton("Сделать рассылку в группы", callback_data='send_mailing_groups')],
        ]
        filepath = os.path.join("static/", "greetingsPM.png")
    elif username in list(map(lambda x: x["tg_username"], ADMINS["admins"])):
        context.user_data["role"] = "admin"
        keyboard = [
            [InlineKeyboardButton("Создать расписание", callback_data='create_schedule')],
            [InlineKeyboardButton("Посмотреть расписание", callback_data='get_schedule_admin')],
            [InlineKeyboardButton("Сделать рассылку", callback_data='send_mailing')],
        ]
        filepath = os.path.join("static/", "greetingsAdmin.png")
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open(filepath, 'rb') as file:
        update.effective_message.reply_photo(
            photo=file,
            caption=f"""Приветствую, {context.user_data["role"]}""",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    return 'GREETINGS'


def send_query(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id
    keyboard = [
        [InlineKeyboardButton("8:00 - 12:00", callback_data='ch_time_student_1')],
        [InlineKeyboardButton("12:00 - 16:00", callback_data='ch_time_student_2')],
        [InlineKeyboardButton("18:00 - 22:00", callback_data='ch_time_student_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(
        text=f"""Выберите интервал""",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return 'CHS_TIME_STUDENT'


def ch_time_student_1(update, context):
    context.user_data["time_interval"] = "8:00 - 12:00"
    return time_student_chd(update, context)


def ch_time_student_2(update, context):
    context.user_data["time_interval"] = "12:00 - 16:00"
    return time_student_chd(update, context)


def ch_time_student_3(update, context):
    context.user_data["time_interval"] = "18:00 - 22:00"
    return time_student_chd(update, context)


def time_student_chd(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    username = update.effective_user.username
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id

    ind = list(map(lambda x: x["tg_username"], STUDENTS["students"])).index(username)
    student = STUDENTS["students"][ind]
    student["times"] = [context.user_data["time_interval"]]

    keyboard = [
        [InlineKeyboardButton("В меню", callback_data='to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(
        text=f"""Ваша заявка отправлена""",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    print(STUDENTS)
    return 'TIME_CHD'


def get_schedule_student(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    username = update.effective_user.username
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id

    time_interval = context.user_data["time_interval"]

    keyboard = [
        [InlineKeyboardButton("В меню", callback_data='to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(
        text=f"""Ваше временное окно: {time_interval}""",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    print(STUDENTS)
    return 'TIME_CHD'


def change_schedule_student(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id
    print(context.user_data)
    if context.user_data.get("time_interval"):
        keyboard = [
            [InlineKeyboardButton("8:00 - 12:00", callback_data='chg_time_student_1')],
            [InlineKeyboardButton("12:00 - 16:00", callback_data='chg_time_student_2')],
            [InlineKeyboardButton("18:00 - 22:00", callback_data='chg_time_student_3')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.reply_text(
            text=f"""Выберите новый интервал""",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Подать заявку", callback_data='send_query')],
            [InlineKeyboardButton("В меню", callback_data='to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.reply_text(
            text=f"""Сначала отправьте заявку""",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    return 'CHG_TIME_STUDENT'


def chg_time_student_1(update, context):
    context.user_data["time_interval"] = "8:00 - 12:00"
    return time_student_chgd(update, context)


def chg_time_student_2(update, context):
    context.user_data["time_interval"] = "12:00 - 16:00"
    return time_student_chgd(update, context)


def chg_time_student_3(update, context):
    context.user_data["time_interval"] = "18:00 - 22:00"
    return time_student_chgd(update, context)


def time_student_chgd(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    username = update.effective_user.username
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id

    ind = list(map(lambda x: x["tg_username"], STUDENTS["students"])).index(username)
    student = STUDENTS["students"][ind]
    student["times"] = [context.user_data["time_interval"]]

    keyboard = [
        [InlineKeyboardButton("В меню", callback_data='to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(
        text=f"""Временное окно было изменено""",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    print(STUDENTS)
    return 'TIME_CHD'


def cancel_query(update, context):
    query = update.callback_query
    user_first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    username = update.effective_user.username
    context.user_data['user_first_name'] = user_first_name
    context.user_data['user_id'] = user_id

    context.user_data["time_interval"] = None
    ind = list(map(lambda x: x["tg_username"], STUDENTS["students"])).index(username)
    student = STUDENTS["students"][ind]
    student["times"] = []
    # Добавить удаление из составленного расписания

    keyboard = [
        [InlineKeyboardButton("В меню", callback_data='to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(
        text=f"""Ваша заявка отменена""",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    print(STUDENTS)
    return 'TIME_CHD'


def get_schedule_pm(update, context): pass
def change_schedule_pm(update, context): pass
def send_mailing_groups(update, context): pass
def create_schedule(update, context): pass
def get_schedule_admin(update, context): pass
def send_mailing(update, context): pass


def main():
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_conversation)],
        states={
            'GREETINGS': [
                CallbackQueryHandler(send_query, pattern='send_query'),
                CallbackQueryHandler(get_schedule_student, pattern='get_schedule_student'),
                CallbackQueryHandler(change_schedule_student, pattern='change_schedule_student'),
                CallbackQueryHandler(cancel_query, pattern='cancel_query'),
                CallbackQueryHandler(get_schedule_pm, pattern='get_schedule_pm'),
                CallbackQueryHandler(change_schedule_pm, pattern='change_schedule_pm'),
                CallbackQueryHandler(send_mailing_groups, pattern='send_mailing_groups'),
                CallbackQueryHandler(create_schedule, pattern='create_schedule'),
                CallbackQueryHandler(get_schedule_admin, pattern='get_schedule_admin'),
                CallbackQueryHandler(send_mailing, pattern='send_mailing'),
            ],
            'CHS_TIME_STUDENT': [
                CallbackQueryHandler(ch_time_student_1, pattern='ch_time_student_1'),
                CallbackQueryHandler(ch_time_student_2, pattern='ch_time_student_2'),
                CallbackQueryHandler(ch_time_student_3, pattern='ch_time_student_3'),
            ],
            'CHG_TIME_STUDENT': [
                CallbackQueryHandler(start_conversation, pattern='to_menu'),
                CallbackQueryHandler(send_query, pattern='send_query'),
                CallbackQueryHandler(chg_time_student_1, pattern='chg_time_student_1'),
                CallbackQueryHandler(chg_time_student_2, pattern='chg_time_student_2'),
                CallbackQueryHandler(chg_time_student_3, pattern='chg_time_student_3'),
            ],
            'TIME_CHD': [
                CallbackQueryHandler(start_conversation, pattern='to_menu'),
            ]
        },
        fallbacks=[CommandHandler('cancel', start_conversation)],
        per_chat=False
    )
    dispatcher.add_handler(conv_handler)
    start_handler = CommandHandler('start', start_conversation)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern='to_start'))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
