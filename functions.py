import logging
import os
import requests
import json
import re

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from constants import *
from menu_buttons import *
from test_db import get_all_users


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


async def ask_user_inf(user_id, user_inf):
    user_name, user_phone = user_inf.split(';')
    user_inf_params = {'ФИО': user_name, 'Номер телефона': user_phone}
    await update_user_in_db(user_id, user_inf=user_inf_params)


async def user_full_information_process(update: Update, context: ContextTypes.DEFAULT_TYPE, current_text):
    user_id = update.effective_user.id
    step = {
        'Старт': ('ФИО','Для начала укажите в сообщении ваши ФИО:'),
        'ФИО': ('Номер телефона', 'Ваш контактный номер телефона:'),
        'Номер телефона': ('Должность', 'Желаемая должность:'),
        'Должность': ('Опыт работы', 'Ваш стаж:\n\nМенее года\n1-2 года\n2-3 года\n3 и более лет'),
        'Опыт работы': ('done', 'Ура, ваша анкета уже у нас! Спасибо за Ваше время, мы Вас не подведем!\nЕсли Вам не хочется ждать, Вы можете позвонить нам напрямую: +7 495 957-19-57')
    }
    current_step = context.user_data['Запрос full данных']
    if current_step != 'Старт':
        await update_user_in_db(user_id, user_inf={current_step:current_text})

    next_step, message_text = step[current_step]
    context.user_data['Запрос full данных'] = next_step
    await context.bot.send_message(chat_id=user_id, text=message_text, parse_mode='Markdown')
    if next_step.__eq__('done'):
        context.user_data.pop('Запрос full данных')


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
        ['Назад']
    ]

    message_text = update.message.text
    if message_text == 'Да':
        current_message_text, image_path = context.user_data.get('message_inf')
        users = await get_all_users()  # Получаем всех пользователей
        users_id = [user['telegram_id'] for user in users]

        users = [2091023767]

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
    message_text = context.user_data.get('current_text')
    file_path = None

    if update.message.photo:
        message_text = update.message.caption
        context.user_data['current_text'] = message_text
        photo = update.message.photo[-1]  # Получаем самое высокое качество изображения
        file = await photo.get_file()
        file_path = f"/home/WeddellDen/big_project/downloads/{photo.file_id}.jpg"
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


async def get_vacancies_proccess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info('send process')
    # Запрос текста сообщения от пользователя
    message_creator = {
        'Creating' : get_vacancies_search_query,
        'Looking' : get_vacancies,
        'Choosen' : choose_vacancy
        # 'Completed' : message_text_sending
    }
    if 'vacancies_proccess' not in context.user_data:
        context.user_data['vacancies_proccess'] = 'Creating'
    current_message_state = context.user_data.get('vacancies_proccess')

    current_step = message_creator[current_message_state]

    await current_step(update, context)



async def get_vacancies_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info('request creating process')
    

    await update.message.reply_text('Пришлите ключевое слово, по которому будем осуществлять поиск', reply_markup=ReplyKeyboardRemove())

    context.user_data['vacancies_proccess'] = 'Looking'

