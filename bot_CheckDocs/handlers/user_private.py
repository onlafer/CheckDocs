from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command, CommandStart, or_f

from kbds import create_buttons_inline, getting_the_message_object
from kbds.create_buttons import create_menus

user_private_router = Router()

btns_start_command = create_buttons_inline(
    "🥇 впервые",
    "🏆 уже использовал",
    input_field_placeholder="Вы впервые используете этого бота?",
)
btns_first_use = create_buttons_inline(
    "✅ У меня есть доступ к Техэксперту",
    "❌ У меня нет доступа к Техэксперту",
)
btns_has_access = create_buttons_inline(
    "✅ У меня установлен kAssist",
    "❌ У меня не установлен kAssist (не знаю)",
)
btns_installation_instructions = create_buttons_inline("➡️ Пропустить", "📋 Инструкция")
btns_installating_techexpert = create_buttons_inline(
    "💯 Все получилось", "❌ Вылезла ошибка"
)
btns_installing_kassis = create_buttons_inline(
    "✅ Все получилось", '➡️ 2 вариант (установка kAssist)'
)
btns_step_by_step_verification = create_buttons_inline(
    "👟 Начать проверку документа по шагам", one_time_keyboard=True
)
btns_relevance = create_buttons_inline(
    "🧩 Подробнее про актуальность редакции", " 🎲 Другие виды ссылок"
)
btns_for_links = create_buttons_inline("🔙 Назад", "2️⃣ 2 шаг")
btns_links_to_current_documents = create_buttons_inline(
    "🔙 Обратно", "🎗 Сравнить редакции"
)
btns_another_links_for_second_step = create_buttons_inline(
    "🔙 Обратно", "⛳️ Сравнение стандартов"
)
btns_end_link_verification = create_buttons_inline(
    "🔄 Начать проверку ссылок заново", one_time_keyboard=True
)


kb_main = create_menus(
    main_login="Как войти в систему Техэксперт 🏫",
    main_errors="Ошибки при работе с kAssist (интеграция) 🔎",
    main_functional="Функционал 🌇",
    main_checking_links="Проверить ссылки через 1-2 месяца 🕘",
    main_installation_links="Установка ссылок вручную 🖐",
    about_us="О нас 📞"
)
kb_choosing_a_university = create_menus(
    mos_polytech="Я учусь/работаю в Московском Политехе 🏫",
    another_university="Я из другого ВУЗа/организации 🏡",
)
kb_step_by_step_verification = create_menus(
    placed_links="Расставленные ссылки",
    several_suitable_documents="Фрагменты с несколькими подходящими документами",
    unsuitable_documents="Фрагменты без подходящих документов",
    outside_links="Сторонние ссылки",
)
kb_step_two = create_menus(
    links_to_current_documents="Ссылки на действующие документы",
    links_to_invalid_documents="Ссылки на недействующие документы",
    links_with_special_application="Ссылки с особым применением",
    links_with_irrelevant_information="Ссылки с неактуальной информацией",
    independent_work_with_links="Опции для самостоятельной работы со ссылками и выгрузка отчета",
    unrecognized_text_fragments="Нераспознанные фрагменты текста (текст без ссылок)",
)


# Команда start
@user_private_router.message(or_f(CommandStart(), F.text.lower().endswith("старт")))
async def process_start_command(message: Message):
    await message.answer(
        "<b>Техэксперт</b> - это профессиональные справочные системы для работы с нормативными документами. Узнать подробнее можно в гиде молодого специалиста http://53814571.tilda.ws/"
    )
    await message.answer("Впервые используете бот?", reply_markup=btns_start_command)


# Главное меню бота
@user_private_router.message(
    or_f(
        Command("menu"),
        F.text.lower().endswith("уже использовал"),
        F.text.lower().endswith("меню"),
    )
)
async def get_help_menu(message: Message):
    await message.answer("Навигация", reply_markup=kb_main)
    await message.answer(
        "Нажмите на кнопку навигации, которая вас интересует",
        reply_markup=ReplyKeyboardRemove(),
    )


# не использовал бота
@user_private_router.message(F.text.lower().endswith("впервые"))
async def process_first_use(message: Message):
    await message.answer(
        "<b>Чат-бот поможет:</b>\n"
        "1. Настроить автоматическую проверку файлов большого объема\n\n"
        "2. Повысить качество и оригинальность работы\n\n"
        "3. Приобрести навыки работы с нормативно-технической информацией\n\n",
    )
    await message.answer(
        "У вас есть доступ к <b>Техэксперту</b>?", reply_markup=btns_first_use
    )


