from telebot.types import Message
from loader import bot
from lexicon.lexicon_ru import LEXICON_RU
from services.services import reset_state_and_data
from database.database import add_user, User
from logs.logger import Logger


# Этот хэндлер срабатывает на команду /start
@bot.message_handler(commands=['start'])
@Logger.command_log(command='/start')
@add_user
def bot_start(message: Message):
    bot.reply_to(message=message, text=LEXICON_RU['/start'])
    # Сброс состояния до default и хранилища
    Logger.reset_state_and_data(update=message)
    reset_state_and_data(update=message)