# async def get_vacancies(update, context, client_id, client_secret, search_query, page=1, per_page=3):
async def get_vacancies(update, context, page=1, per_page=100):
    
    """
    Получает список вакансий с hh.ru.
    
    Args:
        client_id (str): Client ID вашего приложения.
        client_secret (str): Client Secret вашего приложения.
        search_query (str): Поисковый запрос для вакансий.
        page (int): Номер страницы результатов (по умолчанию 0).
        per_page (int): Количество вакансий на странице (по умолчанию 20).
        
    Returns:
        dict: Словарь с информацией о вакансиях.
    """
    
    keyboard = [
    ['Первая', 'Вторая', 'Третья'],
    ['Показать еще'],
    ['Назад']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    request_key_word = update.message.text

    await get_vacancies_by_key_word(update, context, key_word=request_key_word)


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


async def get_vacancies_by_keys_list(update, context, keywords, page=0, per_page=100):
    # Формируем строку запроса с использованием оператора OR
    query = ' OR '.join(keywords)
    
    logging.info(f'Токен доступа = {ACCESS_TOKEN}')
    
    # Запрос списка вакансий
    vacancies_url = "https://api.hh.ru/vacancies"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "area": 1,  # ID города, например, Москва - 1
        'employer_id': [27708],
        "text": query,
        "page": page,
        "per_page": per_page
    }
    response = requests.get(vacancies_url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Ошибка при получении списка вакансий: {response.status_code} - {response.text}")
    else:
        result = response.json()
        vacancies_count = result['found']
        logging.info(f'result = {result}\n\n')
        if result['found'].__eq__(0):
            await update.message.reply_text('К сожалению, на текущий момент подходящих вакансий нет.')
            context.user_data['Запрос full данных'] = 'Старт'
            await user_full_information_process(update, context, current_text=None)
            return
        
        formatted_json = json.dumps(result['items'], ensure_ascii=False, indent=4)
        logging.info(f'formatted_json = {formatted_json}\n\n')
        tight_inf = await inf_taker(result['items'])

        logging.info(f'tight_inf = {tight_inf}\n\n')


        context.user_data['vacancies_proccess'] = 'Choosen'
        # context.user_data.pop('vacancies_proccess')
        # new_vac['id Вакансии'] = vac['id']
        context.user_data['vacancies_id'] = []
        for vacancy in tight_inf:
            vacancy_url = vacancy['Ссылка на вакансию']
            vacancy_text = await message_creater(vacancy)
            
            vacancy_id = vacancy.pop('id Вакансии')
            context.user_data['vacancies_id'].append(vacancy_id)
            # context.user_data[vacancy_id] = vacancy_text
            await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_url=vacancy_url)


async def get_no_exp_vacancies(update, context, page=0, per_page=100):
    
    logging.info(f'Токен доступа = {ACCESS_TOKEN}')
    
    # Запрос списка вакансий
    vacancies_url = "https://api.hh.ru/vacancies"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "area": 1,  # ID города, например, Москва - 1
        'employer_id': [27708],
        "experience": "noExperience",
        "page": page,
        "per_page": per_page
    }
    response = requests.get(vacancies_url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Ошибка при получении списка вакансий: {response.status_code} - {response.text}")
    else:
        result = response.json()
        vacancies_count = result['found']
        logging.info(f'result = {result}\n\n')
        if result['found'].__eq__(0):
            await update.message.reply_text('К сожалению, на текущий момент подходящих вакансий нет.')
            context.user_data['Запрос full данных'] = 'Старт'
            await user_full_information_process(update, context, current_text=None)
            return
        
        formatted_json = json.dumps(result['items'], ensure_ascii=False, indent=4)
        logging.info(f'formatted_json = {formatted_json}\n\n')
        tight_inf = await inf_taker(result['items'])

        logging.info(f'tight_inf = {tight_inf}\n\n')


        context.user_data['vacancies_proccess'] = 'Choosen'
        # context.user_data.pop('vacancies_proccess')
        # new_vac['id Вакансии'] = vac['id']
        context.user_data['vacancies_id'] = []
        for vacancy in tight_inf:
            vacancy_url = vacancy['Ссылка на вакансию']
            vacancy_text = await message_creater(vacancy)
            
            vacancy_id = vacancy.pop('id Вакансии')
            context.user_data['vacancies_id'].append(vacancy_id)
            # context.user_data[vacancy_id] = vacancy_text
            await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_url=vacancy_url)


async def get_vacancies_by_key_word(update, context, key_word, page=0, per_page=100):
    request_key_word = key_word
    
    logging.info(f'Токен доступа = {ACCESS_TOKEN}')
    
    # Запрос списка вакансий
    vacancies_url = "https://api.hh.ru/vacancies"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "area": 1,  # ID города, например, Москва - 1
        'employer_id': [27708],
        # "only_with_salary": True,
        "text": request_key_word,
        "page": page,
        "per_page": per_page
    }
    response = requests.get(vacancies_url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Ошибка при получении списка вакансий: {response.status_code} - {response.text}")
    else:
        result = response.json()
        vacancies_count = result['found']
        logging.info(f'result = {result}\n\n')
        
        formatted_json = json.dumps(result['items'], ensure_ascii=False, indent=4)
        logging.info(f'formatted_json = {formatted_json}\n\n')
        if result['found'].__eq__(0):
            await update.message.reply_text('К сожалению, на текущий момент подходящих вакансий нет.')
            context.user_data['Запрос full данных'] = 'Старт'
            await user_full_information_process(update, context, current_text=None)
            return
        tight_inf = await inf_taker(result['items'])

        logging.info(f'tight_inf = {tight_inf}\n\n')


        context.user_data['vacancies_proccess'] = 'Choosen'
        # context.user_data.pop('vacancies_proccess')
        # new_vac['id Вакансии'] = vac['id']
        context.user_data['vacancies_id'] = []
        for vacancy in tight_inf:
            vacancy_url = vacancy['Ссылка на вакансию']
            vacancy_text = await message_creater(vacancy)
            
            vacancy_id = vacancy.pop('id Вакансии')
            context.user_data['vacancies_id'].append(vacancy_id)
            # context.user_data[vacancy_id] = vacancy_text
            await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_url=vacancy_url)
            

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

    f'🔗 <a href="{vacancy_url}">Ссылка на вакансию</a>\n\n'

    'Присоединяйтесь к нашей команде и станьте частью\nдинамичной сферы энергетики! 💡✨'
    )

    return vacancy_text