# есть доступ к техэксперту
@user_private_router.message(
    F.text.lower().endswith("у меня есть доступ к техэксперту")
    | F.text.lower().endswith("успешная установка")
    | F.text.lower().endswith("пропустить")
)
async def process_there_is_access(message: Message):
    await message.answer(
        "Автоматическая проверка ссылок на нормативную документацию осуществляется с помощью утилиты <b>kAssist</b> (интеграция)",
    )
    await message.answer(
        "У вас установлен <b>kAssist</b>?", reply_markup=btns_has_access
    )


# нет доступа к техэксперту
@user_private_router.callback_query(F.data == "main_login")
@user_private_router.message(
    F.text.lower().endswith("у меня нет доступа к техэксперту")
)
async def process_there_is_no_access(request: Message | CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "1. Доступ из дома с любого усторойства - https://promo.cntd.ru/action/docs?utm_campaign=promo&utm_medium=banner&utm_source=docs\n\n"
        "2. Доступ из МосПолитеха (компьютер должен быть в сети вуза) - http://172.16.3.18:8080/docs/\n\n"
        "3. Корпоративная лицензия (уточняйте в своей компании)\n\n"
        "4. Ссылки на доступ из московских вузов - https://t.me/te_edu/364",
    )
    await message.answer(
        "Автоматическая проверка ссылок на нормативную документацию осуществляется с помощью утилиты <b>kAssist</b> (интеграция)."
    )
    await message.answer(
        "У вас установлен <b>kAssist</b>?", reply_markup=btns_has_access
    )


# алгоритм установки kAssist
@user_private_router.message(
    F.text.lower().endswith("у меня не установлен kassist (не знаю)")
)
async def process_installing_kassist(message: Message):
    await message.answer(
        "Алгоритм установки утилиты <b>kAssist</b>:\n"
        "<b>1 вариант.</b>\n"
        "Проверить наличие приложения <b>Техэксперт</b> на компьютере и запустить систему. После запуска в Word появится надстройка <b>Техэксперт</b>."
    )
    await message.answer_photo(FSInputFile("static/img/kassist_installed.jpeg"))
    await message.answer("Получилось ли у вас установить утилиту <b>kAssist</b>?")
    await message.answer(
        "Если у вас нет приложения, то выберите второй вариант.",
        reply_markup=btns_installing_kassis,
    )


# алгоритм установки Техэксперт
@user_private_router.message(
    F.text.lower().endswith('2 вариант (установка kassist)')
)
async def process_installing_tech_expert(message: Message):
    await message.answer(
        "2 вариант установки зависит от того, какой системой <b>Техэксперт</b> вы пользуетесь:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        "Где вы учитесь/работаете?",
        reply_markup=kb_choosing_a_university,
    )


