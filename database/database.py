from peewee import SqliteDatabase, Model, CharField, IntegerField, \
    DateTimeField, AutoField, ForeignKeyField, IntegrityError
from typing import Callable
from telebot.types import Message
from config_data.config import DB_PATH
import functools
import datetime
from logs.logger import Logger

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """ Базовый класс с указанием БД"""
    class Meta:
        database = db


class User(BaseModel):
    """
    Модель пользователя
    """
    # идентификационный номер пользователя - целочисленное уникальное значение
    user_id = IntegerField(primary_key=True)
    # никнейм
    user_name = CharField(null=True)
    # имя пользователя
    first_name = CharField(null=True)
    # фамилия пользователя (может быть и не указана)
    last_name = CharField(null=True)


class Command(BaseModel):
    """
    Модель команды
    """
    # идентификационный номер команды - целочисленное уникальное значение c автозаполнением
    command_id = AutoField()
    # пользователь, выполнивший команду, с обратной ссылкой (возможность получения команд пользователя: user.commands)
    user = ForeignKeyField(model=User, backref='commands')
    # название команды
    command_name = CharField()
    # дата и время выполнения команды c текущей датой и временем по умолчанию
    date_time = DateTimeField(default=datetime.datetime.now())
    # параметры запроса команды
    params = CharField()
    # кол-во результатов в запросе
    # res_count = IntegerField()


def create_models() -> None:
    """
    Функция создания таблиц моделей-наследников класса BaseModel
    """
    db.create_tables(BaseModel.__subclasses__())


def add_user(func: Callable) -> Callable:
    """
    Декоратор добавления пользователя в таблицу User БД
    при выполнении хэндлера на команду /start
    """
    @functools.wraps(func)
    def wrapper(message: Message) -> None:
        # Обработка исключения при повторном добавлении пользователя
        try:
            Logger.add_user(update=message)
            User.create(
                user_id=message.from_user.id,
                user_name=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
        except IntegrityError:
            Logger.get_warning(update=message, message='Пользователь уже был добавлен в БД')
            pass
        return func(message)
    return wrapper
