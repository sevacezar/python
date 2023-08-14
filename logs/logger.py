from loguru import logger
from lexicon.lexicon_ru import LOG_RU
from telebot.types import CallbackQuery, Message
from typing import Callable
import functools
from loader import bot


class Logger:
    """
    Класс для работы с логгером loguru
    """
    @staticmethod
    def get_info(update: [CallbackQuery, Message], message: str) -> None:
        logger.info(f'User name: {update.from_user.full_name};\t'
                    f'User ID: {update.from_user.id};\t'
                    f'State: {bot.get_state(user_id=update.from_user.id)};\t'
                    f'Message: {message}')

    @staticmethod
    def get_warning(update: [CallbackQuery, Message], message: str) -> None:
        logger.warning(f'User name: {update.from_user.full_name};\t'
                       f'User ID: {update.from_user.id};\t'
                       f'State: {bot.get_state(user_id=update.from_user.id)};\t'
                       f'Message: {message}')

    @classmethod
    def command_log(cls, command: str) -> Callable:
        """Декоратор с аргументом для логирования выполнения команд"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(update: [CallbackQuery, Message]) -> None:
                cls.get_info(update=update, message=LOG_RU['start_command']+command)
                func(update)
                cls.get_info(update=update, message=LOG_RU['finish_command']+command)
            return wrapper
        return decorator

    @classmethod
    def handler_log(cls, func: Callable) -> Callable:
        """Декоратор для логирования хэндлеров"""
        @functools.wraps(func)
        def wrapper(update: [CallbackQuery, Message]) -> None:
            cls.get_info(update=update, message=LOG_RU['start_handler']+func.__name__)
            func(update)
            cls.get_info(update=update, message=LOG_RU['finish_handler']+func.__name__)
        return wrapper

    @classmethod
    def func_log(cls, func: Callable) -> Callable:
        """Декоратор для логирования вспомогательных функций"""
        @functools.wraps(func)
        def wrapper(update: [CallbackQuery, Message]) -> None:
            cls.get_info(update=update, message=LOG_RU['start_func']+func.__name__)
            func(update)
            cls.get_info(update=update, message=LOG_RU['finish_func']+func.__name__)
        return wrapper

    @classmethod
    def set_state_log(cls, update: [Message, CallbackQuery], state: str) -> None:
        cls.get_info(update=update, message=LOG_RU['set_state']+state)

    @classmethod
    def reset_state_and_data(cls, update: [CallbackQuery, Message]):
        cls.get_info(update=update, message=LOG_RU['reset'])

    @classmethod
    def add_user(cls, update: [CallbackQuery, Message]):
        cls.get_info(update=update, message=LOG_RU['new_db_auth'])

    @classmethod
    def add_command_to_db(cls, update: [CallbackQuery, Message]):
        cls.get_info(update=update, message=LOG_RU['add_command_to_db'])

    @classmethod
    def record_data(cls, update: [CallbackQuery, Message], data: list):
        cls.get_info(update=update, message=LOG_RU['data_record']+', '.join(data))

    @classmethod
    def output_results(cls, update: [CallbackQuery, Message], status: str):
        if status == 'start':
            text = LOG_RU['start_output_results']
        else:
            text = LOG_RU['finish_output_results']
        cls.get_info(update=update, message=text)

    @classmethod
    def reset_data(cls, update: [CallbackQuery, Message]):
        cls.get_info(update=update, message=LOG_RU['reset_data'])

    @classmethod
    def get_city_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['city_warning'])

    @classmethod
    def get_text_type_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['none_text_warning'])

    @classmethod
    def get_inline_button_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['wrong_button_warning'])

    @classmethod
    def get_digit_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['none_digit_warning'])

    @classmethod
    def get_some_message_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['some_message'])

    @classmethod
    def get_none_history_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['none_history'])

    @classmethod
    def get_cancel_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['cancel_warning'])

    @classmethod
    def get_none_results_warning(cls, update: [CallbackQuery, Message]):
        cls.get_warning(update=update, message=LOG_RU['none_results_warning'])
