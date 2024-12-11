from dotenv import load_dotenv
import os

from time import sleep
import logging
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from settings import *
from menu_options import *
from menu_buttons import *
from functions import *
from constants import *

from test_db import User_tg, creat_user_in_db, get_user_from_db, update_user_in_db, start_create_table

# Хранение пользователей
admins_id = [787264207, 155771631]


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_id = update.effective_user.id
    query = update.callback_query
    # logging.info(f'КНОПКУ НАЖАЛИ\n{query}')
    await query.answer()  # Подтверждаем нажатие кнопки
    if query.data.__eq__('get_spec'):
        user = await get_user_from_db(user_id)
        user_inf = user['user_inf']
        if not user_inf['ФИО'] or not user_inf['Номер телефона']:
            context.user_data['запрос данных'] = True
            await context.bot.send_message(chat_id=user_id, text=inf_example_text, parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=user_id, text=inf_contacts_text, parse_mode='Markdown')
    # ФУНКЦИЯ РЕДАКТИРОВАНИЯ СОПРОВОДИТЕЛЬНОГО ПИСЬМА
    
    # Вызвать функцию отправки отклика, со всеми вытекающими:
    # Проверка : 1. Авторизован ли пользователь ? 2. Есть ли у него аккаунт для авторизации 3. Процесс авторизации при налиии такового 4. Повторное отправление отклика


    # logging.info(f'USER\n{context.user_data}')
    # new_keyboard = [
    #     # [InlineKeyboardButton("Отклик отправлен", callback_data=f'{vacancy_id}, Отклик отправлен')],
    #         [InlineKeyboardButton("Отклик отправлен", callback_data='Отклик отправлен')],
    #     ]
    # await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))


    # text = query.data[1]
    # Обрабатываем нажатие кнопки
    # await query.edit_message_text(text=f"Selected option: {query.data}", reply_markup=reply_markup)
    # await query.edit_message_text(text=f"{vacancy_id}\nВы откликнулись на вакансию\n{text_v}")
    # await query.answer(f'{text_v}')


# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await start_create_table()
    user_id = update.effective_user.id
    user = await get_user_from_db(user_id)
    if not user:
        await creat_user_in_db(user_id)
    
    # if admin_authenticated.get(user_id, False):
    if user_id in admins_id:
        await update_user_in_db(user_id, menu_state='Меню администратора')
        text = welcome_text 

        keyboard = [
            ['Вакансии'],
            ['О компании'],
            ['Частые вопросы'],
            ['Лист ожидания'],
            ['Контакты'],
            ['Панель администратора']
        ]
        
        # Создаем разметку клавиатуры
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        # Отправляем сообщение с кнопками
        await update.message.reply_text(text, reply_markup=reply_markup)

        sleep(0.5)
        await context.bot.send_message(chat_id=user_id, text=welcome_two, parse_mode='Markdown')

    else:
        await update_user_in_db(user_id, menu_state='Меню пользователя')

        keyboard = [
            ['Вакансии'],
            ['О компании'],
            ['Частые вопросы'],
            ['Лист ожидания'],
            ['Контакты']
        ]
        
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


    elif 'запрос данных' in context.user_data:
        await ask_user_inf(user_id, current_text)
        context.user_data.pop('запрос данных')
        await context.bot.send_message(chat_id=user_id, text=inf_contacts_text, parse_mode='Markdown')

    else:
        current_menu = menu_list[menu_state]
        await current_menu(current_text, update, context)


async def main(telegram_bot_token) -> None:
    
    nest_asyncio.apply()

    application = Application.builder().token(telegram_bot_token).build()

    # Регистрируем обработчики команд и сообщений
    application.add_handler(CommandHandler('start', start))
    # application.add_handler(CommandHandler('buttons', send_inline_buttons))
    application.add_handler(CallbackQueryHandler(button_callback))  # Добавляем обработчик для инлайн кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND | filters.PHOTO, button_handler))
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
        