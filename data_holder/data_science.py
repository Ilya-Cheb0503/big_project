import json
import os

from pwd_generator import get_current_directory
from settings import logging

vacancies_keys_file = '/data_holder/vacancies_keys.json'

async def load_vacancies_keys():
    
    project_folder = await get_current_directory()
    vacancies_keys_path = project_folder + vacancies_keys_file
    
    if os.path.exists(vacancies_keys_path):
        with open(vacancies_keys_path, 'r') as file:
            vacancies_keys = json.load(file)
            # logging.info("Уведомления успешно загружены.")
            return vacancies_keys
    
    logging.warning("Файл уведомлений не найден, возвращается пустой словарь.")
    return {}


async def save_vacancies_keys(vacancies_keys):
    # logging.info("Сохранение уведомлений в файл.")
    
    project_folder = await get_current_directory()
    vacancies_keys_path = project_folder + vacancies_keys_file
    
    with open(vacancies_keys_path, 'w') as file:
        json.dump(vacancies_keys, file, ensure_ascii=True, indent=4)
    
    # logging.info("Уведомления успешно сохранены.")


async def key_keeper(word_key):
    keys_bank = await load_vacancies_keys()

    if word_key not in keys_bank:
        keys_bank[word_key] = 1
    else:
        keys_bank[word_key] += 1
    
    await save_vacancies_keys(keys_bank)


async def data_inf():
    text = (
        'Статистика по ключюевым словам, которые используют пользователи при поиске вакансий:\n'
    )

    keys_collections = await load_vacancies_keys()

    popular_keys = 0
    for key, count in keys_collections.items():
        if count > 1:
            text += f'"{key}": {count};\n'
            popular_keys += 1
    
    if popular_keys == 0:
        text = 'На текущий момент нет вакансий, которые пользователь искал бы чаще одного раза.'
    # отправить текст
        # функция отправки текста админу
