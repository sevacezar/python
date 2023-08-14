import json
import time
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto
from telebot.handler_backends import State
from lexicon.lexicon_ru import LEXICON_RU
from external_services.pet_finder_api import PetFinderReq
from keyboards.inline_keyboards import create_link_keyboard, GeneralKeyboards
from states.user_states import PetInformationStates, OrgInformationStates, AdditionalStates
from database.database import Command
from logs.logger import Logger
from loader import bot


ALL_CONTENT_TYPES = ['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact']


def reset_state_and_data(update: [Message, CallbackQuery]) -> None:
    """
    Функция очистки состояний и временного хранилища данных
    """
    Logger.set_state_log(update=update, state=str(AdditionalStates.default))
    bot.reset_data(user_id=update.from_user.id)
    bot.set_state(user_id=update.from_user.id, state=AdditionalStates.default)


def check_res_count(update: [Message, CallbackQuery], method_endswith: str, params: dict,
                    text_key: str, new_state: State, reply_markup: InlineKeyboardMarkup = None) -> None:
    """
    Функция проверки кол-ва результатов в запросе.
    """
    # Запрос к API
    check_result = PetFinderReq.get_request(method_endswith=method_endswith, params=params)
    # Определение общего кол-ва результатов в запросе
    total_res = check_result['pagination']['total_count']
    if total_res == 0:
        Logger.get_none_results_warning(update=update)
        # уведомление пользователя об отсутствии результатов в запросе
        text = ''
        if method_endswith == 'get_animals':
            text = LEXICON_RU['none_results']
        elif method_endswith == 'get_organizations':
            text = LEXICON_RU['none_results_org']
        bot.send_message(chat_id=update.from_user.id, text=text)
        # очистка хранилища и состояния
        reset_state_and_data(update=update)
    else:
        # отправка пользователю кол-ва найденных результатов
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['res_count'] + str(total_res))
        # отправка пользователю следующего вопроса
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU[text_key],
                         reply_markup=reply_markup)
        # бот принимает новое состояние
        Logger.set_state_log(update=update, state=str(new_state))
        bot.set_state(user_id=update.from_user.id, state=new_state)


def get_req_results_pet(update: [Message, CallbackQuery], method_endswith: str, params: dict) -> None:
    """
    Функция отправляет пользователю результаты запроса.
    """
    req = PetFinderReq.get_request(method_endswith=method_endswith, params=params)
    total_pages = req['pagination']['total_pages']
    current_page = req['pagination']['current_page']
    bot.send_message(chat_id=update.from_user.id,
                     text=LEXICON_RU['page'](current_page=current_page, total_pages=total_pages))
    Logger.output_results(update=update, status='start')
    # цикл по животным
    for i_pet in req['animals']:
        name: str = i_pet['name']
        gender: str = i_pet['gender']
        tags: str = ', '.join(i_pet['tags']) if i_pet['tags'] else '-'
        description: str = i_pet['description']
        photos: list = i_pet['photos']
        distance: float = round(i_pet['distance'] * 1.61, 2)  # перевод из миль в км
        contact: dict = i_pet['contact']
        url = i_pet['url']
        text = LEXICON_RU['pet_text'](name=name, gender=gender, tags=tags, description=description,
                                      distance=distance, contact_inf=contact)

        if len(photos) == 0:
            # При отсутствии фотографий - отправляется обычное сообщение
            bot.send_message(chat_id=update.from_user.id, text=text)
        else:
            # формирование списка с фото питомца
            media = list()
            for i_index, i_photo in enumerate(photos):
                if i_index == 0:
                    media.append(InputMediaPhoto(media=i_photo['full'], caption=text))
                else:
                    media.append(InputMediaPhoto(media=i_photo['full']))
            # отправка пользователю фото питомца и текста с описанием
            bot.send_media_group(chat_id=update.from_user.id, media=media)

        # отправка пользователю ссылки на страницу с питомцем на сайте
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['learn_more'],
                         reply_markup=create_link_keyboard(link=url))
        time.sleep(1.5)
    Logger.output_results(update=update, status='finish')

    #  Проверка, выведены ли все доступные результаты
    if current_page < total_pages:
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['show_more'],
                         reply_markup=GeneralKeyboards.change_page_keyboard())
        Logger.set_state_log(update=update, state=str(PetInformationStates.change_page))
        bot.set_state(user_id=update.from_user.id, state=PetInformationStates.change_page)
    else:
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['all_results_displayed'])
        # сброс состояния, чистка хранилища
        Logger.reset_state_and_data(update=update)
        reset_state_and_data(update=update)


def get_req_results_org(update: [Message, CallbackQuery], method_endswith: str, params: dict) -> None:
    """
    Функция отправляет пользователю результаты запроса.
    """
    req = PetFinderReq.get_request(method_endswith=method_endswith, params=params)
    total_pages = req['pagination']['total_pages']
    current_page = req['pagination']['current_page']
    bot.send_message(chat_id=update.from_user.id,
                     text=LEXICON_RU['page'](current_page=current_page, total_pages=total_pages))
    Logger.output_results(update=update, status='start')
    # цикл по организациям
    for i_org in req['organizations']:
        name: str = i_org['name']
        address: dict = i_org['address']
        url = i_org['url']
        mission_statement: str = i_org['mission_statement']
        distance: float = round(i_org['distance'] * 1.61, 2)
        photos: list = i_org['photos']
        text = LEXICON_RU['org_text'](name=name, mission_statement=mission_statement,
                                      address=address, distance=distance)

        if len(photos) == 0:
            # При отсутствии фотографий - отправляется обычное сообщение
            bot.send_message(chat_id=update.from_user.id, text=text)
        else:
            # формирование списка с объектами-фото организации
            media = list()
            for i_index, i_photo in enumerate(photos):
                if i_index == 0:
                    media.append(InputMediaPhoto(media=i_photo['full'], caption=text))
                else:
                    media.append(InputMediaPhoto(media=i_photo['full']))
            # отправка пользователю фото организации и текста с описанием
            bot.send_media_group(chat_id=update.from_user.id, media=media)

        # отправка пользователю ссылки на страницу с питомцем на сайте
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['learn_more_org'],
                         reply_markup=create_link_keyboard(link=url))
        time.sleep(1.5)
    Logger.output_results(update=update, status='finish')

    #  Проверка, выведены ли все доступные результаты
    if current_page < total_pages:
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['show_more'],
                         reply_markup=GeneralKeyboards.change_page_keyboard())
        Logger.set_state_log(update=update, state=str(OrgInformationStates.change_page))
        bot.set_state(user_id=update.from_user.id, state=OrgInformationStates.change_page)
    else:
        bot.send_message(chat_id=update.from_user.id, text=LEXICON_RU['all_results_displayed'])
        # сброс состояния, чистка хранилища
        Logger.reset_state_and_data(update=update)
        reset_state_and_data(update=update)


def get_info_by_command_id(command_id: int) -> dict:
    """
    Функция получения параметров для request-запроса из БД по id команды
    """
    info_dict = dict()
    # Получение модели команды по id
    command = Command.get(Command.command_id == command_id)
    # Формирование словаря с параметрами запроса
    params = json.loads(command.params.replace("'", '"'))
    # Формирование названия команды
    command_name = command.command_name
    info_dict['command_name'], info_dict['params'] = command_name, params
    return info_dict
