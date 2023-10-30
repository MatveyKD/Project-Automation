import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler
)
from project_automation_admin.settings import STATIC_URL, BASE_DIR
from admin_panel.models import Student, ProjectManager, Team

from write_schedule import write_schedule
from sending_notifications import send_schedule
from create_teams import create_project_teams

from environs import Env

env = Env()
env.read_env()

BOT = None


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        global BOT
        print("H")
        load_dotenv()
        tg_token = env.str("TG_BOT_TOKEN")
        updater = Updater(token=tg_token, use_context=True)
        BOT = updater.bot
        dispatcher = updater.dispatcher

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
            if username in list(map(lambda x: x.username, list(Student.objects.all()))):
                context.user_data["role"] = "student"
                student = Student.objects.get(username=username)
                user_fullname = student.full_name
                student.telegram_chat_id = update.effective_user.id
                if student.status not in ["fixed", "waiting"]: student.status = "started"
                student.save()
                context.user_data["student"] = student
                keyboard = [
                    [InlineKeyboardButton("Подать заявку", callback_data='send_query')],
                    [InlineKeyboardButton("Посмотреть расписание", callback_data='get_schedule_student')],
                    [InlineKeyboardButton("Изменить заявку", callback_data='change_schedule_student')],
                    [InlineKeyboardButton("<т. р.> Отказаться от записи", callback_data='cancel_query')],
                ]
                filepath = os.path.join(STATIC_URL, "greetingsStudent.jpg")
            elif username in list(map(lambda x: x.telegram_nickname, list(ProjectManager.objects.all()))):
                context.user_data["role"] = "pm"
                context.user_data["pm"] = ProjectManager.objects.get(telegram_nickname=username)
                user_fullname = context.user_data["pm"].full_name
                keyboard = [
                    [InlineKeyboardButton("Посмотреть расписание", callback_data='get_schedule_pm')],
                    [InlineKeyboardButton("<т. р.> Изменить расписание", callback_data='change_schedule_pm')],
                    [InlineKeyboardButton("Сделать рассылку в группы", callback_data='send_mailing_groups')],
                ]
                filepath = os.path.join(STATIC_URL, "greetingsPM.png")
            elif username in env.list("ADMINS"):
                context.user_data["role"] = "admin"
                user_fullname = env.str("ADMIN_NAME")
                keyboard = [
                    [InlineKeyboardButton("<т. р.> Загрузить файлы", callback_data='upload_files')],
                    [InlineKeyboardButton("Создать расписание", callback_data='create_schedule')],
                    [InlineKeyboardButton("Посмотреть расписание", callback_data='get_schedule_admin')],
                    [InlineKeyboardButton("Сделать рассылку", callback_data='send_mailing')],
                ]
                filepath = os.path.join(STATIC_URL, "greetingsAdmin.png")
            else:
                print(type(str(list(env.list("ADMINS"))[0])), str(list(env.list("ADMINS"))[0]), username)
                update.effective_message.reply_text(
                    text=f"""Вас нет в списке учеников. Обратитесь к администратору""",
                    parse_mode=ParseMode.HTML
                )
                return
            reply_markup = InlineKeyboardMarkup(keyboard)
            with open(filepath, 'rb') as file:
                update.effective_message.reply_photo(
                    photo=file,
                    caption=f"""Приветствую, {user_fullname}""",
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
            keyboard = []
            print(context.user_data["student"].status)
            if context.user_data["student"].status != "fixed":
                context.user_data['pms'] = ProjectManager.objects.all()
                for ind, pm in enumerate(context.user_data['pms']):
                    keyboard.append([InlineKeyboardButton(pm.period, callback_data=f'ch_time_student_{ind+1}')]),
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.effective_message.reply_text(
                    text=f"""Выберите интервал""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            else:
                keyboard = [
                    [InlineKeyboardButton("В меню", callback_data='to_menu')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.effective_message.reply_text(
                    text=f"""Вы уже зафискированы за командой""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'CHS_TIME_STUDENT'

        def ch_time_student_1(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][0].period
            return time_student_chd(update, context)

        def ch_time_student_2(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][1].period
            return time_student_chd(update, context)

        def ch_time_student_3(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][2].period
            return time_student_chd(update, context)

        def ch_time_student_4(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][3].period
            return time_student_chd(update, context)

        def ch_time_student_5(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][4].period
            return time_student_chd(update, context)

        def time_student_chd(update, context):
            query = update.callback_query
            user_first_name = update.effective_user.first_name
            user_id = update.effective_user.id
            username = update.effective_user.username
            context.user_data['user_first_name'] = user_first_name
            context.user_data['user_id'] = user_id

            student = context.user_data["student"]
            student.period_requested = context.user_data["time_interval"]
            student.status = "waiting"
            student.save()

            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.effective_message.reply_text(
                text=f"""Ваша заявка отправлена""",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            return 'TIME_CHD'

        def get_schedule_student(update, context):
            query = update.callback_query
            user_first_name = update.effective_user.first_name
            user_id = update.effective_user.id
            username = update.effective_user.username
            context.user_data['user_first_name'] = user_first_name
            context.user_data['user_id'] = user_id

            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            team = context.user_data["student"].student_team.all()
            if team.count() > 0:
                team = team.all()[0]
                time, pm, level, brief, trello = team.timeslot, team.project_manager.full_name, team.level, team.brief, team.trello_board_link
                if team.project_manager.telegram_nickname:
                    pm += " @" + team.project_manager.telegram_nickname
                students = ""
                for student in team.students.all():
                    students += student.student.full_name
                    if student.username:
                        students += " @" + student.student.username
                    students += "\n"

                update.effective_message.reply_text(
                    text=f"""{time} {level}
PM: {pm}
{students}
Brief: {brief}
Trello: {trello}""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            elif Team.objects.filter(status="full").count() == 0:
                update.effective_message.reply_text(
                    text=f"""Нет сформированных групп""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            else:
                update.effective_message.reply_text(
                    text=f"""Для вас не нашлось свободных мест в командах""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'TIME_CHD'

        def change_schedule_student(update, context):
            query = update.callback_query
            user_first_name = update.effective_user.first_name
            user_id = update.effective_user.id
            context.user_data['user_first_name'] = user_first_name
            context.user_data['user_id'] = user_id
            print(context.user_data)
            if context.user_data["student"].status != "fixed":
                if context.user_data["student"].period_requested:
                    keyboard = []
                    context.user_data['pms'] = ProjectManager.objects.all()
                    for ind, pm in enumerate(context.user_data['pms']):
                        keyboard.append([InlineKeyboardButton(pm.period, callback_data=f'chg_time_student_{ind + 1}')]),
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
            else:
                keyboard = [
                    [InlineKeyboardButton("В меню", callback_data='to_menu')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.effective_message.reply_text(
                    text=f"""Вы уже зафискированы за командой""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'CHG_TIME_STUDENT'

        def chg_time_student_1(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][0].period
            return time_student_chgd(update, context)

        def chg_time_student_2(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][1].period
            return time_student_chgd(update, context)

        def chg_time_student_3(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][2].period
            return time_student_chgd(update, context)

        def chg_time_student_4(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][3].period
            return time_student_chgd(update, context)

        def chg_time_student_5(update, context):
            context.user_data["time_interval"] = context.user_data['pms'][4].period
            return time_student_chgd(update, context)

        def time_student_chgd(update, context):
            query = update.callback_query
            user_first_name = update.effective_user.first_name
            user_id = update.effective_user.id
            username = update.effective_user.username
            context.user_data['user_first_name'] = user_first_name
            context.user_data['user_id'] = user_id

            student = context.user_data["student"]
            student.period_requested = context.user_data["time_interval"]
            student.save()

            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.effective_message.reply_text(
                text=f"""Временное окно было изменено""",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            return 'TIME_CHD'

        def cancel_query(update, context):
            query = update.callback_query
            user_first_name = update.effective_user.first_name
            user_id = update.effective_user.id
            username = update.effective_user.username
            context.user_data['user_first_name'] = user_first_name
            context.user_data['user_id'] = user_id

            if context.user_data["student"].status != "fixed":
                student = context.user_data["student"]
                student.period_requested = None
                student.status = "canceled"
                student.save()

                keyboard = [
                    [InlineKeyboardButton("В меню", callback_data='to_menu')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.effective_message.reply_text(
                    text=f"""Ваша заявка отменена""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            else:
                keyboard = [
                    [InlineKeyboardButton("В меню", callback_data='to_menu')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.effective_message.reply_text(
                    text=f"""Вы уже зафискированы за командой""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'TIME_CHD'

        def get_schedule_pm(update, context):
            filename = "Schedule"
            write_schedule(filename, pm=context.user_data["pm"])

            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            filepath = os.path.join(BASE_DIR, f"{filename}.xlsx")
            with open(filepath, 'rb') as file:
                update.effective_message.reply_document(
                    document=file,
                    caption=f"""Расписание""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'SCHEDULE_GET'

        def change_schedule_pm(update, context): pass  # <т. р.>

        def send_mailing_groups(update, context):
            successful = send_schedule(BOT, context.user_data["pm"])
            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if successful:
                update.effective_message.reply_text(
                    text=f"""Рассылка отправлена""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            else:
                update.effective_message.reply_text(
                    text=f"""Нет сформированных групп. Рассылка не выполнена""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'SEND_MAILING'

        def create_schedule(update, context):
            create_project_teams()
            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.effective_message.reply_text(
                text="""Обработка выполнена""",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            return 'SCHEDULE_CREATE'

        def get_schedule_admin(update, context):
            filename = "Schedule"
            write_schedule(filename)

            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            filepath = os.path.join(BASE_DIR, f"{filename}.xlsx")
            with open(filepath, 'rb') as file:
                update.effective_message.reply_document(
                    document=file,
                    caption=f"""Расписание""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'SCHEDULE_GET'

        def send_mailing(update, context):
            successful = send_schedule(BOT)
            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if successful:
                update.effective_message.reply_text(
                    text=f"""Рассылка отправлена""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            else:
                update.effective_message.reply_text(
                    text=f"""Нет сформированных групп. Рассылка не выполена""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            return 'SEND_MAILING'

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
                    CallbackQueryHandler(ch_time_student_4, pattern='ch_time_student_4'),
                    CallbackQueryHandler(ch_time_student_5, pattern='ch_time_student_5'),
                    CallbackQueryHandler(start_conversation, pattern='to_menu'),
                ],
                'CHG_TIME_STUDENT': [
                    CallbackQueryHandler(start_conversation, pattern='to_menu'),
                    CallbackQueryHandler(send_query, pattern='send_query'),
                    CallbackQueryHandler(chg_time_student_1, pattern='chg_time_student_1'),
                    CallbackQueryHandler(chg_time_student_2, pattern='chg_time_student_2'),
                    CallbackQueryHandler(chg_time_student_3, pattern='chg_time_student_3'),
                    CallbackQueryHandler(chg_time_student_4, pattern='chg_time_student_4'),
                    CallbackQueryHandler(chg_time_student_5, pattern='chg_time_student_5'),
                    CallbackQueryHandler(start_conversation, pattern='to_menu'),
                ],
                'TIME_CHD': [
                    CallbackQueryHandler(start_conversation, pattern='to_menu'),
                ],
                'SCHEDULE_GET': [
                    CallbackQueryHandler(start_conversation, pattern='to_menu'),
                ],
                'SCHEDULE_CREATE': [
                    CallbackQueryHandler(start_conversation, pattern='to_menu'),
                ],
                'SEND_MAILING': [
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


comm = Command()
comm.handle()
