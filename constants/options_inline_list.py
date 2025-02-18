from constants.company_info import *
from constants.keyboards import *
from constants.messages_text import contacts_info, welcome_text

get_vacancies_options = {
    'risk': 'show_all',
}

but_opt = {
'region': [
    'Выберите регион поиска?',
    
    [
        ['Ставропольский край', 'Ставропольская ГРЭС'],
        ['Ленинградская область', 'Киришская ГРЭС'],
        ['Челябинская область', 'Троицкая ГРЭС'],
        ['Ростовская область', 'Новочеркасская ГРЭС'],
        ['Псковская область', 'Псковская ГРЭС'],
        ['Краснодарский край', 'Адлерская ТЭС'],
        ['Чеченская Республика', 'Грозненская ТЭС'],
        ['Амурская область', 'Свободненская ТЭС'],
        ['Вологодская область', 'Череповецкая ГРЭС'],
        ['Ханты-Мансийский автономный округ - Югра', 'Сургутская ГРЭС-1'],
        ['Рязанская область', 'Рязанская ГРЭС'],
        ['Свердловская область', 'Серовская ГРЭС'],
    ]
],


'vacancies': [
    'Какую работу Вы ищете?\nВыберите нужный пункт.',
    
    [
        ['Все вакансии', 'show_all'],
        ['Вакансии по направлениям деятельности', 'categories'],
        ['Без опыта работы', 'no_exp'],
        ['Главное меню', 'main_menu'],
    ]
],

'show_all': [
    'develop', # добавить вызов функции и определять количество вакансий или добавить в расписанин способ его обновления и тогда просто подставляем готовое значение в текст
    [
        ['Да, я готов 🔍', 'risk'],
        ['Назад', 'vacancies'],
    ]
],
'risk': [
    'will be soon',
    None
],



'categories': [
    'Выберите область профессиональной деятельности.',
    [
        ['Производство', 'power_vacancies'],
        ['Офисные подразделения', 'ofice_vacancies'],
        ['Стажировка', 'duty_vacancies'],
        ['Назад', 'vacancies']
    ]
],
'power_vacancies': [
    'Выберите нужную подкатегорию',
    [
        ['Теплоэнергетика', 'power'],
        ['Электроэнергетика', 'energy'],
        [
            ['АСУ ТП', 'ACY'],
            ['РЗА', 'PZA']
        ],
        [
            ['Ремонт', 'repair'],
            ['Химия', 'chemichal']
        ],
        [
            ['HR', 'powe_HR'],
            ['ИТ', 'pow_IT']
        ],
        [
            ['Экономика', 'pow_economy'],
            ['Сбыт', 'sales']
        ],
        ['Промышленная безопасность и охрана труда', 'pow_safe'],
        ['Другое', 'other'],
        ['Назад', 'categories'],
    ]
],

'power': [
    '0',
    None
],
'energy': [
    '1',
    None
],
'ACY': [
    '2',
    None
],
'PZA': [
    '3',
    None
],
'repair': [
    '4',
    None
],
'chemichal': [
    '5',
    None
],
'powe_HR': [
    '6',
    None
],
'pow_IT': [
    '7',
    None
],

'pow_economy': [
    '8',
    None
],
'sales': [
    '9',
    None
],
'pow_safe': [
    '10',
    None
],
'other': [
    '11',
    None
],


'ofice_vacancies': [
    'Выберите нужную подкатегорию',
    [
        [
            ['Закупки', 'customs'],
            ['Экономика', 'ofi_economy']
        ],
        [
            ['HR', 'ofi_HR'],
            ['Сбыт', 'ofi_sales'],
            ['ИТ', 'ofi_IT']
        ],
        [
            ['Юриспруденция', 'laws'],
            ['Производственное управление', 'prod_control']
        ],
        ['Промышленная безопасность и охрана труда', 'ofi_safe'],
        ['Назад', 'categories']
    ]
],


'customs': [
    '0',
    None
],
'ofi_economy': [
    '1',
    None
],
'ofi_HR': [
    '2',
    None
],
'ofi_sales': [
    '3',
    None
],
'ofi_IT': [
    '4',
    None
],
'laws': [
    '5',
    None
],
'prod_control': [
    '6',
    None
],
'ofi_safe': [
    '7',
    None
],

'duty_vacancies': [
    'Какая-то ошибка',
    None
],

'no_exp': [
    'Какая-то ошибка',
    None
],

'about_company': [
    company_text,
    [
        ['Преимущества работы', 'benefits'],
        ['Филиалы', 'filiales'],
        ['Мотивационные и социальные программы', 'soc_programms'],
        ['Главное меню', 'main_menu'],
    ]
],
'benefits': [
    company_benefit,
    None
],
'filiales': [
    company_filiales,
    None
],
'soc_programms': [
    '👥 Что нас объединяет',
    [
        ['Кадровый резерв и преемственность', 'persons_reserve'],
        ['Обучение и развитие', 'prof_prep'],
        ['Конкурсы профессионального мастерства ', 'prof_masters'],
        ['Спорт', 'sport'],
        ['Культурно-массовые мероприятия', 'mass_events'],
        ['Совет молодых специалистов', 'juns_senate'],
        ['Назад', 'about_company'],
    ]
],
'persons_reserve': [
    motivations_programms[0],
    None
],
'prof_prep': [
    motivations_programms[1],
    None
],
'prof_masters': [
    motivations_programms[2],
    None
],
'sport': [
    motivations_programms[3],
    None
],
'mass_events': [
    motivations_programms[4],
    None
],
'juns_senate': [
    motivations_programms[5],
    None
],


'FQA': [
    'Выберите интересующий вас вопрос',
    [
        ['Какие документы мне понадобятся при трудоустройстве?', 'work_plan'],
        ['Какие карьерные возможности есть в компании?', 'pay_lvl'],
        ['Какие социальные гарантии и льготы мне предоставят?', 'out_cities'],
        ['По какому графику я буду работать?', 'social_garants'],
        ['На какие вакансии я могу претендовать без опыта работы?', 'adresses'],
        ['Кому я могу задать дополнительные вопросы?', 'whiches_no_exp'],
        # ['📝 Какие документы мне понадобятся при трудоустройстве?', 'whiches_docks'],
        # ['🚀 Есть ли в компании возможность карьерного роста?', 'career_grown'],
        ['Главное меню', 'main_menu'],
    ]
],
'work_plan': [
    FAQ[0],
    None
],
'pay_lvl': [
    FAQ[1],
    None
],
'out_cities': [
    FAQ[2],
    None
],
'social_garants': [
    FAQ[3],
    None
],
'adresses': [
    FAQ[4],
    None
],
'whiches_no_exp': [
    FAQ[5],
    None
],


'user_data': [
    '0',
    None
],

'contacts': [
    contacts_info,
    None
],

'admin_soft': [
    'Выберите опцию',
    [
        ['Рассылка', 'postman'],
        ['Главное меню', 'main_menu']
    ]
],

'postman': [
    'postman',
    None
],

'main_menu': [
    welcome_text,
    [
    user_main_menu_keyboard,
    admin_main_menu_keyboard
    ]
]
}