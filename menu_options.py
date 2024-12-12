import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from nice_bot import send_messages, admins_id
from functions import *
from constants import *
from menu_buttons import *


async def user_main_menu(button_text, update, context):
        button_text_options = {
            'Вакансии': show_vacancies,
            'О компании': show_about_company,
            'Частые вопросы': show_FAQ,
            'Лист ожидания': list_waiting,
            'Контакты': contacts,
        }
        if 'Запрос full данных' in context.user_data:
            await list_waiting(update, context)
        elif button_text not in button_text_options:
            if button_text.lower().__eq__('без опыта'):
                logging.info('БЕЗ ОПЫТА')
                await get_no_exp_vacancies(update, context)
            else:
                await get_vacancies_by_key_word(update, context, button_text)
        else:
            current_option = button_text_options[button_text]
            await current_option(update, context)


async def admin_main_menu(button_text, update, context):
        button_text_options = {
            'Вакансии': show_vacancies,
            'О компании': show_about_company,
            'Частые вопросы': show_FAQ,
            'Лист ожидания': list_waiting,
            'Контакты': contacts,
            'Панель администратора': show_admin_options
        }
        if 'Запрос full данных' in context.user_data:
            await list_waiting(update, context)
        elif button_text not in button_text_options:
            if button_text.lower().__eq__('без опыта'):
                logging.info('БЕЗ ОПЫТА')
                await get_no_exp_vacancies(update, context)
            else:
                await get_vacancies_by_key_word(update, context, button_text)
        else:
            current_option = button_text_options[button_text]
            await current_option(update, context)


async def admin_options_menu(button_text, update, context):
    logging.info('admin options')
    
    button_text_options = {
        'Рассылка': send_messages,
        'Главное меню': main_start_menu,
    }
    
    if 'message_state' not in context.user_data:
        current_option = button_text_options[button_text]
        logging.info(f'current admin option = {current_option}')
        await current_option(update, context)
    elif 'message_state' in context.user_data:
        await send_messages(update, context)


async def vacancies_menu(button_text, update, context):
    button_text_options = {
        'Посмотреть все вакансии': None,
        'Категории': show_categories,
        'Вакансии без опыта': get_no_exp_vacancies,
        'Главное меню': main_start_menu
    }

    # current_option = button_text_options[button_text]
    # await current_option(update, context)
    if 'a_lot_of_vacancies' in context.user_data:
        context.user_data.pop('a_lot_of_vacancies')
        if button_text.__eq__('Рискну'):
            await get_all_company_vacancies(update, context)
            
        else:
            await show_vacancies(update, context)
    
    elif button_text.__eq__('Посмотреть все вакансии'):
        context.user_data['a_lot_of_vacancies'] = True
        vacancies_count = await get_vacancy_count()
        context.user_data['vacancies_count'] = vacancies_count
        await show_all_vacancies_sure(update, context)
        

    elif 'vacancies_proccess' in context.user_data:
        await get_vacancies_proccess(update, context)
    elif type(button_text_options[button_text]) == str:
        await update.message.reply_text(button_text_options[button_text])
        
    else:
        current_option = button_text_options[button_text]
        await current_option(update, context)


async def categories_menu(button_text, update, context):
    button_text_options = {
        'ТЭЦ': show_power_vacancies,
        'Офис': show_office_vacancies,
        'Главное меню': main_start_menu
    }

    # current_option = button_text_options[button_text]
    # await current_option(update, context)
    if button_text.__eq__('Стажировка'):
        await get_vacancies_by_key_word(update, context, key_word='Стажор')
        
    else:
        current_option = button_text_options[button_text]
        await current_option(update, context)


async def power_vacancies_menu(button_text, update, context):
    vacancies_options = [
        'Теплоэнергетика', 'Электроэнергетика', 'АСУ ТП',
        'РЗА', 'Ремонт', 'Химия', 'HR', 'ИТ', 'Экономика', 'Сбыт',
        'Промышленная безопасность и охрана труда', 'Другое'
    ]

    if button_text.__eq__('Главное меню'):
        await main_start_menu(update, context)
    elif button_text in energy_vacancy_keys:
        await get_vacancies_by_keys_list(update, context, energy_vacancy_keys[button_text])
    else:
        await update.message.reply_text('Такой опции нет')


async def office_vacancies_menu(button_text, update, context):
    vacancies_options = [
        'Закупки', 'Экономика','HR', 'Сбыт', 'ИТ',
        'Юриспруденция', 'Производственное управление',
        'Промышленная безопасность и охрана труда'
        ]

    if button_text.__eq__('Главное меню'):
        await main_start_menu(update, context)
    elif button_text in ofice_vacancy_keys:

        await get_vacancies_by_keys_list(update, context, ofice_vacancy_keys[button_text])
        pass # Вызов поиска вакансий по ключевым словам
    else:
        await update.message.reply_text('Такой опции нет')


async def about_company_menu(button_text, update, context):
    button_text_options = {
        'Преимущества работы в ПАО «Мосэнерго»': company_benefit,
        'Филиалы': company_filiales,
        'Мотивационные и социальные программы': show_motivations_programms,
        'Главное меню': main_start_menu
    }

    current_option = button_text_options[button_text]
    if type(current_option) == str:
        await update.message.reply_text(current_option)
    else:
        await current_option(update, context)


async def motivations_programms_menu(button_text, update, context):
    button_text_options = {
        'Кадровый резерв': motivations_programms[0],
        'Профессиональная подготовка и повышение квалификации за счет работодателя': motivations_programms[1],
        'Соревнования профессионального мастерства': motivations_programms[2],
        'Спортивные соревнования': motivations_programms[3],
        'Корпоративные культурно-массовые мероприятия': motivations_programms[4],
        'Совет молодых специалистов': motivations_programms[5],
        'Главное меню': main_start_menu,
    }

    current_option = button_text_options[button_text]
    if type(current_option) == str:
        await update.message.reply_text(current_option)
    else:
        await current_option(update, context)


async def FAQ_menu(button_text, update, context):
    button_text_options = {
        '💼 По какому графику я буду работать?': FAQ[0],
        '💰 Какой уровень заработной платы мне ожидать?': FAQ[1],
        '🏠 Какие компенсации существуют для иногородних кандидатов?': FAQ[2],
        '🛡️ Какие социальные гарантии предоставляет Мосэнерго?': FAQ[3],
        '📍 Адреса ТЭЦ Мосэнерго ГЭС-1': FAQ[4],
        '👩‍🏫 На какие должности можно прийти без опыта?': FAQ[5],
        '📝 Какие документы мне понадобятся при трудоустройстве?': FAQ[6],
        '🚀 Есть ли в компании возможность карьерного роста?': FAQ[7],
        'Главное меню': main_start_menu

    }
    
    current_option = button_text_options[button_text]
    if type(current_option) == str:
        await update.message.reply_text(current_option, parse_mode='HTML')
    else:
        await current_option(update, context)


async def list_waiting(update, context):
    current_text = update.message.text
    text_wait = (
        'Если вы не нашли подходящей вакансии, предлагаем заполнить\n'
        'небольшую форму и мы сообщим Вам в числе первых, когда\n'
        'подходящая вакансия появится!'
    )
    if 'Запрос full данных' not in context.user_data:
        await update.message.reply_text(text_wait)
        context.user_data['Запрос full данных'] = 'Старт'
        context.user_data['information_form'] = {}
    await user_full_information_process(update, context, current_text)

async def contacts(update, context):
    await update.message.reply_text(contacts_info)
