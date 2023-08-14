from telebot.types import Message
from loader import bot
from lexicon.lexicon_ru import LEXICON_RU
from services.services import reset_state_and_data
from states.user_states import AdditionalStates
from logs.logger import Logger


# Этот хэндлер срабатывает на команду /cancel
# при нахождении в состоянии AdditionalStates.default
@bot.message_handler(commands=['cancel'], state=AdditionalStates.default)
@Logger.command_log(command='/help')
def bot_help(message: Message):
    Logger.get_cancel_warning(update=message)
    bot.reply_to(message=message, text=LEXICON_RU['/cancel_false'])


# Этот хэндлер срабатывает на команду /cancel
# при нахождении в другом состоянии
@bot.message_handler(commands=['cancel'])
@Logger.command_log(command='/help')
def bot_help(message: Message):
    Logger.reset_state_and_data(update=message)
    reset_state_and_data(update=message)
    bot.reply_to(message=message, text=LEXICON_RU['/cancel_true'])
