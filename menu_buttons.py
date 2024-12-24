import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from constants import *
from keyboards import *
from test_db import get_user_from_db, update_user_in_db


async def main_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = 'Выберите опцию'
    if user_id in admins_id:
        user = await get_user_from_db(user_id)
        if user:
                await update_user_in_db(user_id, menu_state='Меню администратора')
        keyboard = admin_main_menu_keyboard
    else:
        await update_user_in_db(user_id, menu_state='Меню пользователя')
        keyboard = user_main_menu_keyboard
    # Создаем разметку клавиатуры
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Отправляем сообщение с кнопками
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)


async def show_admin_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Панель администратора')
    
    keyboard = admin_options_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите опцию', reply_markup=reply_markup)


async def show_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню вакансий')
    
    keyboard = vacancies_menu_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите вариант вакансий', reply_markup=reply_markup)


async def show_all_vacancies_sure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='SURE?')
    
    
    keyboard = warning_options_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    count = context.user_data['vacancies_count']
    
    warning_text = (
        'Внимание‼️\n\n'
        f'Актуальных вакансий сейчас: {count}\n\n'
        'Вы точно уверены, что хотите посмотреть все вакансии?')

    await update.message.reply_text(warning_text, reply_markup=reply_markup)


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню категорий')

    
    keyboard = vacancies_categories_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите нужную категорию', reply_markup=reply_markup)


async def show_power_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню вакансий ТЭЦ')
    
    
    keyboard = power_vacancies_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите нужную категорию', reply_markup=reply_markup)


async def show_office_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню вакансий офис')
    
    
    keyboard = office_vacancies_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите нужную категорию', reply_markup=reply_markup)


async def show_about_company(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='О компании')
    
    
    keyboard = about_company_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    

    await update.message.reply_text(company_text, reply_markup=reply_markup)


async def show_motivations_programms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Мотивационные программы')
    
    
    keyboard = motivations_programms_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    

    await update.message.reply_text('Выберите пункт', reply_markup=reply_markup)


async def show_FAQ(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Частые вопросы')
    
    
    keyboard = FAQ_keyboard
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите интересующий вопрос', reply_markup=reply_markup)

