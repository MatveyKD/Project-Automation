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


def send_schedule(bot, pm=None):
    if pm:
        teams = Team.objects.filter(project_manager=pm, status="full")
    else:
        teams = Team.objects.filter(status="full")
    for team in teams:
        time, pm, level, brief, trello = team.timeslot, team.project_manager.full_name, team.level, team.brief, team.trello_board_link
        if team.project_manager.telegram_nickname:
            pm += " @" + team.project_manager.telegram_nickname

        students = ""
        for student in team.students.all():
            students += student.student.full_name
            if student.student.username:
                students += " @" + student.student.username
            students += "\n"

        for student in team.students.all():
            tg_id = student.student.telegram_chat_id
            if tg_id:
                bot.send_message(
                    chat_id=tg_id,
                    text=f"""{time} {level}
PM: {pm}
{students}
Brief: {brief}
Trello: {trello}"""
                )
    if teams.count() == 0:
        return False
    return True


if __name__ == "__main__":
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    updater = Updater(token=tg_token, use_context=True)
    bot = updater.bot
    send_schedule(bot)
