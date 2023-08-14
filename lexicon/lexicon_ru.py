from keyboards.set_menu import DEFAULT_COMMANDS
from external_services.pet_finder_api import MAX_RES_COUNT


def _create_help_text(commands: tuple[tuple]) -> str:
    """
    Функция формирует текст для команды /help
    """
    text = [f"/{command} - {description}" for command, description in commands]
    return '\n'.join(text)


def create_text_page(current_page: int, total_pages: int) -> str:
    return f'📄Результаты {current_page}-ой страницы из {total_pages} страниц:'


def create_pet_description_text(name: str, gender: str, tags: str, description: str,
                                distance: float, contact_inf: dict) -> str:
    text = f'🔹Имя: {name}\n' \
           f'🔹Пол: {gender}\n' \
           f'🔹Характеристики: {tags}\n' \
           f'🔹Краткое описание: {description}\n' \
           f'🔹Местоположение: {contact_inf["address"]["country"]}, {contact_inf["address"]["city"]}\n' \
           f'🔹Расстояние до питомца: {distance} км\n' \
           f'🔹E-mail для связи: {contact_inf["email"]}'
    return text


def create_org_description_text(name: str, mission_statement: str, address: dict,
                                distance: float) -> str:
    text = f'🔸Название организации: {name}\n' \
           f'🔸Миссия организации: {mission_statement}\n' \
           f'🔸Местоположение: {address["country"]}, {address["city"]}\n' \
           f'🔸Расстояние до организации: {distance} км\n'
    return text


def create_history_text(data: dict, command_name: str) -> str:
    city = data['location']
    text_part = ''
    if command_name == 'find_pet':
        text_part = 'питомца'
    elif command_name == 'find_org':
        text_part = 'организации'
    return f'<b>🔎Результаты поиска {text_part} в городе {city}</b>'


LEXICON_RU = {
    '/start': '<b>👋🏽Привет!</b>\n\nЯ — чат-бот, в котором вы можете подыскать '
              'себе питомца. Для просмотра списка доступных команд '
              'наберите /help',
    '/help': '<b>📋Список доступных команд:</b>\n\n'
             '{}'.format(_create_help_text(DEFAULT_COMMANDS)),
    '/cancel_true': '<b>🛑Выполнение команды прервано</b>\n\nДля просмотра списка доступных команд '
                    'наберите /help',
    '/cancel_false': '<b>Выполнение поиска на данный момент не происходит</b>\n\nДля просмотра списка доступных команд '
                    'наберите /help',
    'none_results': f'😒Результаты, к сожалению, не найдены. \n'
                    f'Попробуйте совершить поиск с другими параметрами, '
                    f'воспользовавшись командой /find_pet',
    'none_location_results': '❌К сожалению, по данному городу информация о питомцах отсутствует.'
                             '\nПопробуйте ввести другой город. '
                             '\nДля отмены поиска вы всегда можете набрать /cancel',
    'res_count': '✔Найденное кол-во результатов: ',
    'location': '🏙В каком городе проживаете?',
    'none_text': '‼Необходимо указать информацию в текстовом формате',
    'pet_type': '🐈🐩Какого питомца подыскиваете?',
    'pet_age': '🧸Выберите желаемый возраст животного',
    'wrong_button': '‼Выберите один из предложенных вариантов нажатием соответствующей кнопки клавиатуры',
    'pet_size': '🐘Выберите желаемый размер питомца',
    'has_child': '🤱🏽Есть ли у вас маленькие дети?',
    'has_pet': '🦎Есть ли у вас другие животные?',
    'has_allergy': '🤧Есть ли у вас аллергия на шерсть?',
    'res_count_outcome': f'📋Сколько результатов показать на странице? (максимум - {MAX_RES_COUNT})',
    'not_digit': '‼Пожалуйста, введите целое число',
    'page': create_text_page,
    'pet_text': create_pet_description_text,
    'learn_more': 'Узнать больше о питомце',
    'show_more': '❓Показать больше результатов?❓',
    'all_results_displayed': '<b>🏁Были выведены все результаты поиска!</b>\n'
                             'Для просмотра списка доступных команд наберите /help',
    'finish': '<b>🏁Поиск завершен!</b>\nДля просмотра списка доступных команд наберите /help',
    'some_message': '‼К сожалению, мой функционал ограничен.. '
                    'Для просмотра списка доступных команд наберите /help',
    'some_callback': '‼Кажется, вы пытаетесь нажать на кнопку, которая на данный момент не активна. '
                     'Для просмотра списка доступных команд наберите /help',
    'location_org': '🏙В каком городе ищете организацию?',
    'none_results_org': f'😒Результаты, к сожалению, не найдены. \n'
                        f'Попробуйте совершить поиск с другими параметрами, '
                        f'воспользовавшись командой /find_org',
    'sort_param': '🔀Выберите параметр сортировки результатов',
    'none_location_results_org': '❌К сожалению, по данному городу информация об организациях отсутствует.'
                                 '\nПопробуйте ввести другой город. '
                                 '\nДля отмены поиска вы всегда можете набрать /cancel',
    'org_text': create_org_description_text,
    'learn_more_org': 'Узнать больше об организации',
    '/history': '<b>📋Вывожу список ваших последних запросов</b>\n '
                'Для вывода результатов запроса нажмите на одну из кнопок ниже',
    'none_history': 'История запросов отсутствует...\n '
                    'Для просмотра списка доступных команд наберите /help',
    'history_res': create_history_text
}


LOG_RU = {
    'start_command': 'Начинаю выполнение команды ',
    'finish_command': 'Завершаю выполнение команды ',
    'reset': 'Сброс состояния до default и данных временного хранилища',
    'reset_data': 'Очистка временного хранилища',
    'start_handler': 'Начинаю выполнение обработчика ',
    'finish_handler': 'Завершаю выполнение обработчика ',
    'start_func': 'Начинаю выполнение вспомогательной функции ',
    'finish_func': 'Завершаю выполнение вспомогательной функции ',
    'set_state': 'Устанавливаю состояние ',
    'new_db_auth': 'Добавление нового пользователя в БД',
    'add_command_to_db': 'Добавление команды в БД',
    'data_record': 'Запись данных во временное хранилище: ',
    'start_output_results': 'Начинаю вывод результатов',
    'finish_output_results': 'Завершаю вывод результатов',
    'city_warning': 'Отсутствуют результаты по введенному городу',
    'none_text_warning': 'Введены НЕ текстовые данные',
    'wrong_button_warning': 'Действие пользователя выполнено вне активной Inline-клавиатуры',
    'none_digit_warning': 'Введено НЕ целое число',
    'some_message': 'Попытка отправки неизвестной команды',
    'none_history': 'История запросов по данному пользователю отсутствует',
    'cancel_warning': 'Попытка выполнить команду /cancel при отсутствии выполнения какой либо другой команды',
    'none_results_warning': 'Результаты по запросу отсутствуют'
}

