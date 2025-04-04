import json
from time import sleep

import requests

from constants.some_constants import ACCESS_TOKEN
from data_holder.data_science import key_keeper
from db_depart.new_module import (filling_vacancies_to_db,
                                  get_all_vacancies_module,
                                  get_no_exp_vacancies_module,
                                  get_vacancies_by_key_word_module,
                                  get_vacancies_by_keys_list_module)
from functions.inline_buttons import inline_buttons_packed
from functions.special_functions import check_for_empty_list
from functions.vacancies_cards import inf_taker
from settings import logging


async def get_vacancies_by_keys_list(update, context, keywords, first_key):

    await key_keeper('categories', first_key)

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
            'Попробуйте сформировать новый запрос.\n'
        )
            user_id = update.effective_user.id
            await context.bot.send_message(chat_id=user_id, text=text)
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
            'Попробуйте сформировать новый запрос.\n'
        )
            user_id = update.effective_user.id
            await context.bot.send_message(chat_id=user_id, text=text)
            return

        await inline_buttons_packed(update, context, result)


async def get_vacancies_by_key_word(update, context, key_word):

    await key_keeper('keys_word', key_word)

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
            'Попробуйте сформировать новый запрос.\n'
        )
            user_id = update.effective_user.id
            await context.bot.send_message(chat_id=user_id, text=text)
            return

        await inline_buttons_packed(update, context, result)
            

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
            'Попробуйте сформировать новый запрос.\n'
        )
            user_id = update.effective_user.id
            await context.bot.send_message(chat_id=user_id, text=text)
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
        # НЕОБХОДИМО ДОБАВИТЬ РАЗДЕЛЕНИЕ ПО ГОРОДАМ И ПРОДУМАТЬ ВООБЩЕ СПОСОБ ХРАНЕНИЯ ВАКАСНИЙ ПО РАЗНЫМ ГОРОДАМ
        # "area": 1,  # ID города, например, Москва - 1
        'employer_id': [1279490],
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


async def get_vacancy_count():
    employer_id = '1279490'
    url = f'https://api.hh.ru/vacancies?employer_id={employer_id}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Получаем общее количество вакансий
        total_vacancies = data['found']
        return total_vacancies
    else:
        logging.error(f"Ошибка при запросе: {response.status_code}")