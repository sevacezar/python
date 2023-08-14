from loader import bot
from states.user_states import PetInformationStates
from keyboards.inline_keyboards import PetKeyboards, GeneralKeyboards,\
    get_callback_options, change_button
from lexicon.lexicon_ru import LEXICON_RU
from telebot.types import Message, CallbackQuery
from utils.exceptions import ServerError
from services.services import reset_state_and_data, check_res_count, get_req_results_pet, ALL_CONTENT_TYPES
from database.database import Command
from logs.logger import Logger


# Этот хэндлер срабатывает на команду /find_pet
@bot.message_handler(commands=['find_pet'])
@Logger.command_log(command='/find_pet')
def find_pet(message: Message) -> None:
    # Очистка хранилища при запуске команды в каком-либо из состояний
    if bot.get_state(user_id=message.from_user.id, chat_id=message.chat.id):
        Logger.reset_data(update=message)
        bot.reset_data(user_id=message.from_user.id, chat_id=message.chat.id)
    # Бот принимает состояние location
    Logger.set_state_log(update=message, state=str(PetInformationStates.location))
    bot.set_state(chat_id=message.from_user.id, state=PetInformationStates.location, user_id=message.chat.id)
    # отправка пользователю вопроса
    bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['location'])


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.location
# при условии передачи текстовых данных
@bot.message_handler(content_types=['text'], state=PetInformationStates.location)
@Logger.handler_log
def get_location(message: Message) -> None:
    try:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            Logger.record_data(update=message, data=['location'])
            data['location'] = message.text
            check_res_count(update=message, method_endswith='get_animals', params=data, text_key='pet_type',
                            new_state=PetInformationStates.pet_type, reply_markup=PetKeyboards.choose_pet_markup())
    except ServerError:
        Logger.get_city_warning(update=message)
        bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['none_location_results'])


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.location
# при условии передачи НЕ текстовых данных
@bot.message_handler(state=PetInformationStates.location, content_types=ALL_CONTENT_TYPES)
@Logger.handler_log
def get_location_warning(message: Message) -> None:
    Logger.get_text_type_warning(update=message)
    bot.reply_to(message=message, text=LEXICON_RU['none_text'])


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.pet_type
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=PetKeyboards.choose_pet_markup()), state=PetInformationStates.pet_type)
@Logger.handler_log
def callback_query_type(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    if call.data == 'Dog':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=PetKeyboards.choose_pet_markup_dog())
    elif call.data == 'Cat':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=PetKeyboards.choose_pet_markup_cat())

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        Logger.record_data(update=call, data=['type'])
        data['type'] = call.data
        check_res_count(update=call, method_endswith='get_animals', params=data, text_key='pet_age',
                        new_state=PetInformationStates.pet_age, reply_markup=PetKeyboards.choose_age_markup())


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.pet_type
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data,
                            state=PetInformationStates.pet_type)
