from loader import bot
from states.user_states import OrgInformationStates
from keyboards.inline_keyboards import OrgKeyboards, GeneralKeyboards,\
    get_callback_options, change_button
from lexicon.lexicon_ru import LEXICON_RU
from telebot.types import Message, CallbackQuery
from utils.exceptions import ServerError
from services.services import reset_state_and_data, check_res_count, get_req_results_org, ALL_CONTENT_TYPES
from database.database import Command
from logs.logger import Logger


# Этот хэндлер срабатывает на команду /find_org
@bot.message_handler(commands=['find_org'])
@Logger.command_log(command='/find_org')
def find_org(message: Message) -> None:
    # Очистка хранилища при запуске команды в каком-либо из состояний
    if bot.get_state(user_id=message.from_user.id, chat_id=message.chat.id):
        Logger.reset_data(update=message)
        bot.reset_data(user_id=message.from_user.id, chat_id=message.chat.id)
    # Бот принимает состояние location
    Logger.set_state_log(update=message, state=str(OrgInformationStates.location))
    bot.set_state(chat_id=message.from_user.id, state=OrgInformationStates.location, user_id=message.chat.id)
    # отправка пользователю вопроса
    bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['location_org'])


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.location
# при условии передачи текстовых данных
@bot.message_handler(content_types=['text'], state=OrgInformationStates.location)
@Logger.handler_log
def get_location(message: Message) -> None:
    try:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            Logger.record_data(update=message, data=['location'])
            data['location'] = message.text
            Logger.get_info(update=message, message="Начинаю выполнять функцию")
            check_res_count(update=message, method_endswith='get_organizations', params=data,
                            text_key='sort_param', new_state=OrgInformationStates.sort_param,
                            reply_markup=OrgKeyboards.choose_sort_param_markup())
    except ServerError:
        Logger.get_city_warning(update=message)
        bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['none_location_results_org'])


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.location
# при условии передачи НЕ текстовых данных
@bot.message_handler(state=OrgInformationStates.location, content_types=ALL_CONTENT_TYPES)
@Logger.handler_log
def get_location_warning(message: Message) -> None:
    Logger.get_text_type_warning(update=message)
    bot.reply_to(message=message, text=LEXICON_RU['none_text'])


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.sort_param
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=OrgKeyboards.choose_sort_param_markup()), state=OrgInformationStates.sort_param)
@Logger.handler_log
def callback_query_sort(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        Logger.record_data(update=call, data=['sort'])
        data['sort'] = call.data
        bot.send_message(chat_id=call.from_user.id,
                         text=LEXICON_RU['res_count_outcome'])
        Logger.set_state_log(update=call, state=str(OrgInformationStates.res_count))
        bot.set_state(user_id=call.from_user.id,
                      state=OrgInformationStates.res_count)


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.sort_param
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=OrgInformationStates.sort_param)
@Logger.handler_log
def callback_query_sort_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.res_count
# при условии отправки числового значения
@bot.message_handler(state=OrgInformationStates.res_count, func=lambda message: message.text.isdigit())
@Logger.handler_log
def get_res_count(message: Message) -> None:
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        res_count = min(int(message.text), 10)
        Logger.record_data(update=message, data=['limit', 'page'])
        data['limit'] = res_count  # кол-во результатов в запросе
        data['page'] = 1

        # Запись команды и параметров команды в БД
        Logger.add_command_to_db(update=message)
        new_command = Command(
            user_id=message.from_user.id,
            command_name='find_org',
            # пропуск даты и времени (заполняется значением по умолчанию)
            params=str(data)
        )
        new_command.save()

        # Вывод результатов
        get_req_results_org(update=message, method_endswith='get_organizations', params=data)


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.res_count
# при условии отправки НЕ числового значения
@bot.message_handler(state=OrgInformationStates.res_count)
@Logger.handler_log
def get_res_count_warning(message: Message) -> None:
    Logger.get_digit_warning(update=message)
    bot.send_message(chat_id=message.from_user.id, text=LEXICON_RU['not_digit'])


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.change_page
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=GeneralKeyboards.change_page_keyboard()), state=OrgInformationStates.change_page)
@Logger.handler_log
def callback_query_page(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    if call.data == 'change_page':
        with bot.retrieve_data(user_id=call.from_user.id) as data:
            Logger.record_data(update=call, data=['page'])
            data['page'] += 1
            get_req_results_org(update=call, method_endswith='get_organizations', params=data)
    else:
        Logger.reset_state_and_data(update=call)
        reset_state_and_data(update=call)
        bot.send_message(chat_id=call.from_user.id, text=LEXICON_RU['finish'])


# Этот хэндлер срабатывает при нахождении в состоянии OrgInformationStates.change_page
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=OrgInformationStates.change_page)
@Logger.handler_log
def callback_query_page_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состояниях, подразумевающих использование Inline-клавиатуры
# при условии получения в качестве апдейта - сообщения, вместо колбэка
@bot.message_handler(state=[OrgInformationStates.sort_param, OrgInformationStates.change_page])
@Logger.handler_log
def handle_any_message(message: Message) -> None:
    Logger.get_inline_button_warning(update=message)
    bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['wrong_button'])


# Этот хэндлер срабатывает при отправке любого сообщения с учетом отсутствия какого-либо состояния
@bot.message_handler(func=lambda message: True)
@Logger.handler_log
def handle_any_message(message: Message) -> None:
    Logger.get_some_message_warning(update=message)
    bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['some_message'])


# Этот хэндлер срабатывает при нажатии на любую Inline-кнопку с callback-data при отсутствии какого-либо состояния
@bot.callback_query_handler(func=lambda call: call.data)
@Logger.handler_log
def handle_any_call(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['some_callback'], show_alert=True)
