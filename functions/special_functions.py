from functions.user_data_form import user_full_information_process
from settings import logging


async def check_for_empty_list(result):
    return result == []


async def list_waiting(update, context):
    logging.info('ВЫЗВАЛИ list_waitnig')
    
    if 'Запрос full данных' not in context.user_data:
        # await update.message.reply_text(text_wait, reply_markup=reply_markup)
        context.user_data['Запрос full данных'] = 'Запуск анкетирования'
        context.user_data['information_form'] = {}
    await user_full_information_process(update, context)

    logging.info('ЗАВЕРШИЛИ list_waitnig')
