from telebot.handler_backends import State, StatesGroup


class AdditionalStates(StatesGroup):
    """
    Класс состояния по умолчанию
    """
    default = State()


class PetInformationStates(StatesGroup):
    """
    Класс состояний пользователя при выполнении команды /find_pet
    """
    location = State()
    pet_type = State()
    pet_age = State()
    pet_size = State()
    has_child = State()
    has_pet = State()
    has_allergy = State()
    res_count = State()
    change_page = State()


class OrgInformationStates(StatesGroup):
    """
    Класс состояний пользователя при выполнении команды /find_pet
    """
    location = State()
    sort_param = State()
    res_count = State()
    change_page = State()