@Logger.handler_log
def callback_query_type_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.pet_age
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=PetKeyboards.choose_age_markup()), state=PetInformationStates.pet_age)
@Logger.handler_log
def callback_query_age(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        Logger.record_data(update=call, data=['age'])
        data['age'] = call.data
        check_res_count(update=call, method_endswith='get_animals', params=data, text_key='pet_size',
                        new_state=PetInformationStates.pet_size, reply_markup=PetKeyboards.choose_size_markup())


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.pet_age
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=PetInformationStates.pet_age)
@Logger.handler_log
def callback_query_age_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.pet_size
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=PetKeyboards.choose_size_markup()), state=PetInformationStates.pet_size)
@Logger.handler_log
def callback_query_size(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        Logger.record_data(update=call, data=['size'])
        data['size'] = call.data
        check_res_count(update=call, method_endswith='get_animals', params=data, text_key='has_child',
                        new_state=PetInformationStates.has_child, reply_markup=PetKeyboards.choose_having_child())


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.pet_size
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=PetInformationStates.pet_size)
@Logger.handler_log
def callback_query_size_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.has_child
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=PetKeyboards.choose_having_child()), state=PetInformationStates.has_child)
@Logger.handler_log
def callback_query_child(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        if call.data == 'has_child':
            Logger.record_data(update=call, data=['good_with_children'])
            data['good_with_children'] = 1
        check_res_count(update=call, method_endswith='get_animals', params=data, text_key='has_pet',
                        new_state=PetInformationStates.has_pet, reply_markup=PetKeyboards.choose_having_pet())


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.has_child
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=PetInformationStates.has_child)
@Logger.handler_log
def callback_query_child_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.has_pet
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=PetKeyboards.choose_having_pet()), state=PetInformationStates.has_pet)
@Logger.handler_log
def callback_query_pets(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        if call.data == 'has_dog':
            Logger.record_data(update=call, data=['good_with_dogs'])
            data['good_with_dogs'] = 1
        elif call.data == 'has_cat':
            Logger.record_data(update=call, data=['good_with_cats'])
            data['good_with_cats'] = 1
        elif call.data == 'has_cat&dog':
            Logger.record_data(update=call, data=['good_with_dogs', 'good_with_cats'])
            data['good_with_dogs'] = 1
            data['good_with_cats'] = 1
        check_res_count(update=call, method_endswith='get_animals', params=data, text_key='has_allergy',
                        new_state=PetInformationStates.has_allergy, reply_markup=PetKeyboards.choose_having_allergy())


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.has_pet
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=PetInformationStates.has_pet)
@Logger.handler_log
def callback_query_pets_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.has_allergy
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=PetKeyboards.choose_having_allergy()), state=PetInformationStates.has_allergy)
@Logger.handler_log
def callback_query_allergy(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    # Кастомизация выбранной кнопки
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=change_button(call=call))

    with bot.retrieve_data(user_id=call.from_user.id) as data:
        if call.data == 'has_allergy':
            Logger.record_data(update=call, data=['coat'])
            data['coat'] = 'hairless'
        check_res_count(update=call, method_endswith='get_animals', params=data, text_key='res_count_outcome',
                        new_state=PetInformationStates.res_count)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.has_allergy
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=PetInformationStates.has_allergy)
@Logger.handler_log
def callback_query_allergy_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.res_count
# при условии отправки числового значения
@bot.message_handler(state=PetInformationStates.res_count, func=lambda message: message.text.isdigit())
@Logger.handler_log
def get_res_count(message: Message) -> None:
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        res_count = min(int(message.text), 10)
        Logger.record_data(update=message, data=['sort', 'limit', 'page'])
        data['sort'] = 'distance'
        data['limit'] = res_count  # кол-во результатов в запросе
        data['page'] = 1

        # Запись команды и параметров команды в БД
        Logger.add_command_to_db(update=message)
        new_command = Command(
            user_id=message.from_user.id,
            command_name='find_pet',
            # пропуск даты и времени (заполняется значением по умолчанию)
            params=str(data),
        )
        new_command.save()

        # вывод результатов
        get_req_results_pet(update=message, method_endswith='get_animals', params=data)


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.res_count
# при условии отправки НЕ числового значения
@bot.message_handler(state=PetInformationStates.res_count)
@Logger.handler_log
def get_res_count_warning(message: Message) -> None:
    Logger.get_digit_warning(update=message)
    bot.send_message(chat_id=message.from_user.id, text=LEXICON_RU['not_digit'])


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.change_page
# при условии нажатой кнопки Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data in get_callback_options(
    inline_keyboard=GeneralKeyboards.change_page_keyboard()), state=PetInformationStates.change_page)
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
            get_req_results_pet(update=call, method_endswith='get_animals', params=data)
    else:
        Logger.reset_state_and_data(update=call)
        reset_state_and_data(update=call)
        bot.send_message(chat_id=call.from_user.id, text=LEXICON_RU['finish'])


# Этот хэндлер срабатывает при нахождении в состоянии PetInformationStates.change_page
# при условии нажатой кнопки ДРУГОЙ Inline-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data, state=PetInformationStates.change_page)
@Logger.handler_log
def callback_query_page_wrong(call: CallbackQuery) -> None:
    Logger.get_inline_button_warning(update=call)
    bot.answer_callback_query(callback_query_id=call.id, text=LEXICON_RU['wrong_button'], show_alert=True)


# Этот хэндлер срабатывает при нахождении в состояниях, подразумевающих использование Inline-клавиатуры
# при условии получения в качестве апдейта - сообщения, вместо колбэка
@bot.message_handler(state=[PetInformationStates.pet_type, PetInformationStates.pet_age,
                            PetInformationStates.pet_size, PetInformationStates.has_child,
                            PetInformationStates.has_pet, PetInformationStates.has_allergy,
                            PetInformationStates.change_page])
@Logger.handler_log
def handle_any_message(message: Message) -> None:
    Logger.get_inline_button_warning(update=message)
    bot.send_message(chat_id=message.chat.id, text=LEXICON_RU['wrong_button'])
