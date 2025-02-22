from constants.company_info import *
from constants.keyboards import *
from constants.messages_text import contacts_info, welcome_text, social_media

get_vacancies_options = {
    'risk': 'show_all',
}

but_opt = {
'vacancies': [
    'Что именно вас интересует ?',
    [
        ['Посмотреть все вакансии', 'show_all'],
        ['Категории', 'categories'],
        ['Вакансии без опыта', 'no_exp'],
        ['Главное меню', 'main_menu'],
    ]
],

'show_all': [
    'develop', # добавить вызов функции и определять количество вакансий или добавить в расписанин способ его обновления и тогда просто подставляем готовое значение в текст
    [
        ['Рискну', 'risk'],
        ['Главное меню', 'main_menu'],
    ]
],
'risk': [
    'will be soon',
    None
],



'categories': [
    'Выберите нужную категорию',
    [
        ['ТЭЦ', 'power_vacancies'],
        ['Офис', 'ofice_vacancies'],
        ['Стажировка', 'duty_vacancies'],
        ['Главное меню', 'main_menu']
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
        ['Главное меню', 'main_menu'],
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
        ['Главное меню', 'main_menu']
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
    'Выберите интересующий пункт',
    [
        ['Кадровый резерв', 'persons_reserve'],
        ['Профессиональная подготовка и повышение квалификации за счет работодателя', 'prof_prep'],
        ['Соревнования профессионального мастерства', 'prof_masters'],
        ['Спортивные соревнования', 'sport'],
        ['Корпоративные культурно-массовые мероприятия', 'mass_events'],
        ['Совет молодых специалистов', 'juns_senate'],
        ['Главное меню', 'main_menu'],
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
        ['💼 По какому графику я буду работать?', 'work_plan'],
        ['💰 Какой уровень заработной платы мне ожидать?', 'pay_lvl'],
        ['🏠 Какие компенсации существуют для иногородних кандидатов?', 'out_cities'],
        ['🛡️ Какие социальные гарантии предоставляет Мосэнерго?', 'social_garants'],
        ['📍 Адреса ТЭЦ Мосэнерго ГЭС-1', 'adresses'],
        ['👩‍🏫 На какие должности можно прийти без опыта?', 'whiches_no_exp'],
        ['📝 Какие документы мне понадобятся при трудоустройстве?', 'whiches_docks'],
        ['🚀 Есть ли в компании возможность карьерного роста?', 'career_grown'],
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
'whiches_docks': [
    FAQ[6],
    None
],
'career_grown': [
    FAQ[7],
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

'social_media' : [
    social_media,
    None
],

'admin_soft': [
    'Выберите опцию',
    [
        ['Рассылка', 'postman'],
        ['Метрика', 'analiz'],
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