async def get_all_company_vacancies(update, context, page=0, per_page=100):
    
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
        logging.info(f'result = {result}\n\n')
        if result['found'].__eq__(0):
            await update.message.reply_text('К сожалению, на текущий момент подходящих вакансий нет.')
            context.user_data['Запрос full данных'] = 'Старт'
            await user_full_information_process(update, context, current_text=None)
            return
        formatted_json = json.dumps(result['items'], ensure_ascii=False, indent=4)
        logging.info(f'formatted_json = {formatted_json}\n\n')
        tight_inf = await inf_taker(result['items'])

        logging.info(f'tight_inf = {tight_inf}\n\n')

        context.user_data['vacancies_proccess'] = 'Choosen'
        for vacancy in tight_inf:
            vacancy_url = vacancy['Ссылка на вакансию']
            vacancy_text = await message_creater(vacancy)
            
            await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_url=vacancy_url)
            


        # await send_inline_buttons(update, context, message_text=vacancy_text, vacancy_url=vacancy_url)


async def send_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text, vacancy_url) -> None:
    logging.info('РЕГИСТРАЦИЯ КНОПОК')
    # Создаем инлайн кнопки
    keyboard = [
        [InlineKeyboardButton("Откликнуться", url=vacancy_url)],
        [InlineKeyboardButton("Получить консультацию специалиста 📞", callback_data='get_spec')],
    ]

    # Создаем разметку для кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с инлайн кнопками
    await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='HTML')



async def choose_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choosed_option = update.message.text

    context.user_data['vacancy_turn_choosed'] = choosed_option
    all_options = {
        'Первая' : send_request,
        'Вторая' : send_request,
        'Третья' : send_request,
        'Показать еще' : None,
        'Назад' : show_vacancies
        # 'Completed' : message_text_sending
    }
    current_option = all_options[choosed_option]
    await current_option(update, context)

async def request_creating():
    pass

# async def send_request(context, access_token, user_access_token, resume_id, message):
async def send_request(update, context):

    id_translator = {
        'Первая' : 0,
        'Вторая' : 1,
        'Третья' : 2,
    }

    vacancies_id = context.user_data.get('vacancies_id')
    vacancy_turn_choosed = context.user_data.get('vacancy_turn_choosed')
    vacancy_id = vacancies_id[id_translator[vacancy_turn_choosed]]


    access_token = os.getenv('ACCESS_TOKEN')
    
    
    headers = {
        "Authorization": f"Bearer {USER_ACCESS_TOKEN}"
    }
    resume_id = '05e6f3e0ff0d9395310039ed1f33566f415a30'
    data = {
            "Authorization": f"Bearer {access_token}",
            'vacancy_id': vacancy_id, # id вакансии
            'resume_id': resume_id, 
            "message": request_text, # текст сопроводительного документа
            "Content-Type": "application/json"
            }

    


    click_url = 'https://api.hh.ru/negotiations'
    response = requests.post(click_url, headers=headers, data=data)
    try:
        resp = json.loads(
        response.content.decode()
    )
        # logging.info(resp)
    except Exception:
        pass
    # logging.info(response)
    # Проверка статуса ответа
    if response.status_code != 201:
       pass
        # logging.info(f"Ошибка при отправке отклика: {response.status_code} - {response.text}")


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

    folder = r'C:/dev_py/hh_bit/bot_project/bot_architecture/downloads'
    folder = '/home/WeddellDen/big_project/downloads'
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
