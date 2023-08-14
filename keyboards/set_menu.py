from telebot.types import BotCommand
from telebot import TeleBot

DEFAULT_COMMANDS = (
    ('start', '🚀Запустить бота'),
    ('help', 'ℹСписок команд'),
    ('find_pet', '🦮Подобрать питомца'),
    ('find_org', '🏢Найти организацию'),
    ('history', '🔎Показать историю поиска'),
    ('cancel', '↩Отменить поиск')
)


def set_default_commands(bot: TeleBot) -> None:
    """
    Функция регистрации команд меню бота
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
