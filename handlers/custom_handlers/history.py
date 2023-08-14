from loader import bot
from telebot.types import Message, CallbackQuery
from states.user_states import AdditionalStates
from database.database import Command, User
from keyboards.inline_keyboards import HistoryKeyboards, change_button
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_info_by_command_id, get_req_results_pet, get_req_results_org
from logs.logger import Logger


# Этот хэндлер срабатывает на команду /history
@bot.message_handler(commands=['history'])
@Logger.command_log(command='/history')
def get_history(message: Message) -> None:
    # Очистка хранилища
    Logger.reset_data(update=message)
    bot.reset_data(user_id=message.from_user.id, chat_id=message.chat.id)

    user_id = message.from_user.id
    user = User.get(User.user_id == user_id)

    # Формирование списка команд пользователя
    commands: list[Command] = user.commands.order_by(-Command.date_time).limit(10)

    if commands:
        # Формирование списка кнопок Inline-клавиатуры
        bot.send_message(chat_id=message.from_user.id, text=LEXICON_RU['/history'],
                         reply_markup=HistoryKeyboards(commands=commands).get_history_markup())
    else:
        Logger.get_none_history_warning(update=message)
        bot.send_message(chat_id=message.from_user.id, text=LEXICON_RU['none_history'])
        # Бот принимает состояние AdditionalStates.default
        Logger.set_state_log(update=message, state=str(AdditionalStates.default))
        bot.set_state(chat_id=message.from_user.id, state=AdditionalStates.default, user_id=message.chat.id)


# Этот хэндлер срабатывает при условии нажатой кнопки Inline-клавиатуры
# с callback-датой в цифровом формате,
# чтобы можно было в любом состоянии выводить исторические результаты
@bot.callback_query_handler(func=lambda call: call.data.isdigit())
@Logger.handler_log
def callback_query_history(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)

    # Кастомизация выбранной кнопки при отсутствии более ранней кастомизации
    for line in call.message.reply_markup.keyboard:
        for btn in line:
            if btn.callback_data == call.data and '✅' not in btn.text:
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=change_button(call=call))
    Logger.set_state_log(update=call, state=str(AdditionalStates.default))
    bot.set_state(user_id=call.from_user.id, state=AdditionalStates.default)
    with bot.retrieve_data(user_id=call.from_user.id) as data:
        info = get_info_by_command_id(command_id=int(call.data))
        for i_key, i_value in info['params'].items():
            Logger.record_data(update=call, data=[i_key])
            data[i_key] = i_value
        bot.send_message(chat_id=call.from_user.id, text=LEXICON_RU['history_res'](data=data,
                                                                                   command_name=info['command_name']))
        if info['command_name'] == 'find_pet':
            get_req_results_pet(update=call, method_endswith='get_animals', params=data)
        elif info['command_name'] == 'find_org':
            get_req_results_org(update=call, method_endswith='get_organizations', params=data)
