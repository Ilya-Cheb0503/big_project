import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from constants import *

from test_db import get_user_from_db, update_user_in_db

async def main_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = 'Выберите опцию'
    if user_id in admins_id:
        user = await get_user_from_db(user_id)
        if user:
                await update_user_in_db(user_id, menu_state='Меню администратора')
                context.user_data['menu_state'] = 'Меню администратора'
                text = 'Выберите опцию'
        keyboard = [
                ['Вакансии'],
                ['О компании'],
                ['Частые вопросы'],
                ['Лист ожидания'],
                ['Контакты'],
                ['Панель администратора']
            ]
    else:
        context.user_data['menu_state'] = 'Меню пользователя'
        await update_user_in_db(user_id, menu_state='Меню пользователя')
        keyboard = [
                ['Вакансии'],
                ['О компании'],
                ['Частые вопросы'],
                ['Лист ожидания'],
                ['Контакты'],
            ]
    # Создаем разметку клавиатуры
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Отправляем сообщение с кнопками
    await update.message.reply_text(text, reply_markup=reply_markup)


async def show_admin_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Панель администратора')
    
    keyboard = [
        ['Рассылка'],
        ['Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите опцию', reply_markup=reply_markup)


async def show_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню вакансий')
    context.user_data['menu_state'] = 'Меню вакансий'
    if 'vacancies_proccess' in context.user_data:
        context.user_data.pop('vacancies_proccess')
    
    keyboard = [
        ['Посмотреть все вакансии'],
        ['Категории'],
        ['Вакансии без опыта'],
        ['Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите вариант вакансий', reply_markup=reply_markup)


async def show_all_vacancies_sure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='SURE?')
    
    
    keyboard = [
        ['Рискну'],
        ['Назад'],

    ]
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

    
    keyboard = [
        ['ТЭЦ'],
        ['Офис'],
        ['Стажировка'],
        ['Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите нужную категорию', reply_markup=reply_markup)


async def show_power_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню вакансий ТЭЦ')
    
    
    keyboard = [
        ['Теплоэнергетика', 'Электроэнергетика'],
        ['АСУ ТП', 'РЗА'],
        ['Ремонт', 'Химия'],
        ['HR', 'ИТ'],
        ['Экономика', 'Сбыт'],
        ['Промышленная безопасность и охрана труда'],
        ['Другое', 'Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите нужную категорию', reply_markup=reply_markup)


async def show_office_vacancies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Меню вакансий офис')
    
    
    keyboard = [
        ['Закупки', 'Экономика'],
        ['HR', 'Сбыт', 'ИТ'],
        ['Юриспруденция', 'Производственное управление'],
        ['Промышленная безопасность и охрана труда'],
        ['Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите нужную категорию', reply_markup=reply_markup)


async def show_about_company(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='О компании')
    
    
    keyboard = [
        ['Преимущества работы'],
        ['Филиалы'],
        ['Мотивационные и социальные программы'],
        ['Назад'],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    

    await update.message.reply_text(company_text, reply_markup=reply_markup)


async def show_motivations_programms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Мотивационные программы')
    
    
    keyboard = [
        ['Кадровый резерв'],
        ['Профессиональная подготовка и повышение квалификации за счет работодателя'],
        ['Соревнования профессионального мастерства'],
        ['Спортивные соревнования'],
        ['Корпоративные культурно-массовые мероприятия'],
        ['Совет молодых специалистов'],
        ['Назад'],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    

    await update.message.reply_text('Выберите пункт', reply_markup=reply_markup)


async def show_FAQ(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update_user_in_db(user_id, menu_state='Частые вопросы')
    
    
    keyboard = [
        ['💼 По какому графику я буду работать?'],
        ['💰 Какой уровень заработной платы мне ожидать?'],
        ['🏠 Какие компенсации существуют для иногородних кандидатов?'],
        ['🛡️ Какие социальные гарантии предоставляет Мосэнерго?'],
        ['📍 Адреса ТЭЦ Мосэнерго ГЭС-1'],
        ['👩‍🏫 На какие должности можно прийти без опыта?'],
        ['📝 Какие документы мне понадобятся при трудоустройстве?'],
        ['🚀 Есть ли в компании возможность карьерного роста?'],
        ['Назад'],

    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите интересующий вопрос', reply_markup=reply_markup)

