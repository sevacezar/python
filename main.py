from loader import bot
import handlers  # noqa
from telebot.custom_filters import StateFilter
from keyboards.set_menu import set_default_commands
from database.database import create_models
from loguru import logger

if __name__ == '__main__':
    # добавление логгера
    logger.add('logs/bot.log', format='{time:DD.MM.YYYY HH:mm:ss.SSSS} {level} {message}',
               level='INFO', serialize=False)
    #  регистрируем фильтр состояний
    bot.add_custom_filter(custom_filter=StateFilter(bot=bot))
    #  добавляем кнопки меню
    set_default_commands(bot=bot)
    #  создаем модели БД
    create_models()
    #  запускаем бота
    bot.infinity_polling()
