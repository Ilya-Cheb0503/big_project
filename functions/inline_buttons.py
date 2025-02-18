from time import sleep

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from functions.vacancies_cards import message_creater
from settings import logging

from db_depart.new_module import get_vacancy_by_vacancy_id

async def inline_buttons_packed(update, context, result):
    time_wait = 0
    if len(result) > 5:
        time_wait = 2
    vacancy_num = 0
    for vacancy_full in result:
        vacancy_num += 1
        vacancy = vacancy_full.vacancy_inf
        vacancy_id = vacancy_full.vacancy_id
        vacancy_text = await message_creater(vacancy)

        options_ask = [
            ['Показать еще', 'more-more'],
            ['Достаточно', 'stop'],
        ]
        ask_text = 'Показать еще вакансии или остановиться ?'

        await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_id=vacancy_id)
        if vacancy_num == 5:
            sleep(2)
            # await set_inline_keyboard(update, context, options_ask, ask_text)
            # query = update.callback_query
            # rest = await query.answer()
            # print(f'Rest is {rest}')
            # while rest:
            #     query = update.callback_query
            #     rest = await query.answer() 

            #     # Мы отправляем сообщение "Показать еще вакансии" и там только вариант "еще", который ведет к тому, что подгружается еще 5 вакансий, а если нет, то никакого ожилания
            #     # то есть просто в само сообщение закладываем инфу о вакансиях, которые подргузятся, если их запросят
            #     # Можно оставить кнопку - Достаточно, которая будет удалять это сообщение.

            #     # await button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE)
            #     sleep(2)
            #     print(f'rest is {rest}')
            # print(123)
            vacancy_num = 0
            # if context.user_data['user_move'] == 'stop':
            #     context.user_data.pop('user_move')
            #     return
            # context.user_data.pop('user_move')


async def send_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text, vacancy_id) -> None:
    logging.info('РЕГИСТРАЦИЯ КНОПОК')
    user_id = update.effective_user.id

    vacancy = await get_vacancy_by_vacancy_id(vacancy_id)
    vacancy_url = vacancy.vacancy_inf['Ссылка на вакансию']
    # Создаем инлайн кнопки
    keyboard = [
        [
            InlineKeyboardButton("Откликнуться", callback_data=f'tq;{vacancy_id}')
        ],

        # [
        #     InlineKeyboardButton("Откликнуться через hhru", callback_data=f'{vacancy_id}')
        # ],
        [
            InlineKeyboardButton("Ссылка на вакансию", callback_data='req_button', url=vacancy_url)
        ],

        [
            InlineKeyboardButton("Получить консультацию специалиста 📞", callback_data='get_spec')
        ],
    ]

    # Создаем разметку для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup, parse_mode='HTML')


async def set_inline_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, buttons_list: list, message_text: str) -> None:
    logging.info('РЕГИСТРАЦИЯ КНОПОК')
    # Создаем инлайн кнопки
    keyboard = []

    for button in buttons_list:
        logging.info(button)
        if all(isinstance(element, str) for element in button):
            button_name, button_data = button
            keyboard.append(
                [InlineKeyboardButton(text = button_name, callback_data = button_data)]
            )
        else:
            next_button_row = []
            for element in button:
                button_name, button_data = element
                next_button_row.append(
                    InlineKeyboardButton(text = button_name, callback_data = button_data)
                )
            keyboard.append(next_button_row)

    # Создаем разметку для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text=message_text, reply_markup=reply_markup, parse_mode='HTML')




async def extra_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE, inline_message_text, user_id = None, parse_mode=None) -> None:
    # Создаем инлайн кнопки
    keyboard = [
        [
            InlineKeyboardButton("Главное меню", callback_data=f'main_menu')
        ],

    ]
    # Создаем разметку для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)
    if user_id:
        await context.bot.send_message(chat_id=user_id, text=inline_message_text, reply_markup=reply_markup, parse_mode=parse_mode)
    else:
        await update.message.reply_text(inline_message_text, reply_markup=reply_markup, parse_mode=parse_mode)