# скачивание из московского политеха
@user_private_router.callback_query(F.data == "mos_polytech")
async def process_from_mos_polytech(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Скачать установочный пакет (Установить утилиту интеграции справочных систем <b>Техэксперт</b>) по ссылке: http://172.16.3.18:8080"
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-51-44.jpg"))
    await message.answer(
        "Хотите посмотреть инструкцию по установке?",
        reply_markup=btns_installation_instructions,
    )


# скачивание из другого университета
@user_private_router.callback_query(F.data == "another_university")
async def process_from_another_university(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Скачать установочный пакет (Установить утилиту интеграции справочных систем <b>Техэксперт</b>):\n"
        "Открыть браузер, перейти по ссылке в <b>Техэксперт</b>, удалить из адреса ссылки (docs).\n\n"
        "Пример: http://172.16.3.18:8080/"
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-51-44.jpg"))
    await message.answer(
        "Хотите посмотреть инструкцию по установке?",
        reply_markup=btns_installation_instructions,
    )


# инструкция по установке техэксперт
@user_private_router.message(F.text.lower().endswith("инструкция"))
async def process_installation_instructions(message: Message):
    await message.answer(
        "После завершения загрузки необходимо распаковать архив в одноимённую папку.\n\n"
        "Для успешной установки программы перед началом загрузки нужно закрыть приложения, с которыми возможна интеграция:\n"
        "• Microsoft Office;\n"
        "• LibreOffice;\n"
        "• Adobe Acrobat Pro;\n"
        "• Компас 3D;\n• AutoCAD;\n"
        "• Autodesk Inventor;\n"
        "• NanoCAD;\n"
        "• Siemens NX;\n"
        "• Solidworks;\n"
        "• T-Flex CAD и др."
    )
    await message.answer("Открыть распакованную папку и запустить файл setup.exe")
    await message.answer("Установка происходит автоматически")
    await message.answer(
        "Если нужна интреграция с CAD-программами, то:\n"
        "Перейти по вкладке <b>Приложения для интеграции</b> и выбрать нужную программу (поставить галочку в чек-бокс).\n"
        "Подробная видеоинструкция поустановке: https://youtu.be/vPy7vUMHnvk?si=N1qNpNhqPRIcPuh1"
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-49-29 (7).jpg"))
    await message.answer(
        "Если установка прошла успешно, вы увидите на своем экране:"
    )
    await message.answer(
        "Получилось ли у вас установить программу?",
        reply_markup=btns_installating_techexpert,
    )


# успешная установка kAssist
@user_private_router.callback_query(F.data == "main_functional")
@user_private_router.message(
    (F.text.lower().endswith("все получилось"))
    | (F.text.lower().endswith("у меня установлен kassist"))
)
async def process_access_install_kassist(request: Message | CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "На интеллектуальной панели в надстройках Word появятся кнопки:\n"
        "1. <b>Расставить ссылки</b> (связывает фрагмент текста вашего документа с материалами справочной системы);\n\n"
        "2. <b>Проверить ссылки</b> (проверяет актуальность уже расставленных в вашем документе гиперссылок на материалы систем Кодекс/Техэксперт и применяет к ним ряд операций);\n\n"
        "3. <b>Строка поиска</b> (запускает интеллектуальный поиск);\n\n"
        "4. <b>Кнопка вызова справки</b>;\n\n"
        "5. <b>Список источников</b> (какая из систем <b>Кодекс/Техэксперт</b> используется для интеграции);\n\n"
        "6. <b>Кнопка перехода в систему</b>.",
        reply_markup=btns_step_by_step_verification,
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-49-29.jpg"))


# При установке kAssist вылезла ошибка
@user_private_router.callback_query(F.data == "main_errors")
@user_private_router.message(F.text.lower().endswith("вылезла ошибка"))
async def process_user_errors(request: Message | CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "1. Интеграция может не подключиться, если были запущены приложения во время установки.\n\n"
        "2. Интеграция с CAD-программами возможна при наличии прав администратора\n\n"
        "3. Некорректная распаковка архива (все файлы должны распаковаться в папку <b>kAssist</b>)\n\n"
        "4. Ошибка при скачивании архива, архив пустой или неполный. Нужно скачать заново (размер архива более 30 мб.).\n\n"
        "5. Чтобы отключить <b>kAssist</b>, нужно заново запустить файл setup.exe, перейти во вкладку "
        "<b>Приложения для интеграции</b> и передвинуть ползунок в положение выключить. "
        "То же самое нужно сделать и при переустановке <b>kAssist</b>.\n\n"
        "7. Если надстройка интеграции появилась только в одной программе, то нужно перезапустить ПК.",
    )
    await message.answer("Если установка прошла успешно, вы увидите на своем экране ⬇️")
    await message.answer_photo(FSInputFile("static/img/kassist_installed.jpeg"))
    await message.answer(
        "Получилось ли у вас установить программу?",
        reply_markup=btns_step_by_step_verification,
    )


# проверка документа по шагам (шаг 1)
@user_private_router.message(
    (F.text.lower().endswith("начать проверку документа по шагам"))
    | (F.text.lower().endswith("назад"))
    | (F.text.lower().endswith("начать проверку ссылок заново"))
)
async def process_step_by_step_verification(message: Message):
    ReplyKeyboardRemove()
    await message.answer(
        "<b>1 ШАГ.</b>\n"
        "<b>Расставить ссылки</b>.\n"
        "Нажмите на кнопку «Расставить ссылки» на интеллектуальной панели. В появившемся диалоговом окне отобразятся обработанные фрагменты текста, подходящие для установки гиперссылок.\n\n"
        "В результате полуавтоматической расстановки ссылки будут отличаться по цвету в зависимости от статуса документа:\n\n"
        "🔵 синий цвет — для действующих документов;\n\n"
        "🔴 тёмно-красный — для недействующих документов;\n\n"
        "🟠 оранжевый — для документов с особым статусом.\n\n"
        "По итогам анализа текста все гиперссылки будут разделены на 4 группы:",
        reply_markup=kb_step_by_step_verification,
    )
    await message.answer_photo(FSInputFile("static/img/types_of_links.jpg"), reply_markup=ReplyKeyboardRemove())


# расставленные ссылки
@user_private_router.callback_query(F.data == "placed_links")
async def process_placed_links(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Автоматически расставленные гиперссылки (данные фрагменты текста имеют только один подходящий документ) ⬇️",
        reply_markup=btns_for_links,
    )
    await message.answer_photo(FSInputFile("static/img/placed_links.jpg"))


# фрагменты с несколькими подходящими документами
@user_private_router.callback_query(F.data == "several_suitable_documents")
async def process_several_suitable_document(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Фрагменты, имеющие несколько подходящих документов (нужный документ можно выбрать вручную из списка) ⬇️",
        reply_markup=btns_for_links,
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-49-29 (4).jpg"))


# фрагменты без подходящих документов
@user_private_router.callback_query(F.data == "unsuitable_documents")
async def process_unsuitable_documents(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Фрагменты, не имеющие подходящих документов (если выделить документ в тексте курсором, то можно запустить интеллектуальный поиск вручную).\n"
        "Так как иногда kAssist не распознает атрибуты документа, сформулированные некорректно. ⬇️",
        reply_markup=btns_for_links,
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-49-29 (5).jpg"))


# сторонние ссылки
@user_private_router.callback_query(F.data == "outside_links")
async def process_outside_links(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Фрагменты, имеющие сторонние ссылки (kAssist предложит удалить ссылки на сторонние ресурсы или заменить на гиперссылки систем <b>Кодекс</b>/<b>Техэксперт</b>)",
        reply_markup=btns_for_links,
    )


# проверка документа по шагам (шаг 2)
@user_private_router.message(
    (F.text.lower().endswith("обратно")) | (F.text.lower().endswith("2 шаг"))
)
@user_private_router.callback_query(F.data == "main_checking_links")
async def process_step_two(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "<b>2 ШАГ.</b>\n"
        "После обработки всех ссылок нужно запустить проверку ссылок. Нажмите на кнопку <b>Проверить ссылки</b>. Появится окно, содержащее полную информацию о гиперссылках.\n\n"
        "По итогам анализа ссылки будут разделены на 4 группы в окне проверки",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-15_13-49-29 (6).jpg"), reply_markup=kb_step_two)


# ссылки на действующие документы
@user_private_router.callback_query(F.data == "links_to_current_documents")
async def process_links_to_current_documents(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "<b>Ссылки на действующие документы</b>: эти ссылки не требуют дополнительной обработки, кроме правовых документов.\n\n"
        "<b>kAssist</b> по умолчанию ставит ссылки на ту редакцию Кодекса (или ФЗ), которая действует на данный момент.\n\n"
        "Чтобы проверить актуальность редакции, нужно перейти в текст документа и воспользоваться <b>Cервисом документ во времени</b>. ⬇️",
        reply_markup=btns_links_to_current_documents,
    )
    await message.answer_photo(FSInputFile("static/img/current_documents.jpg"))


# ссылки на недействующие документы
@user_private_router.callback_query(F.data == "links_to_invalid_documents")
async def process_links_to_invalid_documents(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "<b>Ссылки на недействующие документы.</b>\n"
        "Для каждого документа из списка реализованы функции:\n"
        "1. Переход к тексту документа;\n\n"
        "2. Указан период действия документа;\n\n"
        "3. Указана действующая редакция документа с возможностью замены ссылки;\n\n"
        "4. Аналитическая работа с документами",
        reply_markup=btns_another_links_for_second_step,
    )
    await message.answer_photo(FSInputFile("static/img/invalid_documents.jpg"))


# ссылки с особым применением
@user_private_router.callback_query(F.data == "links_with_special_application")
async def process_links_with_special_application(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "<b>Ссылки с особым применением.</b>\n"
        "Для каждого документа из списка реализованы функции:\n"
        "1. Переход к тексту документа (ознакомление с особенностями применения);\n\n"
        "2. Указан период действия документа;\n\n"
        "3. Указаны связанные документы;\n\n"
        "4. Переход в службу поддержки пользователя.",
        reply_markup=btns_another_links_for_second_step,
    )
    await message.answer_photo(FSInputFile("static/img/special_application.jpg"))


# ссылки с неактульной информацией
@user_private_router.callback_query(F.data == "links_with_irrelevant_information")
async def process_links_with_irrelevant_information(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "<b>Ссылки с неактуальной информацией.</b>\n"
        "В диалоговом окне необходимо обновить ссылку, пока она не изменит цвет "
        "(синий - действующий документ, красный - отмененнный документ, оранжевый - документ с особым статусом)."
        "Дальнейшая работа см. пункты 1-3",
        reply_markup=btns_another_links_for_second_step,
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-29_13-28-16.jpg"))


# опции для самостоятельной работы со ссылками и выгрузка отчета
@user_private_router.callback_query(F.data == "independent_work_with_links")
async def process_independent_work_with_links(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Опции для самостоятельной работы со ссылками:\n"
        "🔸 Просмотр списка установленных гиперссылок;\n\n"
        "🔹 Открытие документов в системе или удаление гиперссылки;\n\n"
        "🔸 Выделение нужных гиперссылок цветом;\n\n"
        "🔹 Ручной поиск нужного документа в системе, на который будет направлена ссылка.",
        reply_markup=btns_another_links_for_second_step,
    )
    await message.answer_photo(FSInputFile("static/img/photo_2024-04-29_13-59-59.jpg"))


# нераспознанные фрагменты текста (текст без ссылок)
@user_private_router.callback_query(F.data == "unrecognized_text_fragments")
async def process_unrecognized_text_fragments(request: CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "В случае, когда во фрагментах текста есть опечатки, можно просмотреть список данных фрагментов и выбрать дальнейшее действие:\n"
        "- воспользоваться поиском по системе <b>Кодекс</b>/<b>Техэксперт</b> для уточнения информации и самостоятельного создания гиперссылки или оставить фрагмент текста без внимания.",
        reply_markup=btns_another_links_for_second_step,
    )


# сравнить редакции, установка ссылок вручную
@user_private_router.callback_query(F.data == "main_installation_links")
@user_private_router.message(F.text.lower().endswith("сравнить редакции"))
async def process_compare_editions(request: Message | CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Пример проверки редакций\n"
        "1. Перейти в актуальную редакцию Кодекса.\n\n"
        "2. Открыть меню.\n\n"
        "3. Запустить сервис <b>Документ во времени</b>.\n\n"
        "4. Выбрать нужную дату (когда была написана ВКР или другой текст).\n\n"
        "5. Система откроет ту редакцию, которая действовала в эту дату в прошлом.\n\n"
        "6. Сравнить эту редакцию документа и актуальную (вкладка Редакции, подробнее - http://project5381457.tilda.ws/page27082427.html).\n\n"
        "7. Если времени нет, то скопировать ссылку на старую редакцию и поставить ее в текст вручную. Проверить позже. (пункт установка ссылок вручную)",
        reply_markup=btns_another_links_for_second_step,
    )


# Финиш
@user_private_router.callback_query(F.data == "unrecognized_text_fragments")
@user_private_router.message(F.text.lower().endswith("сравнение стандартов"))
async def process_main_installation_links(request: Message | CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.answer(
        "Если вы обнаружили неактуальную ссылку, то рекомендуем вам сравнить редакции документа или открыть сравнение стандартов.\n"
        "Оно доступно по ссылке под названием стандарта, а также во вкладке <b>История документа</b>.\n\n"
        "Подробнее (http://project5381457.tilda.ws/page27082427.html)\n",
        reply_markup=btns_end_link_verification,
    )


# обратная связь
@user_private_router.callback_query(F.data == "about_us")
@user_private_router.message(or_f((Command("about")), F.text.lower().endswith("О нас")))
async def process_feedback(request: Message | CallbackQuery):
    message: Message = getting_the_message_object(request)
    await message.reply(
        "Чат-бот разработан командой студентов МосПолитеха,\n"
        "куратор проекта Н.В. Каширина.\n"
        "Техническая поддержка: kashirina@kodeks.ru\n"
        "Для улучшения работы чат-бота пройдите опрос:\n"
        "https://docs.google.com/forms/d/e/1FAIpQLScUP-xYKGO9OA-5cbegjM_GSdJZ7R_8wmuqDDX2Mks1Mmczhw/viewform?usp=sf_link",
        reply_markup=ReplyKeyboardRemove(),
    )


# Остальные сообщения
@user_private_router.message()
async def other_message(message: Message):
    if message.text in ("Привет", "привет", "hi", "hello"):
        await message.reply("И тебе привет!")
    else:
        await message.reply(
            "🚫 Такой запрос мы не обрабатываем. Напишите /menu или /start, чтобы использовать этого бота."
        )
