import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv('HHRU_CLIENT_ID')
CLIENT_SECRET = os.getenv('HHRU_CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
USER_ACCESS_TOKEN = os.getenv('USER_ACCESS_TOKEN')

request_text = ('Добрый день!\n'
'Меня зовут Илья, я Python разработчик.\n\n'

'У меня есть опыт работы с ОС Linux, Git & GitHub, Nginx, Uvicorn, Docker, Django, Flask, FastAPI, SQLite, PostgreSQL, MySQL, Pydantic, HTML, CSS, Google Cloud Platform и написания как многопоточных, так и асинхронных функций.\n'
'С удовольствием приму участие в работе над вашими проектами самой разной сложности.\n\n'

'Готов применять все имеющиеся навыки для оптимизации и поддержки кода, оттачивать их, а также изучать новое, увеличивая свой вклад в ваш проект.\n'
'Готов выполнить тестовое задание и буду благодарен за обратную связь.\n\n'

'Мои контакты:\n'
'Telegram: @Weddell_Den\n'
'Почта: cheb.ilya05@yandex.ru\n'
'Номер телефона: +7(989)631-95-88\n'
)

admins_id = [787264207, 155771631]

energy_vacancy_keys = {
    "Теплоэнергетика": [
        "машинист котлов",
        "машинист-обходчик",
        "инженер ТТС",
        "инженер",
        "теплоэнергетик",
        "машинист центрального щита",
        "теплотехнической службы",
        "инженер по наладке и испытаниям",
        "турбинное отделение",
        "специалист группы наладки",
        "инженер по расчетам и режимам",
        "теплотехника",
        "машинист энергоблока"
    ],
    "Электроэнергетика": [
        "инженер-электрик",
        "электромонтер по обслуживанию электрооборудования",
        "электротехнической службы",
        "электрического цеха",
        "слесарь по обслуживанию оборудования",
        "электромонтер по ремонту и обслуживанию электрооборудования",
        "по ремонту электротехнического оборудования",
        "слесарь по обслуживанию оборудования электростанций"
    ],
    "АСУ ТП": [
        "АСУ",
        "КИПиА",
        "автоматизации и контроля",
        "инженер-электроник",
        "испытаний и измерений",
        "электрослесарь по обслуживанию автоматики и средств измерений",
        "электрослесарь по ремонту и обслуживанию автоматики и средств измерений",
        "инженер по автоматизированным системам управления производством",
        "по ремонту оборудования КИПиА",
        "по ремонту КИПиА"
    ],
    "РЗА": [
        "электротехнической лаборатории",
        "лаборатории металлов",
        "электромонтер по ремонту аппаратуры",
        "релейной защиты и автоматики"
    ],

    "Ремонт": [
        "по ремонту оборудования котельных и пылеприготовительных цехов",
        "по ремонту парогазотурбинного оборудования",
        "по ремонту приборов и аппаратуры",
        "токарь",
        "по ремонту котельного оборудования",
        "электрогазосварщик",
        "специалист сектора планирования ремонтов",
        "по ремонту химического и топливотранспортного оборудования",
        "электромонтер по ремонту оборудования",
        "машинист мостового крана",
        "электромонтер по ремонту и обслуживанию электрооборудования",
        "по ремонту электротехнического оборудования",
        "слесарь по обслуживанию оборудования электростанций",
        "электрослесарь по ремонту и обслуживанию автоматики и средств измерений",
        "инженер по автоматизированным системам управления производством",
        "по ремонту оборудования КИПиА",
        "по ремонту КИПиА"
    ],

    "Химия": [
        "химводоочистки",
        "химического анализа"
    ],
    "HR": [
        "рекрутер",
        "специалист в отдел кадров ТЭЦ"
    ],
    "ИТ": [
        "инженер-программист"
    ],
    "Экономика": [
        "инженер по расчетам и режимам"
    ],
    "Сбыт": [
        "сектора оптового рынка электроэнергии и учета"
    ],
    "Промышленная безопасность и охрана труда": [
        "по охране труда",
        "по промышленной безопасности"
    ],
    "Другое": [
        "дефектоскопист",
        "по метрологии",
        "техперевооружения",
        "мастер средств связи",
        "службы производственного контроля",
        "взаимодействие с изготовителями",
        "по видеонаблюдению",
        "кладовщик"
    ]
}

ofice_vacancy_keys = {
    
    "Закупки": [
        "отдела закупок"
    ],
    "Экономика": [
        "управления капитальных вложений",
        "по налогам",
        "по финансовому моделированию проектов"
    ],
    "Промышленная безопасность и охрана труда": [
        "по охране труда Юго-западная",
        "по промышленной безопасности Юго-западная"
    ],
    "HR": [
        "специалист по подбору персонала",
        "специалист в отдел кадров",
        "специалист отдела компенсаций и льгот",
        "специалист отдела по развитию персонала"
    ],
    "Сбыт": [
        "службы тарифообразования",
        "анализа сбыта",
        "сбыта",
        "аналитики и прогнозирования",
        "по реализации тепловой энергии"
    ],
    "ИТ": [
        "инженер связи",
        "программист 1C",
        "консультант информационных систем",
        "по ИТ-проектам блока развития"
    ],
    "Юриспруденция": [
        "по правовой работе"
    ],
    "Производственное управление": [
        "экспертизы и технического развития",
        "инженерного управления",
        "вибродиагностики и наладки"
    ]
}
inf_contacts_text = (
    'Специалист свяжется с вами в ближайшее время 📞\n\n'
    'Если вам не терпится связаться с нами, то напишите нам на почту rabota@mosenergo.ru\n'
    'Или позвоните по номеру +7 (495) 957-19-57, доб. 4006\n'
    'Наши специалисты помогут вам!'
)

inf_example_text = 'Для скорейшего ответа, пожалуйста, укажите ваши ФИО и Номер телефона\n\nПример:\n\nИванов Дмитрий ; 8(888)888-88-88'

welcome_text = (
    'Добро пожаловать в официальный бот для работы в ПАО «Мосэнерго»!\n\n'
    'Что может делать этот бот?\n\n'
    'Выдавать актуальные вакансии по ключевым словам.\n'
    'Просто напишите «электрик» или «стажер» в поисковую строку и он выдаст вам результат.\n\n'
    '⦁	Давать ответы на самые частые вопросы\n'
    '⦁	И многое другое!\n\n'
    '👇 Нажмите на меню и попробуйте сами'

)

welcome_two = (
    'Если вы уже готовы приступить к поиску, напишите нам ключевое\nслово вакансии в ответном сообщении, например: «без опыта» или\n«электрик» и мы выдадим вам результаты!'
)

contacts_info = (
    'Адрес: 119526, Москва, проспект Вернадского, д.101, корп.3\n\n'
    'Юридический адрес: 119526, Москва, проспект Вернадского, д.101, корп.3\n\n'
    'Телефон: +7 495 957-19-57\n'
    'Факс: +7 495 957-32-00\n'
    'Электронная почта: mosenergo@mosenergo.ru'
)

FAQ = [
    (
        '🔹 График ДНВВ (Д-день, Н-ночь, В-выходной; День - 08:00-20:00, Ночь - 20:00-08:00):\n'
        '- ГЭС-1\n'
        '- ТЭЦ-20\n'
        '- ТЭЦ-22\n\n'
        '🔹 График ДДННВВВ (Д-день, Н-ночь, В-выходной; День - 08:00-20:00, Ночь - 20:00-08:00):\n'  
        '- ТЭЦ-9\n\n'
        '🔹 График ДДВННВВВ (Д-день, Н-ночь, В-выходной; День - 08:00-20:00, Ночь - 20:00-08:00):\n'  
        '- ТЭЦ-8\n'
        '- ТЭЦ-11\n'
        '- ТЭЦ-12\n'
        '- ТЭЦ-16\n'
        '- ТЭЦ-17\n'
        '- ТЭЦ-21\n'
        '- ТЭЦ-23\n'
        '- ТЭЦ-25\n'
        '- ТЭЦ-26\n'
        '- ТЭЦ-27'
    ),

    (
        'Мы предлагаем конкурентоспособную зарплату.\nБолее подробно готовы обсудить это на собеседовании! 😊 '
    ),

    (
        '- Компенсация расходов на аренду жилья до 31 000 рублей.\n'  
        '- Единовременная выплата при переезде в г. Москву – 93 000 рублей.\n'
        '- Для кандидатов из Московской области предусмотрена компенсация проезда:\n'  
        '  - 18 000 рублей – для дальних городов (Шатура, Коломна, Кашира).\n'
        '  - 3 450 рублей – для населенных пунктов в пределах 60 км от МКАД.'
    ),

    (
        'Мосэнерго заботится о своих сотрудниках и предоставляет:\n'
        '- ДМС со стоматологией после трех месяцев работы\n'  
        '- Страхование жизни\n'
        '- Негосударственное пенсионное обеспечение\n'
        '- Коллективный договор (МГК «Электропрофсоюз»): выплаты и льготы\n'
        '- Компенсация питания в столовых филиалов\n'
    ),

    (
        'ГЭС-1, Москва, ул. Садовническая, д. 11\n'
        'ТЭЦ-8, Москва, Остаповский пр-д, д. 1\n'
        'ТЭЦ-9, Москва, ул. Автозаводская, д. 12, корп.1\n'
        'ТЭЦ-11, Москва, шоссе Энтузиастов, д. 32\n'
        'ТЭЦ-12, Москва, Бережковская наб., д. 16\n'
        'ТЭЦ-16, Москва, ул. 3-я Хорошевская, д. 14\n'
        'ТЭЦ-17, Ступино, ул. Фрунзе, вл. 19\n'
        'ТЭЦ-20, Москва, ул. Вавилова, д. 13\n'
        'ТЭЦ-21, Москва, ул. Ижорская, д. 9\n'
        'ТЭЦ-22, Дзержинский, ул. Энергетиков, д. 5\n'
        'ТЭЦ-23, Москва, ул. Монтажная, д. 1/4\n'
        'ТЭЦ-25, Москва, ул. Генерала Дорохова, д. 16\n'
        'ТЭЦ-26, Москва, Востряковский пр-д, домовладение 10\n'
        'ТЭЦ-27, Мытищинский район, п. Челобитьево, Волковское шоссе 1\n'
        'ТЭЦ-30, Павловский Посад, Большой Железнодорожный пр., 25А\n'
    ),

    (
        '<u>Список начальных вакансий без опыта и профильного образования:</u>\n'
        '- Машинист-обходчик по котельному / турбинному оборудованию\n'
        '- Аппаратчик ХВО\n'
        '- Машинист насосных установок\n\n'

        '<u>Начальные вакансии, на которые можно прийти без опыта после окончания вуза/ссуза:</u>\n'
        '- Машинист-обходчик по котельному / турбинному оборудованию\n'
        '- Аппаратчик ХВО\n'
        '- Машинист насосных установок\n'
        '- Электромонтер по ремонту и обслуживанию электрооборудования электростанции\n'
        '- Электрослесарь по ремонту и обслуживанию автоматики и средств измерений электростанции\n'
        '- Слесарь по ремонту парогазотурбинного оборудования\n'
        '- Слесарь по ремонту оборудования котельных и пылеприготовительных цехов\n'
        '- Лаборант химического анализа\n'
    ),
    
    (
        'Список документов, необходимых для трудоустройства:\n'
        '- Паспорт РФ\n'
        '- Документы об образовании\n'
        '- СНИЛС\n'
        '- ИНН\n'
        '- Трудовая книжка\n'
        '- Документы воинского учета\n'
    ),
   
    (
        'В компании существуют программы для профессионального и карьерного развития:\n'
        '- Кадровый резерв\n'
        '- Программы подготовки по должности\n'
        '- Наставничество\n'
        '- Профессиональная переподготовка и повышение квалификации за счет работодателя\n'
        '- Соревнования профессионального мастерства\n'
        '- Ротации между филиалами\n'
    ),
]



motivations_programms = [
    ('Наша компания ценит своих сотрудников и предоставляет\n'
     'возможность развиваться до руководящих позиций\n'
     'благодаря программе кадрового резерва 👥'),

    ('Поддержание уровня квалификации сотрудников — один\n'
    'из главных приоритетов Мосэнерго. Поэтому, помимо\n'
    'обучения в корпоративном Учебном центре, у вас есть\n'
    'шанс пройти профпереподготовку или повысить\n'
    'квалификацию по профильному направлению в НИУ МЭИ 📚'),

    ('Сотрудники Мосэнерго ежегодно демонстрируют свой\n'
    'профессионализм не только на рабочих местах, но и на\n'
    'соревнованиях по оперативной работе, ремонту, охране\n'
    'труда, пожарной безопасности и многих других\n'
    'направлениях!🏆'),

    ('Движение — это жизнь! Ежегодно мы проводим более 40\n'
    'спортивных соревнований по различным видам спорта: от\n'
    'футбола до шахмат, и даже по игре в городки!⚽'),

    ('В нашей компании вы можете развиваться не только\n'
    'профессионально, но и творчески. Концерты, фестивали,\n'
    'конкурсы — это отличная возможность проявить свои\n'
    'скрытые таланты! 🎉'),

    ('Хотите найти единомышленников и почувствовать себя\n'
    'частью большой команды, принять участие в интересных\n'
    'мероприятиях? Присоединяйтесь к совету молодых\n'
    'специалистов! 🤝\n\n'
    'Вместе мы достигнем больших высот! 🔝'),
]



company_text = (
'🌟 ПАО «Мосэнерго» — крупнейшая территориальная генерирующая компания в России! 🌍\n\n'
'В состав «Мосэнерго» входит 15 теплоэлектроцентралей, расположенных в Москве и Московской области, а также районные и квартальные тепловые станции.\n\n'
'💡 Наши производственные объекты обеспечивают более 50% электрической энергии, потребляемой в Московском регионе, и около 90% потребностей Москвы в тепловой энергии.\n\n'
'👷‍♂️ Численность персонала компании — более 7 тысяч человек!'
)
company_benefit = (
'✨ Оформление по ТК, стабильная выплата заработной платы 2 раза в месяц, премии и надбавки.\n\n'
'🏡 Возможность работать рядом с домом – на одной из 15 ТЭЦ.\n\n'
'🍽️ Компенсация питания в столовых филиалов.\n\n'
'🚛 Для иногородних кандидатов: компенсация переезда, аренды жилья и проезда из дальних городов МО.\n\n'
'🏥 ДМС со стоматологией после трех месяцев работы.\n\n'
'💼 Страхование жизни и негосударственное пенсионное обеспечение.\n\n'
'🤝 Коллективный договор (МГК «Электропрофсоюз»): выплаты и льготы.\n\n'
'🛡️ Обеспечение средствами индивидуальной защиты и спецодеждой.'
)
company_filiales = (
'📍 ГЭС-1: Москва, ул. Садовническая, д. 11\n'
'📍 ТЭЦ-8: Москва, Остаповский пр-д, д. 1\n'
'📍 ТЭЦ-9: Москва, ул. Автозаводская, д. 12, корп. 1\n'
'📍 ТЭЦ-11: Москва, шоссе Энтузиастов, д. 32\n'
'📍 ТЭЦ-12: Москва, Бережковская наб., д. 16\n'
'📍 ТЭЦ-16: Москва, ул. 3-я Хорошевская, д. 14\n'
'📍 ТЭЦ-17: Ступино, ул. Фрунзе, вл. 19\n'
'📍 ТЭЦ-20: Москва, ул. Вавилова, д. 13\n'
'📍 ТЭЦ-21: Москва, ул. Ижорская, д. 9\n'
'📍 ТЭЦ-22: Дзержинский, ул. Энергетиков, д. 5\n'
'📍 ТЭЦ-23: Москва, ул. Монтажная, д. 1/4\n'
'📍 ТЭЦ-25: Москва, ул. Генерала Дорохова, д. 16\n'
'📍 ТЭЦ-26: Москва, Востряковский пр-д, домовладение 10\n'
'📍 ТЭЦ-27: Мытищинский район, п. Челобитьево, Волковское шоссе, 1'
)
company_motivation_programms = (
'🏆 Кадровый резерв.\n\n'
'📚 Профессиональная переподготовка и повышение квалификации за счет работодателя.\n\n'
'🥇 Соревнования профессионального мастерства.\n\n'
'⚽ Спортивные соревнования.\n\n'
'🎉 Корпоративные культурно-массовые мероприятия.\n\n'
'👩‍🎓 Совет молодых специалистов.\n\n\n'

'Присоединяйтесь к нашей команде и развивайте свою карьеру в «Мосэнерго»! 💡🚀'
)