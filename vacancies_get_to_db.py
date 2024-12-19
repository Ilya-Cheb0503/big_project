import asyncio
import json
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base
from databases import Database
import logging
from typing import Optional, Dict


Base = declarative_base()


class Vacancy_hh(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(Integer, unique=True)
    vacancy_inf = Column(JSON, nullable=True)

DATABASE_URL = "sqlite:///./vacancies.db"
database = Database(DATABASE_URL)


async def save_vacancy(vacancy_id: int, vacancy_inf: dict = None):
    existing_vacancy = await get_vacancy_by_id(vacancy_id)
    if existing_vacancy:
        print(f"Вакансия с vacancy_id {vacancy_id} уже существует.")
        return

    query = """
    INSERT INTO vacancies (vacancy_id,  vacancy_inf)
    VALUES (:vacancy_id, :vacancy_inf)
    """
    values = {
        "vacancy_id": vacancy_id,
        "vacancy_inf": json.dumps(vacancy_inf)
    }
    await database.execute(query, values)


async def update_vacancy(vacancy_id: int, **kwargs):
    set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
    query = f"UPDATE vacancies SET {set_clause} WHERE vacancy_id = :vacancy_id"
    values = {"vacancy_id": vacancy_id, **kwargs}
    await database.execute(query, values)


async def update_vacancy_info(vacancy_id: int, vacancy_inf: Optional[dict] = None):
    updates = {}
    
    if vacancy_inf is not None:
        updates['vacancy_inf'] = json.dumps(vacancy_inf)
    
    if updates:
        await update_vacancy(vacancy_id, **updates)


async def get_vacancy_by_id(vacancy_id: int):
    query = "SELECT * FROM vacancies WHERE vacancy_id = :vacancy_id"
    vacancy = await database.fetch_one(query, values={"vacancy_id": vacancy_id})
    
    if vacancy:
        vacancy_dict = dict(vacancy)
        vacancy_dict['vacancy_inf'] = json.loads(vacancy_dict['vacancy_inf']) if vacancy_dict['vacancy_inf'] else None
        return vacancy_dict
    return None


async def get_vacancy_by_parameter(parameter, parameter_value):
    query = f"SELECT * FROM vacancies WHERE vacancy_inf LIKE '%\"{parameter}\":\"{parameter_value}\"%'"
    # vacancy = await database.fetch_one(query)
    # query = f"SELECT * FROM vacancies WHERE vacancy_inf->>{parameter} = :parameter_value"
    vacancy = await database.fetch_one(query, values={parameter: parameter_value})
    
    if vacancy:
        vacancy_dict = dict(vacancy)
        vacancy_dict['vacancy_inf'] = json.loads(vacancy_dict['vacancy_inf']) if vacancy_dict['vacancy_inf'] else None
        return vacancy_dict
    return None


async def get_all_vacancies_by_parameter(parameter, parameter_value):
    query = f"SELECT * FROM vacancies WHERE vacancy_inf->>{parameter} = :parameter_value"
    vacancies = await database.fetch_all(query, values={"parameter_value": parameter_value})
    
    result = []
    for vacancy in vacancies:
        vacancy_dict = dict(vacancy)
        vacancy_dict['vacancy_inf'] = json.loads(vacancy_dict['vacancy_inf']) if vacancy_dict['vacancy_inf'] else None
        result.append(vacancy_dict)
    
    return result


async def get_all_vacancys():
    query = "SELECT * FROM vacancies"
    vacancies = await database.fetch_all(query)
    
    vacancy_list = []
    for vacancy in vacancies:
        vacancy_dict = dict(vacancy)
        vacancy_dict['vacancy_inf'] = json.loads(vacancy_dict['vacancy_inf']) if vacancy_dict['vacancy_inf'] else None
        vacancy_list.append(vacancy_dict)
    
    return vacancy_list


async def start_create_table():
    await database.connect()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    await database.disconnect()

async def get_vacancy_from_db_by_id(vacancy_id):
    await database.connect()
    vacancy = await get_vacancy_by_id(vacancy_id)
    await database.disconnect()
    return vacancy


async def get_vacancy_from_db_by_parameter(parameter, par_value):
    await database.connect()
    vacancy = await get_vacancy_by_parameter(parameter, par_value)
    await database.disconnect()
    return vacancy

async def create_vacancy_in_db(vacancy_id, vacancy_inf):
    
    await database.connect()
    await save_vacancy(vacancy_id=vacancy_id, vacancy_inf=vacancy_inf)
    
    await database.disconnect()


async def create_vacancies_in_db(vacancies_data):
    await database.connect()
    
    for vacancy in vacancies_data:
        vacancy_id, vacancy_inf = vacancy
        await save_vacancy(vacancy_id=vacancy_id, vacancy_inf=vacancy_inf)
    
    await database.disconnect()

# подумать о ДЕКОРАТОРЕ, чтобы строки с подключением и отключеним от таблицы прописать лишь раз


async def update_vacancy_in_db(vacancy_id, menu_state=None, vacancy_inf=None):
    await database.connect()

    if vacancy_inf:
        vacancy = await get_vacancy_by_id(vacancy_id)
        vacancy_upd_inf = vacancy['vacancy_inf']
        for key, value in vacancy_inf.items():
            vacancy_upd_inf[key] = value
        logging.info(f'ОБНОВЛЕНИЕ ДАННЫХ {vacancy_upd_inf}')
        await update_vacancy_info(vacancy_id, vacancy_inf=vacancy_upd_inf)

    await database.disconnect()


async def main():
    # await start_create_table()  # Создание таблицы
    # await save_vacancy(111, {'name': 'проверка', 'exp': 'нет опыта'})
    vac_list = [
        [123321, {'name': 'проверка123', 'exp': 'нет опыта123'}],
        [321123, {'name': 'проверка321', 'exp': 'нет опыта321'}]
        ]
    
    # await create_vacancies_in_db(vac_list)
    vacancy = await get_vacancy_from_db_by_parameter('exp', 'нет опыта123')
    print(vacancy)

# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())