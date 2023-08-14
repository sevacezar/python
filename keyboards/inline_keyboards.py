from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


class PetKeyboards:
    """
    Класс для создания инлайн-клавиатур команды /find_pet
    """
    __btn_info = {'type_default': [{'callback_data': 'Cat', 'text': 'Кошка'},
                                   {'callback_data': 'Dog', 'text': 'Собака'}],
                  'type_custom_dog': [{'callback_data': 'Cat', 'text': 'Кошка'},
                                      {'callback_data': 'Dog', 'text': '🐶Собака'}],
                  'type_custom_cat': [{'callback_data': 'Cat', 'text': '🐱Кошка'},
                                      {'callback_data': 'Dog', 'text': 'Собака'}],
                  'age': [{'callback_data': 'baby', 'text': 'Маленький'},
                          {'callback_data': 'young', 'text': 'Молодой'},
                          {'callback_data': 'adult', 'text': 'Взрослый'},
                          {'callback_data': 'senior', 'text': 'Пожилой'}],
                  'size': [{'callback_data': 'small', 'text': 'Маленький'},
                           {'callback_data': 'medium', 'text': 'Средний'},
                           {'callback_data': 'large', 'text': 'Большой'},
                           {'callback_data': 'xlarge', 'text': 'Очень большой'}],
                  'having_child': [{'callback_data': 'has_child', 'text': 'Да'},
                                   {'callback_data': 'doesnt_have_child', 'text': 'Нет'}],
                  'having_pet': [{'callback_data': 'has_dog', 'text': 'Да, есть собака'},
                                 {'callback_data': 'has_cat', 'text': 'Да, есть кошка'},
                                 {'callback_data': 'has_cat&dog', 'text': 'Да, есть и кошка, и собака'},
                                 {'callback_data': 'doesnt_have_pet', 'text': 'Нет'}],
                  'having_allergy': [{'callback_data': 'has_allergy', 'text': 'Да'},
                                     {'callback_data': 'doesnt_have_allergy', 'text': 'Нет'}],
                  }

    @classmethod
    def choose_pet_markup(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором типа животного

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['type_default'])

    @classmethod
    def choose_pet_markup_dog(cls) -> InlineKeyboardMarkup:
        """
        Функция создания кастомизированной инлайн-клавиатуры с выбранным животным - собакой

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['type_custom_dog'])

    @classmethod
    def choose_pet_markup_cat(cls) -> InlineKeyboardMarkup:
        """
        Функция создания кастомизированной инлайн-клавиатуры с выбранным животным - кошкой

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['type_custom_cat'])

    @classmethod
    def choose_age_markup(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором возраста животного

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['age'])

    @classmethod
    def choose_size_markup(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором размера животного

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['size'])

    @classmethod
    def choose_having_child(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором наличия/отсутствия детей

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['having_child'])

    @classmethod
    def choose_having_pet(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором наличия/отсутствия других животных

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=1, buttons=cls.__btn_info['having_pet'])

    @classmethod
    def choose_having_allergy(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором наличия/отсутствия аллергии на шерсть

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['having_allergy'])


class OrgKeyboards:
    """
    Класс для создания инлайн-клавиатур команды /find_org
    """
    __btn_info = {
                  'sort': [{'callback_data': 'distance', 'text': 'Расстояние⬆'},
                           {'callback_data': '-distance', 'text': 'Расстояние⬇'},
                           {'callback_data': 'name', 'text': 'Имя⬆'},
                           {'callback_data': '-name', 'text': 'Имя⬇'}]
                  }

    @classmethod
    def choose_sort_param_markup(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором параметра сортировки

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['sort'])


class GeneralKeyboards:
    """
    Класс для создания общих инлайн-клавиатур для команд /find_pet и /find_org
    """
    __btn_info = {
                  'change_page': [{'callback_data': 'change_page', 'text': 'Да'},
                                  {'callback_data': 'dont_change_page', 'text': 'Нет'}],
                  }

    @classmethod
    def change_page_keyboard(cls) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором следующей страницы результатов

        :return: инлайн-клавиатура
        """
        return _create_inline_keyboard(row_width=2, buttons=cls.__btn_info['change_page'])


class HistoryKeyboards:
    """
    Класс для создания инлайн-клавиатур для команды /history
    """
    def __init__(self, commands: list):
        """
        Необходимость конструктора вызвана динамичностью данных для кнопок
        """
        self.__commands = commands
        self.__btn_info = self._create_btn_info()

    def _create_btn_info(self) -> list:
        """
        Функция создания списка данных для кнопок команды /history
        """
        btn_info = list()
        for i_command in self.__commands:
            # параметры request-запроса не передаются в коллбэк-дату из-за размера, используем айдишник
            callback_data = i_command.command_id
            date = i_command.date_time.strftime('%Y.%m.%d')
            time = i_command.date_time.strftime('%H:%M')
            command_text = ''
            if i_command.command_name == 'find_pet':
                command_text = '🐕Питомцы'
            elif i_command.command_name == 'find_org':
                command_text = '🏢Организации'
            text = f'📆{date} ⏱{time}\n{command_text}'
            btn_info.append({'callback_data': callback_data, 'text': text})
        return btn_info

    def get_history_markup(self) -> InlineKeyboardMarkup:
        """
        Функция создания инлайн-клавиатуры с выбором исторических запросов
        """
        return _create_inline_keyboard(row_width=1, buttons=self.__btn_info)


def get_callback_options(inline_keyboard: InlineKeyboardMarkup) -> list:
    """
    Функция формирования списка колбэк-информации кнопок определенной клавиатуры

    :param inline_keyboard: Inline-клавиутура
    :return: список колбэк-информации кнопок Inline-клавиатуры
    """
    options = list()
    for i_line in inline_keyboard.keyboard:
        for i_btn in i_line:
            options.append(i_btn.callback_data)
    return options


def _create_inline_keyboard(row_width: int, buttons: list) -> InlineKeyboardMarkup:
    """
    Функция-конструктор инлайн клавиатур

    :param row_width: кол-во кнопок в одном ряду
    :param buttons: ключ словаря __btn_info со значениями необходимых инлайн-кнопок
    :return: объект инлайн-клавиатуру
    """
    markup = InlineKeyboardMarkup(row_width=row_width)
    buttons_list = list()
    for btn in buttons:
        buttons_list.append(InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data']))
    markup.add(*buttons_list)
    return markup


def create_link_keyboard(link: str) -> InlineKeyboardMarkup:
    """
    Функция создания инлайн-клавиатуры с ссылкой

    :param link: ссылка на веб-страницу
    :return: инлайн-клавиатура
    """
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='🌐🦮🐈',
                                  url=link)
    markup.add(button)
    return markup


def change_button(call: CallbackQuery) -> InlineKeyboardMarkup:
    """
    Функция добавляет к нажатой Inline-кнопке эмодзи '✅'

    :param call: callback от нажатой Inline-кнопки
    :return: модифицированная Inline-клавиатура
    """
    new_keyboard = InlineKeyboardMarkup()
    new_keyboard.row_width = 2
    for line in call.message.reply_markup.keyboard:
        button_line = list()
        for btn in line:
            if call.data == btn.callback_data:
                button_line.append(InlineKeyboardButton(text='✅' + btn.text, callback_data=btn.callback_data))
            else:
                button_line.append(btn)
        new_keyboard.add(*button_line)
    return new_keyboard
