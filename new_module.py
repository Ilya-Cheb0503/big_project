import asyncio
import json

from databases import Database
from sqlalchemy import JSON, Column, Integer, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Vacancy_hh(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(Integer, unique=True)
    vacancy_inf = Column(JSON, nullable=True)

DATABASE_URL_CREATE = "sqlite:///./vacancies_upd.db"
DATABASE_URL = "sqlite:///./vacancies.db"
database = Database(DATABASE_URL)
database_update = Database(DATABASE_URL_CREATE)


async def save_vacancy(vacancy_id: int, vacancy_inf: dict = None):
    existing_vacancy = await get_vacancy_by_vacancy_id(vacancy_id, database_update)
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
    await database_update.execute(query, values)


async def filling_vacancies_to_db(vacancies_data):
    await database_update.connect()
    
    for vacancy in vacancies_data:
        vacancy_id = vacancy.pop('id Вакансии')
        # vacancy_id, vacancy_inf = vacancy
        await save_vacancy(vacancy_id=vacancy_id, vacancy_inf=vacancy)
    
    await database_update.disconnect()


async def get_vacancy_by_vacancy_id(vacancy_id: int, db=database):
    await db.connect()

    query = select(Vacancy_hh).where(Vacancy_hh.vacancy_id == vacancy_id)
    vacancy = await db.fetch_one(query)
    
    await db.disconnect()

    return vacancy


async def get_vacancies_by_key_word_module(key_word):
    await database.connect()
    
    query = select(Vacancy_hh)
    result_list = []
    results = await database.fetch_all(query)
    for vac in results:
        
        vacancy_name = vac.vacancy_inf['Вакансия']
        vacancy_req = vac.vacancy_inf['Требования']
        vacancy_resp = vac.vacancy_inf['Обязанности']

        if key_word in (vacancy_name or vacancy_req or vacancy_resp):
            result_list.append(vac)

    await database.disconnect()

    return result_list


async def get_vacancies_by_keys_list_module(key_words_list):
    await database.connect()
    
    query = select(Vacancy_hh)
    result_list = []
    results = await database.fetch_all(query)
    for vac in results:
        for key_word in key_words_list:
        
            vacancy_name = vac.vacancy_inf['Вакансия']
            vacancy_req = vac.vacancy_inf['Требования']
            vacancy_resp = vac.vacancy_inf['Обязанности']

            if key_word in (vacancy_name or vacancy_req or vacancy_resp):
                result_list.append(vac)

    await database.disconnect()

    return result_list


async def get_no_exp_vacancies_module():
    await database.connect()

    option_name = "Наличие опыта"
    option_value = "Нет опыта"

    query = select(Vacancy_hh)
    result_list = []
    results = await database.fetch_all(query)
    for vac in results:
        if vac.vacancy_inf[option_name] == option_value:
            result_list.append(vac)

    await database.disconnect()

    return result_list


async def get_all_vacancies_module():
    await database.connect()

    query = select(Vacancy_hh)
    results = await database.fetch_all(query)

    await database.disconnect()

    return results


async def start_create_table(DATABASE_URL):
    await database.connect()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    await database.disconnect()


async def main():
    await start_create_table(DATABASE_URL)


if __name__ == '__main__':
    asyncio.run(main())

    