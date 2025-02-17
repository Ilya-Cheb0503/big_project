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


ofice_request_translater = {
    'customs': 'Закупки',
    'ofi_economy': 'Экономика',
    'ofi_HR': 'HR',
    'ofi_sales': 'Сбыт',
    'ofi_IT': 'ИТ',
    'laws': 'Юриспруденция',
    'prod_control': 'Производственное управление',
    'ofi_safe': 'Промышленная безопасность и охрана труда',
}

power_request_translater = {
    'power': 'Теплоэнергетика',
    'energy': 'Электроэнергетика',
    'ACY': 'АСУ ТП',
    'PZA': 'РЗА',
    'repair': 'Ремонт',
    'chemichal': 'Химия',
    'powe_HR': 'HR',
    'pow_IT': 'ИТ',
    'pow_economy': 'Экономика',
    'sales': 'Сбыт',
    'pow_safe': 'Промышленная безопасность и охрана труда',
    'other': 'Другое',
}
