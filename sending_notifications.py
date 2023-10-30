import telegram
import os
import django
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

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'project_automation_admin.settings'
    )
django.setup()

from admin_panel.models import Team, Student


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


def send_schedule(bot):
    for team in Team.objects.all():
        # time, pm, level, trello = team["time"], team["pm"]["name"]+" @"+team["pm"]["tg_username"], team["level"], team["trello"]
        time, pm, level, brief, trello = team.timeslot, team.project_manager.full_name, team.level, team.brief, team.trello_board_link
        if team.project_manager.telegram_nickname:
            pm += " @" + team.project_manager.telegram_nickname

        students = ""
        for student in team.students.all():
            students += student.full_name
            if student.username:
                students += " @" + student.username
            students += "\n"

        for student in team.students.all():
            tg_id = student.telegram_chat_id
            if tg_id:
                bot.send_message(
                    chat_id=tg_id,
                    text=f"""{time} {level}
PM: {pm}
{students}
Brief: {brief}
Trello: {trello}"""
                )


if __name__ == "__main__":
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    updater = Updater(token=tg_token, use_context=True)
    bot = updater.bot
    send_schedule(bot)
