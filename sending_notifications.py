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


SCHEDULE = {"teams": [
    {"time": "08:00-12:00", "pm": {"name": "Artem", "tg_username": "tim_timov"}, "students": [
        {"tg_id": "2116307301", "tg_username": "Matvey2566", "name": "Matvey"},
        {"tg_id": "2116307301", "tg_username": "Antrocent", "name": "kiRL"},
        {"tg_id": "2116307301", "tg_username": "kiselev_dmitry_moscow", "name": "Dmirty"}
    ],
     "level": "beginner", "trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
    {"time": "12:00-16:00", "pm": {"name": "Artem", "tg_username": "tim_timov"}, "students": [{"tg_id": "2116307301", "tg_username": "Matvey2566", "name": "Kiselev"}], "level": "junior", "trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"},
    {"time": "08:00-22:00", "pm": {"name": "Egor", "tg_username": "tim_timov"}, "students": [{"tg_id": "2116307301", "tg_username": "Matvey2566", "name": "Dmirt"}], "level": "beginner+", "trello": "https://trello.com/b/gyAquy6P/4-новички-2000-2020-виктор-wishkin-viktorshish-дмитрий-dmitrykiselevmoscow-kdv150275-матвей-киселев-matvey2566-id699813203"}
]}


def send_schedule(bot, schedule):
    for team in schedule["teams"]:
        time, pm, level, trello = team["time"], team["pm"]["name"]+" @"+team["pm"]["tg_username"], team["level"], team["trello"]
        for student in team["students"]:
            tg_id = student["tg_id"]
            other = ""
            for std_oth in team["students"]:
                other += std_oth["name"] + " @" + std_oth["tg_username"] + "\n"
                bot.send_message(
                    chat_id=tg_id,
                    text=f"""{time} {level} PM: {pm}
{other}
Trello: {trello}"""
                )


if __name__ == "__main__":
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    updater = Updater(token=tg_token, use_context=True)
    bot = updater.bot
    send_schedule(bot, SCHEDULE)
    # dispatcher = updater.dispatcher
    # dispatcher.add_handler(conv_handler)
    # start_handler = CommandHandler('start', start_conversation)
    # dispatcher.add_handler(start_handler)
    # dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern='to_start'))
    # updater.start_polling()
    # updater.idle()


