import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from constants.keyboards import (admin_main_menu_keyboard,
                                 user_main_menu_keyboard)
from constants.messages_text import welcome_text
from constants.some_constants import admins_id, group_id
from db_depart.user_db import update_user_in_db
from functions.inline_buttons import extra_inline_button, set_inline_keyboard


async def user_full_information_process(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if 'Запрос анкетных данных' in context.user_data:
        context.user_data.pop('Запрос анкетных данных')
        warning_text = 'Вы не закончили заполнять анкетные данные для отклика.\nПроцесс был прерван.'
        await context.bot.send_message(chat_id=user_id, text=warning_text)
    # на случай, если пользователь перед тем, как откликнуться на вакансию заполнял анкету и не закончил ее заполнять
    # тогда мы прерываем этот процесс и начинаем процесс заполнения анкеты для отклика

    if update.message:
        current_text = update.message.text
        current_step = context.user_data['Запрос full данных']
    else:
        current_text = None
        current_step = 'Запуск анкетирования'
    
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
    
    
    logging.info(f'current_text = {current_text}')
    if current_text == 'Главное меню' or current_text == 'Назад':
        context.user_data['Запрос full данных'] = 'Запуск анкетирования'
        context.user_data.pop('Запрос full данных')
        
        admin_check = user_id in admins_id
        if admin_check:
            context.user_data['admin_status'] = True
            buttons_list = admin_main_menu_keyboard
        else:
            buttons_list = user_main_menu_keyboard

        keyboard = [
            ['Главное меню'],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text='Возвращаем вас в главное меню', reply_markup=reply_markup)
        await set_inline_keyboard(update, context, buttons_list = buttons_list, message_text = welcome_text)
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
            await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

        else:
            context.user_data['Запрос full данных'] = 'Запуск анкетирования'
            context.user_data.pop('Запрос full данных')
            
            admin_check = user_id in admins_id
            if admin_check:
                context.user_data['admin_status'] = True
                buttons_list = admin_main_menu_keyboard
            else:
                buttons_list = user_main_menu_keyboard

            keyboard = [
                ['Главное меню'],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await context.bot.send_message(chat_id=user_id, text='Возвращаем вас в главное меню', reply_markup=reply_markup)
            await set_inline_keyboard(update, context, buttons_list = buttons_list, message_text = welcome_text)

    elif next_step.__eq__('Номер телефона'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Ваш контактный номер телефона:'
        keyboard = [
        ['Главное меню'],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    

    elif next_step.__eq__('Должность'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Желаемая должность:'
        keyboard = [
            ['Главное меню'],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    

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
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    
    elif next_step.__eq__('Образование'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')
        text = 'Ваш уровень образования:'
        keyboard = [
        ['Высшее образование'],
        ['Среднее профессиональное'],
        ['Школьное'],

    ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)


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
        await context.bot.send_message(chat_id=user_id, text=user_bio, reply_markup=reply_markup, parse_mode='HTML')

    elif current_step.__eq__('Подтверждение'):
        logging.info(f'ТЕКУЩИЙ ШАГ {current_step} а текст сообщения {current_text}')

        keyboard = [
                ['Главное меню'],
            ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

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

            await context.bot.send_message(chat_id=user_id, text='Возвращаем клавиатуру в исходное.', reply_markup=reply_markup)
            await extra_inline_button(update, context, message_text,)
            
            await context.bot.send_message(chat_id=group_id, text=user_bio_notice, parse_mode='HTML')

        else:
            context.user_data['Запрос full данных'] = 'ФИО'
            
            await context.bot.send_message(chat_id=user_id, text='Тогда начнем сначала.\nУкажите ваши ФИО:', reply_markup=reply_markup)

    logging.info(f'ЗАВЕРШАЕМ РАБОТУ ФУНКЦИИ с шагом {current_step} а текст сообщения {current_text}')
    

