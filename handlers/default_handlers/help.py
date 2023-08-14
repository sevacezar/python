from telebot.types import Message
from loader import bot
from lexicon.lexicon_ru import LEXICON_RU
from logs.logger import Logger


# Этот хэндлер срабатывает на команду /help
@bot.message_handler(commands=['help'])
@Logger.command_log(command='/help')
def bot_help(message: Message):
    bot.reply_to(message=message, text=LEXICON_RU['/help'])
