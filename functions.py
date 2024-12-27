import json
import logging
import os
import re
from time import sleep

import requests
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import ContextTypes

from constants import *
from menu_buttons import *
from new_module import *
from test_db import *


async def check_user_inf(user_id):
    user = await get_user(user_id)
    user_inf = user['user_inf']
    if 'ФИО' and 'Образование' in user_inf:
        return True
    return False
    

async def ask_user_inf(user_id, user_inf):
    user_name, user_phone = re.split(r'[;,]', user_inf)
    user_inf_params = {'ФИО': user_name, 'Номер телефона': user_phone}
    await update_user_in_db(user_id, user_inf=user_inf_params)


async def user_form_information_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = await get_user(user_id)
    user_inf_db = user['user_inf']

    if 'information_form' not in context.user_data:
        context.user_data['information_form'] = {}
    user_inf = context.user_data['information_form']
    try:
        current_text = update.message.text
    except Exception:
        current_text = None
        context.user_data['Запрос анкетных данных'] = 'Запуск анкетирования'

    
    step = {
        'Запуск анкетирования': ('check', None),
        'check': ('ФИО', None),
        'ФИО': ('Резюме вопрос', 'Хотите прикрепить резюме?'),
        'Резюме вопрос': ('Проверка pdf файла', 'Пожалуйста, пришлите ваше резюме в формате .pdf'),
        'Проверка pdf файла': ('Проверка анкеты', None),

        # 'Успешная загрузка резюме': ('Проверка анкеты', None),

        'Проверка анкеты': ('Утверждение найденной анкеты', None),
        'Утверждение найденной анкеты': ('done', None),
        'Доп резюме вопрос': ('Доп pdf файл', None),
        'Доп pdf файл': ('Резюме', None),
        
        'Резюме': ('Номер телефона', 'Ваш контактный номер телефона:'),
        'Номер телефона': ('Должность', 'Желаемая должность:'),
        'Должность': ('Опыт работы', 'Ваш стаж:'),
        'Опыт работы': ('Образование', 'Ваш уровень образования:'),
        'Образование': ('Подтверждение', None),
        'Подтверждение': ('done', None),
        'done': (None, None)
    }
    save_steps = [
        'ФИО', 'Номер телефона', 'Должность', 'Опыт работы', 'Образование'
        ]

    current_step = context.user_data['Запрос анкетных данных']

    if current_text == 'Главное меню' or current_text == 'Назад':
        context.user_data.pop('Запрос анкетных данных')
        await main_start_menu(update, context)
        return 
    
    if current_step in save_steps:
        context.user_data['information_form'][current_step] = current_text
        await update_user_in_db(user_id, user_inf={current_step:current_text})

    
    # ПОДУМАТЬ О ТОМ ЧТОБЫ ПЕРЕНЕСТИ ДВЕ СТРОКИ, КОТОРЫЕ НИЖЕ И ИЗМЕНИТЬ ПРОВЕРКУ
    # проверять соответствие не СЛЕДУЮЩЕГО шага, а ТЕКУЩЕГО
    next_step, message_text = step[current_step]
    context.user_data['Запрос анкетных данных'] = next_step

    if current_step.__eq__('Запуск анкетирования'):
        text_wait = (
        'Просто отвечайте на вопросы бота,\nа он бережно соберет Ваши данные в анкету 📠'
    )

        keyboard = [
            ['Согласен с политикой обработки персональных данных ✅'],
            ['Назад']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text_wait, reply_markup=reply_markup)

    elif next_step.__eq__('ФИО'):
        text = 'Для начала укажите в сообщении ваши ФИО:'
        keyboard = [
            ['Назад']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

    elif next_step.__eq__('Резюме вопрос'):
        text = 'Хотите прикрепить резюме?'
        keyboard = [
                ['Да'],
                ['Нет'],
            ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

    elif current_step.__eq__('Резюме вопрос'):
        
        if current_text.__eq__('Да'):
            context.user_data['Запрос анкетных данных'] = 'Проверка pdf файла'
            text = 'Пожалуйста, пришлите ваше резюме в формате .pdf'
            keyboard = [
                ['Главное меню'],
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(text, reply_markup=reply_markup)

        elif current_text.__eq__('Нет'):
            if 'Образование' in user_inf_db:
                message_text = 'У нас уже есть ваши данные,\nможем использовать их в отклике\nили хотите заполнить анкету заново?'
                keyboard = [
                    ['Продолжить с моими данными'],
                    ['Заполнить заново']
                ]
                context.user_data['Запрос анкетных данных'] = 'Утверждение найденной анкеты'
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                await update.message.reply_text(message_text, reply_markup=reply_markup)
            else:
                context.user_data['Запрос анкетных данных'] = 'Номер телефона'
                text = 'Ваш контактный номер телефона:'
                keyboard = [
                    ['Главное меню'],
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                await update.message.reply_text(text, reply_markup=reply_markup)

    elif current_step.__eq__('Проверка pdf файла'):
        document = update.message.document
        file_name = document.file_name
        if not file_name.lower().endswith('.pdf'):
            update.message.reply_text('Ошибка: файл должен быть в формате PDF.')
            
            context.user_data['Запрос анкетных данных'] = 'Проверка pdf файла'
            
        # Получаем файл
        new_file = await context.bot.get_file(document.file_id)
        file_path = f"{downloads_path}/{file_name}.pdf"
        context.user_data['pdf_path'] = file_path
        await new_file.download_to_drive(file_path)

        text = 'Резюме успешно загруженно. Желаете продолжить заполнение данных?'
        keyboard = [
                ['Продолжить'],
                ['Назад']
            ]
        context.user_data['Запрос анкетных данных'] = 'Проверка анкеты'
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)

    elif current_step.__eq__('Доп резюме вопрос'):
        
        if current_text.__eq__('Да'):
            context.user_data['Запрос анкетных данных'] = 'Доп pdf файл'
            text = 'Пожалуйста, пришлите ваше резюме в формате .pdf'
            keyboard = [
                ['Главное меню'],
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(text, reply_markup=reply_markup)

        elif current_text.__eq__('Нет'):
            context.user_data['Запрос анкетных данных'] = 'Номер телефона'
            text = 'Ваш контактный номер телефона:'
            keyboard = [
                ['Главное меню'],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(text, reply_markup=reply_markup)
    

    elif current_step.__eq__('Доп pdf файл'):
        document = update.message.document
        file_name = document.file_name
        if not file_name.lower().endswith('.pdf'):
            update.message.reply_text('Ошибка: файл должен быть в формате PDF.')
            
            context.user_data['Запрос анкетных данных'] = 'Доп pdf файл'
            
        # Получаем файл
        new_file = await context.bot.get_file(document.file_id)
        file_path = f"{downloads_path}/{file_name}.pdf"
        context.user_data['pdf_path'] = file_path
        await new_file.download_to_drive(file_path)

        text = 'Резюме успешно загруженно.\nУкажите Ваш контактный номер телефона:'
        context.user_data['Запрос анкетных данных'] = 'Номер телефона'
        keyboard = [
            ['Главное меню'],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
    


    elif current_step.__eq__('Проверка анкеты'):

        if 'Образование' in user_inf_db:
            message_text = 'У нас уже есть ваши данные,\nможем использовать их в отклике\nили хотите заполнить анкету заново?'
            keyboard = [
                ['Продолжить с моими данными'],
                ['Заполнить заново']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        else:
            context.user_data['Запрос анкетных данных'] = 'Номер телефона'
            text = 'Ваш контактный номер телефона:'
            keyboard = [
                ['Главное меню'],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(text, reply_markup=reply_markup)

    elif current_step.__eq__('Утверждение найденной анкеты'):
        ch = current_text.__eq__('Продолжить с моими данными')
        logging.info(f'Утверждение: {current_text} and {ch}')
        if current_text.__eq__('Продолжить с моими данными'):
            context.user_data.pop('Запрос анкетных данных')
            
            final_text = (
                'Спасибо, что откликнулись! ☺️ Наши специалисты свяжутся с вами в течение 7 дней.\n\n'
                'Если вам не терпится связаться с нами, то напишите нам на почту rabota@mosenergo.ru\n\n'
                'Или позвоните по номеру +7 (495) 957-19-57, доб. 4006'
            )
            user_inf = user['user_inf']
            user_name = user_inf['ФИО']
            vacancion_name = context.user_data['vacancy_name']
            note_text = f'Пользователь: {user_name}\nОткликнулся на вакансию: {vacancion_name}'
            

            await update.message.reply_text(final_text)
            await context.bot.send_message(chat_id=group_id, text=note_text)
            
            if 'pdf_path' in context.user_data:
                pdf_path = context.user_data['pdf_path']
                await send_pdf(update, context, pdf_path=pdf_path, chat_id=group_id, user_name=user_name)
            await main_start_menu(update, context)

        elif current_text.__eq__('Заполнить заново'):


            context.user_data['Запрос анкетных данных'] = 'Доп резюме вопрос'
            text = 'Хотите прикрепить резюме?'
            keyboard = [
                    ['Да'],
                    ['Нет'],
                ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)


            # context.user_data['Запрос анкетных данных'] = 'Номер телефона'
            # text = 'Ваш контактный номер телефона:'
            # keyboard = [
            #     ['Главное меню'],
            # ]
            # reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            # await update.message.reply_text(text, reply_markup=reply_markup)


    elif next_step.__eq__('Должность'):
        text = 'Желаемая должность:'
        keyboard = [
                ['Главное меню'],
            ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

    elif next_step.__eq__('Опыт работы'):
        text = 'Ваш стаж:'
        keyboard = [
        ['менее 1 года'],
        ['1-2 года'],
        ['2-3 года'],
        ['3+ лет']
        
    ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)


    elif next_step.__eq__('Образование'):
        text = 'Ваш уровень образования:'
        keyboard = [
        ['Высшее образование'],
        ['Среднее профессиональное'],
        ['Школьное'],

    ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    elif next_step.__eq__('Подтверждение'):
        keyboard = [
        ['Всё верно!✅'],
        ['Редактировать'],
        ]
        user_inf = context.user_data['information_form']
        full_name = user_inf['ФИО']
        phone = user_inf['Номер телефона']
        work = user_inf['Должность']
        exp = user_inf['Опыт работы']
        educ = user_inf['Образование']
        
        user_bio = (
            f'<b>ФИО:</b>\n{full_name}\n\n'
            f'<b>Номер телефона:</b>\n{phone}\n\n'
            f'<b>Должность:</b>\n{work}\n\n'
            f'<b>Опыт работы:</b>\n{exp}\n\n'
            f'<b>Образование:</b>\n{educ}\n\n'
            )
        logging.info(user_bio)
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(user_bio, reply_markup=reply_markup, parse_mode='HTML')
    
    elif current_step.__eq__('Подтверждение'):
        if current_text.__eq__('Всё верно!✅'):
            context.user_data.pop('Запрос анкетных данных')
            
            user_inf = context.user_data['information_form']
            full_name = user_inf['ФИО']
            phone = user_inf['Номер телефона']
            work = user_inf['Должность']
            exp = user_inf['Опыт работы']
            educ = user_inf['Образование']
            final_text = (
                'Спасибо, что откликнулись! ☺️ Наши специалисты свяжутся с вами в течение 7 дней.\n\n'
                'Если вам не терпится связаться с нами, то напишите нам на почту rabota@mosenergo.ru\n\n'
                'Или позвоните по номеру +7 (495) 957-19-57, доб. 4006'
            )
            await context.bot.send_message(chat_id=user_id, text=final_text, parse_mode='Markdown')

            user_inf = user['user_inf']
            user_name = user_inf['ФИО']
            vacancion_name = context.user_data['vacancy_name']
            note_text = f'Пользователь: {user_name}\nОткликнулся на вакансию: {vacancion_name}'

            await context.bot.send_message(chat_id=group_id, text=note_text)
            if 'pdf_path' in context.user_data:
                pdf_path = context.user_data['pdf_path']
                await send_pdf(update, context, pdf_path=pdf_path, chat_id=group_id, user_name=user_name)
            await main_start_menu(update, context)

        else:
            context.user_data['Запрос анкетных данных'] = 'ФИО'
            keyboard = [
                ['Главное меню'],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text('Тогда начнем сначала.\nУкажите ваши ФИО:', reply_markup=reply_markup)


async def user_full_information_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_text = update.message.text
    user_id = update.effective_user.id
    step = {
        'Запуск анкетирования': ('Старт', 'Просто отвечайте на вопросы бота,\nа он бережно соберет Ваши данные в анкету 📠'),
        # 'Утверждение запуска': ('Старт', None),
        'Старт': ('ФИО','Для начала укажите в сообщении ваши ФИО:'),
        'ФИО': ('Номер телефона', 'Ваш контактный номер телефона:'),
        'Номер телефона': ('Должность', 'Желаемая должность:'),
        'Должность': ('Опыт работы', 'Ваш стаж:'),
        'Опыт работы': ('Образование', 'Ваш уровень образования:'),
        'Образование': ('Подтверждение', None),
        'Подтверждение': ('done', 'Ура, ваша анкета уже у нас! Спасибо за Ваше время, мы Вас не подведем!\nЕсли Вам не хочется ждать, Вы можете позвонить нам напрямую: +7 495 957-19-57'),
        'done': (None, None)
    }

    save_steps = [
        'ФИО', 'Номер телефона', 'Должность', 'Опыт работы', 'Образование'
        ]
    current_step = context.user_data['Запрос full данных']
    
    logging.info(f'current_text = {current_text}')
    if current_text == 'Главное меню' or current_text == 'Назад':
        context.user_data.pop('Запрос full данных')
        await main_start_menu(update, context)
        return

    if current_step in save_steps:
        context.user_data['information_form'][current_step] = current_text
        await update_user_in_db(user_id, user_inf={current_step:current_text})
    
    # ПОДУМАТЬ О ТОМ ЧТОБЫ ПЕРЕНЕСТИ ДВЕ СТРОКИ, КОТОРЫЕ НИЖЕ И ИЗМЕНИТЬ ПРОВЕРКУ
    # проверять соответствие не СЛЕДУЮЩЕГО шага, а ТЕКУЩЕГО
    next_step, message_text = step[current_step]
    context.user_data['Запрос full данных'] = next_step
    
    
    if current_step.__eq__('Запуск анкетирования'):
        text = 'Просто отвечайте на вопросы бота,\nа он бережно соберет Ваши данные в анкету 📠'
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        keyboard_cancel = [
            ['Продолжить'],
            ['Назад']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard_cancel, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

    
    elif next_step.__eq__('ФИО'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Для начала укажите в сообщении ваши ФИО:'
        if current_text.__eq__('Продолжить'):
            keyboard = [
            ['Главное меню'],
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(text, reply_markup=reply_markup)
    

    elif next_step.__eq__('Номер телефона'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Ваш контактный номер телефона:'
        keyboard = [
        ['Главное меню'],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
    

    elif next_step.__eq__('Должность'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Желаемая должность:'
        keyboard = [
            ['Главное меню'],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
    

    elif next_step.__eq__('Опыт работы'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Ваш стаж:'
        keyboard = [
        ['менее 1 года'],
        ['1-2 года'],
        ['2-3 года'],
        ['3+ лет']
        
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    elif next_step.__eq__('Образование'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Ваш уровень образования:'
        keyboard = [
        ['Высшее образование'],
        ['Среднее профессиональное'],
        ['Школьное'],

    ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text, reply_markup=reply_markup)


    elif next_step.__eq__('Подтверждение'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        keyboard = [
        ['Всё верно!✅'],
        ['Редактировать'],
        ]

        user_inf = context.user_data['information_form']
        full_name = user_inf['ФИО']
        phone = user_inf['Номер телефона']
        work = user_inf['Должность']
        exp = user_inf['Опыт работы']
        educ = user_inf['Образование']
        
        user_bio = (
            f'<b>ФИО:</b>\n{full_name}\n\n'
            f'<b>Номер телефона:</b>\n{phone}\n\n'
            f'<b>Должность:</b>\n{work}\n\n'
            f'<b>Опыт работы:</b>\n{exp}\n\n'
            f'<b>Образование:</b>\n{educ}\n\n'
            )
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(user_bio, reply_markup=reply_markup, parse_mode='HTML')

    elif current_step.__eq__('Подтверждение'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        if current_text.__eq__('Всё верно!✅'):
            context.user_data.pop('Запрос full данных')
            
            user_inf = context.user_data['information_form']
            full_name = user_inf['ФИО']
            phone = user_inf['Номер телефона']
            work = user_inf['Должность']
            exp = user_inf['Опыт работы']
            educ = user_inf['Образование']
            
            user_bio_notice = (
            f'Пользователь: {full_name}\n'
            'Заполнил анкету персональных данных.\n\n'
            f'<b>Номер телефона:</b>\n{phone}\n'
            f'<b>Должность:</b>\n{work}\n'
            f'<b>Опыт работы:</b>\n{exp}\n'
            f'<b>Образование:</b>\n{educ}\n'
            )
            
            await context.bot.send_message(chat_id=user_id, text=message_text, parse_mode='Markdown')
            await context.bot.send_message(chat_id=group_id, text=user_bio_notice, parse_mode='HTML')
            await main_start_menu(update, context)

        else:
            context.user_data['Запрос full данных'] = 'ФИО'
            keyboard = [
                ['Главное меню'],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text('Тогда начнем сначала.\nУкажите ваши ФИО:', reply_markup=reply_markup)

    logging.info(f'ЗАВЕРШАЕМ РАБОТУ ФУНКЦИИ с шагом {current_step} а текст сообщения {current_text}')
    

async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info('send process')
    # Запрос текста сообщения от пользователя
    message_creator = {
        'Creating' : message_text_getting,
        'Edited' : message_text_confirmation,
        'Completed' : message_text_sending
    }
    if 'message_state' not in context.user_data:
        context.user_data['message_state'] = 'Creating'
    current_message_state = context.user_data.get('message_state')

    current_step = message_creator[current_message_state]

    await current_step(update, context)


async def message_text_getting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logging.info('edit process')
    context.user_data['message_text'] = None

    await update.message.reply_text('Пришлите мне сообщение, которое хотите разослать:', reply_markup=ReplyKeyboardRemove())

    context.user_data['message_state'] = 'Edited'

async def message_text_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    logging.info('confirm process')
    user_id = update.effective_user.id
    message_text, image_path = await download_message_with_image(update, context)
    context.user_data['message_inf'] = (message_text, image_path)
    
    keyboard = [
        ['Да'],
        ['Нет']
        
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Вы хотите отправить следующее сообщение?', reply_markup=reply_markup)
    await forward_message_with_image(update, context, message_text, image_path, user_id)
    context.user_data['message_state'] = 'Completed'


async def message_text_sending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        ['Рассылка'],
        ['Главное меню']
    ]

    message_text = update.message.text
    if message_text == 'Да':
        current_message_text, image_path = context.user_data.get('message_inf')
        users = await get_all_users()  # Получаем всех пользователей
        users_id = [user['telegram_id'] for user in users]

        for user_id in users_id:
            try:
                await forward_message_with_image(update, context, current_message_text, image_path, user_id)
            except Exception as error:
                logging.exception(f"Не удалось отправить сообщение пользователю {user_id}: {error}")

        context.user_data.pop('message_state')
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text('Рассылка завершена.', reply_markup=reply_markup)

    elif message_text == 'Нет':
        context.user_data['message_state'] = 'Creating'
        await message_text_getting(update, context)
    

async def download_message_with_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем текст сообщения
    # message_text = context.user_data.get('current_text')
    message_text = update.message.text
    file_path = None

    if update.message.photo:
        message_text = update.message.caption
        context.user_data['current_text'] = message_text
        photo = update.message.photo[-1]  # Получаем самое высокое качество изображения
        file = await photo.get_file()
        file_path = f"{downloads_path}/{photo.file_id}.jpg"
        context.user_data['photo_path'] = file_path  # Путь для сохранения изображения
        await file.download_to_drive(file_path)

        return message_text, file_path

    else:
        # Если изображения нет, просто отправляем текст
        return message_text, file_path


async def forward_message_with_image(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text, image_path, user_id) -> None:
    
    # Проверяем, есть ли вложение (изображение)
    if image_path:

        # Отправляем новое сообщение с изображением и текстом
        with open(image_path, 'rb') as img_file:
            await context.bot.send_photo(chat_id=user_id, photo=img_file, caption=message_text, parse_mode='Markdown')
    else:
        # Если изображения нет, просто отправляем текст
        await context.bot.send_message(chat_id=user_id, text=message_text, parse_mode='Markdown')


async def get_vacancy_count():
    employer_id = '27708'
    url = f'https://api.hh.ru/vacancies?employer_id={employer_id}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Получаем общее количество вакансий
        total_vacancies = data['found']
        return total_vacancies
    else:
        logging.error(f"Ошибка при запросе: {response.status_code}")


async def check_for_empty_list(result):
    return result == []


async def user_form_create(update, context, message_text=None):

    keyboard_cancel = [
        ['Продолжить'],
        ['Назад']
    ]
    
    if message_text == None:
        message_text = (
            'К сожалению, на текущий момент подходящих вакансий нет.\n'
            'Предлагаем заполнить небольшую форму.\n'
            'И мы сообщим Вам в числе первых, когда подходящая вакансия появится!'
        )

    reply_markup = ReplyKeyboardMarkup(keyboard_cancel, resize_keyboard=True)
    await update.message.reply_text(message_text, reply_markup=reply_markup)

    context.user_data['Запрос full данных'] = 'Запуск анкетирования'
    context.user_data['information_form'] = {}
    await user_full_information_process(update, context)


async def inline_buttons_packed(update, context, result):
    for vacancy_full in result:
        vacancy = vacancy_full.vacancy_inf
        vacancy_id = vacancy_full.vacancy_id
        vacancy_text = await message_creater(vacancy)
        
        await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_id=vacancy_id)


async def get_vacancies_by_keys_list(update, context, keywords):
    try:
        result = await get_vacancies_by_keys_list_module(keywords)
    
    except Exception as error:
        sleep(5)
        result = await get_vacancies_by_keys_list_module(keywords)
    
    else:
        empty_list = await check_for_empty_list(result)
        if empty_list:
            text = (
            'К сожалению, на текущий момент подходящих вакансий нет.\n'
            'Сформировать новый запрос.\n'
        )
            await update.message.reply_text(text)
            return

        await inline_buttons_packed(update, context, result)


async def get_no_exp_vacancies(update, context):
    try:
        result = await get_no_exp_vacancies_module()

    except Exception as error:
        sleep(5)
        result = await get_no_exp_vacancies_module()

    else:
        empty_list = await check_for_empty_list(result)
        if empty_list:
            text = (
            'К сожалению, на текущий момент подходящих вакансий нет.\n'
            'Сформировать новый запрос.\n'
        )
            await update.message.reply_text(text)
            return

        await inline_buttons_packed(update, context, result)


async def get_vacancies_by_key_word(update, context, key_word):
    try:
        result = await get_vacancies_by_key_word_module(key_word)

    except Exception as error:
        sleep(5)
        result = await get_vacancies_by_key_word_module(key_word)

    else:
        empty_list = await check_for_empty_list(result)
        if empty_list:
            text = (
            'К сожалению, на текущий момент подходящих вакансий нет.\n'
            'Сформировать новый запрос.\n'
        )
            await update.message.reply_text(text)
            return

        await inline_buttons_packed(update, context, result)
            

async def message_creater(vacancy):
    for key, value in vacancy.items():

        if type(value) == list:
            value = ', '.join(value)
            vacancy[key] = value

        if str(value) == '' or str(value) == 'None':
            vacancy[key] = 'Нет данных.\n'

    if 'None' in vacancy['Оплата ОТ']:
        vacancy['Оплата ОТ'] = ''
    if 'None' in vacancy['Оплата ДО']:
        vacancy['Оплата ДО'] = ''


    vacancy_name = vacancy['Вакансия']

    # valute = vacancy['Валюта']
    min_salary = vacancy['Оплата ОТ']
    max_salary = vacancy['Оплата ДО']
    min_max_salary_str = f'{min_salary}{max_salary}'
    if min_max_salary_str == '':
        min_max_salary_str = 'Нет данных\n'
    
    req_text = vacancy['Требования']
    if req_text != 'Нет данных.\n':
        logging.info(f'ПРОВЕРКА:\nreq_text = !!{req_text}!!\ntype ={type(req_text)}\n')
        requirement = vacancy['Требования'].split('. ')
        req_text = '\n'
        for req in requirement:
            
            if len(req) > 3:
                if req[0] == '-':
                    req = req[1::]
                req_text += f'- {req}.\n'
    
    resp_text = vacancy['Обязанности']
    if resp_text != 'Нет данных.\n':
        responsibilities = vacancy['Обязанности'].split('. ')
        resp_text = '\n'
        for resp in responsibilities:
            if resp != '': 
                resp_text += f'- {resp}.\n'

    schedule = vacancy['Рабочий график']

    experience = vacancy['Наличие опыта']
    if 'Нет опыта' in experience:
        experience = 'рассматриваются кандидаты без опыта работы'
    
    employment = vacancy['Занятость']

    vacancy_url = vacancy['Ссылка на вакансию']
    message = f'[Ссылка на вакансию]({vacancy_url})'
    
    vacancy_text = (
    f'<b>Вакансия: {vacancy_name}</b>\n\n'

    f'💰 <u><b>Оплата</b></u>:\n'
    f'{min_max_salary_str}\n'

    f'📋 <u><b>Требования</b></u>: {req_text}\n'

    f'⚙️ <u><b>Обязанности</b></u>: {resp_text}\n'

    f'🕒 <u><b>Рабочий график</b></u>: {schedule}.\n\n'

    f'👥 <u><b>Наличие опыта</b></u>: {experience}.\n\n'

    f'📅 <u><b>Занятость</b></u>: {employment}.\n\n'

    # f'🔗 <a href="{vacancy_url}">Ссылка на вакансию</a>\n\n'

    'Присоединяйтесь к нашей команде и станьте частью\nдинамичной сферы энергетики! 💡✨'
    )

    return vacancy_text


async def get_all_company_vacancies(update, context):
    try:
        result = await get_all_vacancies_module()

    except Exception as error:
        sleep(5)
        result = await get_all_vacancies_module()

    else:
        empty_list = await check_for_empty_list(result)
        if empty_list:
            text = (
            'К сожалению, на текущий момент подходящих вакансий нет.\n'
            'Сформировать новый запрос.\n'
        )
            await update.message.reply_text(text)
            return

        await inline_buttons_packed(update, context, result)


async def update_vacancies_db(page=0, per_page=100):
    
    logging.info(f'Токен доступа = {ACCESS_TOKEN}')
    
    vacancies_url = "https://api.hh.ru/vacancies"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "area": 1,  # ID города, например, Москва - 1
        'employer_id': [27708],
        "page": page,
        "per_page": per_page
    }
    response = requests.get(vacancies_url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Ошибка при получении списка вакансий: {response.status_code} - {response.text}")
    else:
        result = response.json()
        
        formatted_json = json.dumps(result['items'], ensure_ascii=False, indent=4)
        logging.info(f'formatted_json = {formatted_json}\n\n')
        tight_inf = await inf_taker(result['items'])
        await filling_vacancies_to_db(tight_inf)


async def send_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text, vacancy_id) -> None:
    logging.info('РЕГИСТРАЦИЯ КНОПОК')
    # Создаем инлайн кнопки
    keyboard = [
        [
            InlineKeyboardButton("Откликнуться", callback_data=f'tq;{vacancy_id}')
        ],

        [
            InlineKeyboardButton("Откликнуться через hhru", callback_data=f'{vacancy_id}')
        ],

        [
            InlineKeyboardButton("Получить консультацию специалиста 📞", callback_data='get_spec')
        ],
    ]

    # Создаем разметку для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с инлайн кнопками
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='HTML')


async def extra_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создаем инлайн кнопки
    keyboard = [
        [
            InlineKeyboardButton("Главное меню", callback_data=f'main_menu')
        ],

    ]
    # Создаем разметку для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с инлайн кнопками
    text = 'Вы всегда можете вернуться.'
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')


async def inf_taker(full_information):
    tight_information = []
    for vac in full_information:
        new_vac = {}
        new_vac['id Вакансии'] = vac['id']
        new_vac['Название Компании'] = vac['employer']['name']
        new_vac['Вакансия'] = vac['name']
        
        # new_vac['Валюта'] = vac['salary']['currency']
        try:
            valute = vac['salary']['currency']
            if valute.__eq__('RUR'):
                valute = 'руб'
            value_m = vac['salary']['from']
            new_vac['Оплата ОТ'] = f'От {value_m} {valute}\n'
            
            value_max = vac['salary']['to'] 
            new_vac['Оплата ДО'] = f'До {value_max} {valute}\n'
        except Exception:
            new_vac['Оплата ОТ'] = f'От: Нет данных\n'
            new_vac['Оплата ДО'] = f'До: Нет данных\n'
        
        # new_vac['изображение'] = vac['employer']['logo_urls']['original']
        work_req = vac['snippet']['requirement']
        if work_req:
            new_vac['Требования'] = re.sub(r'<[^>]+>', '', work_req)
        else:
            new_vac['Требования'] = None
        work_resp = vac['snippet']['responsibility']
        if work_resp:
            new_vac['Обязанности'] = re.sub(r'<[^>]+>', '', work_resp)
        else:
            new_vac['Обязанности'] = None

        new_vac['Рабочий график'] = vac['schedule']['name']

        new_vac['Наличие опыта'] = vac['experience']['name'] 

        new_vac['Занятость'] = vac['employment']['name']

        
        # new_vac['город'] = vac['address']['city']
        try:
            m_s = vac['address']['metro_stations']
            new_vac['Станции метро'] = []
            for metro_stations in m_s:
                # new_vac['станции метро'].append(metro_stations['station_name'], metro_stations['line_name'])
                new_vac['Станции метро'].append(metro_stations['station_name'])

        except Exception:
            pass
        
        
        new_vac['Ссылка на вакансию'] = vac['alternate_url']
        new_vac['Ссылка на работодателя'] = vac['employer']['alternate_url']
        tight_information.append(new_vac)
        
    return tight_information


async def image_download_by_url(image_url, context):

    folder = downloads_path
    image_name = os.path.basename(image_url)
    file_path = os.path.join(f'{folder}/', image_name)


    response = requests.get(image_url)
    response.raise_for_status()  # Проверяем на ошибки
    print(file_path)
    # Сохраняем изображение на диск
    with open(file_path, 'wb') as file:
        file.write(response.content)

    # context.user_data['company_image_path'] = file_path
    return file_path


async def send_pdf(update, context, pdf_path, chat_id, user_name):
    # Путь к вашему PDF-файлу
    pdf_file_path = pdf_path
    pdf_name = f'Резюме {user_name}.pdf'
    with open(pdf_file_path, 'rb') as pdf_file:
        await context.bot.send_document(chat_id=chat_id, document=pdf_file, filename=pdf_name)
