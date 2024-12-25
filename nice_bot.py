import asyncio
import logging
import os
from functools import partial
from time import sleep

import nest_asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (Application, ApplicationBuilder,
                          CallbackQueryHandler, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from bd_update import create_rename_and_delete
from constants import *
from functions import *
from keyboards import *
from menu_buttons import *
from menu_options import *
from new_module import *
from settings import *
from test_db import (User_tg, creat_user_in_db, get_user_from_db,
                     start_create_table, update_user_in_db)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    user = await get_user_from_db(user_id)
    user_inf = user['user_inf']
    user_name = user_inf['ФИО']

    list_keys = [
    'Запрос full данных',
    'Запрос анкетных данных',
    'information_form',
    'message_inf',
    'message_state',
    'current_text',
    'photo_path',
    'pdf_path',
    'vacancy_name',

]
    if query.data.__eq__('main_menu'):
        for key in list_keys:
            if key in context.user_data:
                context.user_data.pop(key)
        await main_start_menu(update, context)

    elif 'tq' in query.data:
        vac_id = query.data.split(';')[1]
        int_id = int(vac_id)
        vacancy = await get_vacancy_by_vacancy_id(int_id)
        vacancy_name = vacancy.vacancy_inf['Вакансия']
        context.user_data['vacancy_name'] = vacancy_name
        context.user_data['Запрос анкетных данных'] = 'Запуск анкетирования'
        await user_form_information_process(update, context)

    elif not user_inf['ФИО'] or not user_inf['Номер телефона']:
        context.user_data['Запрос анкетных данных'] = 'Запуск анкетирования'
        await user_full_information_process(update, context)

    elif query.data.__eq__('get_spec'):
        await context.bot.send_message(chat_id=user_id, text=inf_contacts_text, parse_mode='Markdown')

    else:
        
        int_id = int(query.data)
        vacancy = await get_vacancy_by_vacancy_id(int_id)
        vacancy_url = vacancy.vacancy_inf['Ссылка на вакансию']
        vacancy_name = vacancy.vacancy_inf['Вакансия']

        user_send_req_text = (
            f'Пользователь: {user_name}\n'
            f'Откликнулся на вакансию: {vacancy_name}'
        )

        await context.bot.send_message(chat_id=group_id, text=user_send_req_text)

        # Создаем новую кнопку с URL
        keyboard = [
        [
            InlineKeyboardButton("Откликнуться", callback_data=f'tq;{int_id}')
        ],

        [
            InlineKeyboardButton("Ссылка на вакансию", callback_data='req_button', url=vacancy_url)
        ],

        [
            InlineKeyboardButton("Получить консультацию специалиста 📞", callback_data='get_spec')
        ],
        ]

        # Создаем разметку для кнопок
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Обновляем сообщение с новой клавиатурой
        await context.bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=reply_markup)


        # await context.bot.send_message(query.from_user.id, "https://example.com")
        vacancion_name = query.data.split(';')[1]
        user = await get_user_from_db(user_id)
        user_inf = user['user_inf']
        user_name = user_inf['ФИО']
        logging.info(f'IMPOOOOORTANT {vacancion_name}')
        note_text = f'Пользователь: {user_name}\nОткликнулся на вакансию: {vacancion_name}'
        if 'ФИО' and 'Образование' in user_inf:
            logging.info(f'SEEEENDING {vacancion_name}')
            await context.bot.send_message(chat_id=group_id, text=note_text, parse_mode='HTML')


# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await start_create_table()
    if 'Запрос full данных' in context.user_data:
        context.user_data.pop('Запрос full данных')

    if 'Запрос анкетных данных' in context.user_data:
        context.user_data.pop('Запрос анкетных данных')

    user_id = update.effective_user.id
    user = await get_user_from_db(user_id)
    if not user:
        await creat_user_in_db(user_id)
    
    # if admin_authenticated.get(user_id, False):
    if user_id in admins_id:
        await update_user_in_db(user_id, menu_state='Меню администратора')
        text = welcome_text 

        keyboard = admin_main_menu_keyboard
        
        # Создаем разметку клавиатуры
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        # Отправляем сообщение с кнопками
        await update.message.reply_text(text, reply_markup=reply_markup)

        sleep(0.5)
        await context.bot.send_message(chat_id=user_id, text=welcome_two, parse_mode='Markdown')

    else:
        await update_user_in_db(user_id, menu_state='Меню пользователя')

        keyboard = user_main_menu_keyboard
        
        # Создаем разметку клавиатуры
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
        # Отправляем сообщение с кнопками
    
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

        sleep(0.5)
        await context.bot.send_message(chat_id=user_id, text=welcome_two, parse_mode='Markdown')


# Функция для обработки нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    current_text = update.message.text
    user_id = update.effective_user.id
    user = await get_user_from_db(user_id)
    if user:
        menu_state = user['menu_state']

    logging.info(f'inf: {current_text}, {menu_state}')
    menu_list = {
    'Меню пользователя': user_main_menu,
    'Меню администратора': admin_main_menu,
    'Панель администратора': admin_options_menu,
    'Меню вакансий': vacancies_menu,
    'SURE?': vacancies_menu,
    'Меню категорий': categories_menu,
    'Меню вакансий ТЭЦ': power_vacancies_menu,
    'Меню вакансий офис': office_vacancies_menu,
    'О компании': about_company_menu,
    'Мотивационные программы': motivations_programms_menu,
    'Частые вопросы': FAQ_menu,
}
    if 'Запрос full данных' in context.user_data:
        await list_waiting(update, context)
    

    elif 'Запрос анкетных данных' in context.user_data:
        await user_form_information_process(update, context)


    # elif 'запрос данных' in context.user_data:
    #     await ask_user_inf(user_id, current_text)
    #     context.user_data.pop('запрос данных')
    #     await context.bot.send_message(chat_id=user_id, text=inf_contacts_text, parse_mode='Markdown')

    else:
        current_menu = menu_list[menu_state]
        await current_menu(current_text, update, context)
    
    await extra_inline_button(update, context)


async def db_update_task(update, context):
    logging.info('ЗАПУСКАЕМ расписание обновления БД')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(create_rename_and_delete, 'cron', hour=0, minute=0)  # Запрашиваем события каждую полночь
    scheduler.start()
    logging.info('ЗАПУСТИЛИ расписание обновления БД')


async def main(telegram_bot_token) -> None:
    
    nest_asyncio.apply()

    application = Application.builder().token(telegram_bot_token).build()

    # Регистрируем обработчики команд и сообщений
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('developer_hand', db_update_task))
    # application.add_handler(CommandHandler('buttons', send_inline_buttons))
    application.add_handler(CallbackQueryHandler(button_callback))  # Добавляем обработчик для инлайн кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND | filters.PHOTO | filters.Document.ALL, button_handler))
      # Обработчик для инлайн кнопок

    # Запускаем бота
    logging.info('Бот запущен')
    try:
        # Запускаем бота
        await application.run_polling()
    except (KeyboardInterrupt, SystemExit):
        # Обрабатываем исключения, чтобы избежать вывода в терминал
        logging.error(f"Бот остановлен", exc_info=True)
        await application.stop()
    

if __name__ == '__main__':
    
    try:
        load_dotenv()
        telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    except Exception as er:
        logging.error(f'Не получилось получить токен телеграм бота.\n{er}\nПроверьте наличие .env')

    asyncio.run(main(telegram_bot_token))
        