from typing import Optional
import requests
from config_data.config import API_KEY, API_SECRET
from utils.exceptions import ServerError

MAX_RES_COUNT = 10


class PetFinderReq:
    # URL-адрес API
    __url = 'https://api.petfinder.com'
    # Данные для получения токена API
    __auth_data = {'grant_type': 'client_credentials',
                   'client_id': API_KEY,
                   'client_secret': API_SECRET}
    # Используемые эндпойнты
    __endpoints = {
        'get_animals': '/v2/animals',  # для вывода данных о животных
        'get_organizations': '/v2/organizations',  # для вывода данных об организациях
    }

    @classmethod
    def get_api_auth(cls) -> dict:
        url = ''.join([cls.__url, '/v2/oauth2/token'])
        response = requests.post(url=url, data=cls.__auth_data, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise ServerError(f'Ответ от сервера не получен.'
                              f'Status error: {response.status_code}. Detail: {response.json()["detail"]}')

    @classmethod
    def get_request(cls, method_endswith: str, params: Optional[dict] = None) -> dict:
        # Получение токена API (каждый раз при GET-запросе, так как ограничен период действия токена)
        headers_data = cls.get_api_auth()
        # Формирование шапки запроса
        headers = {'Authorization': ' '.join([headers_data['token_type'],
                                              headers_data['access_token']])}
        # Формирование url
        url = ''.join([cls.__url, cls.__endpoints[method_endswith]])

        response = requests.get(url=url, params=params, headers=headers, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise ServerError(f'Ответ от сервера не получен.'
                              f'Status error: {response.status_code}. Detail: {response.json()["detail"]}')



