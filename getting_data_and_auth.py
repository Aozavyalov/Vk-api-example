import requests
import json
import re


def json_form_request(url, params=None):
    # не требуется ручками перобразовывать параметры
    return requests.get(url, params=params).json()


def request_to_vk(method, params=None, base_url=r"https://api.vk.com/method/"):
    url = f"{base_url}{method}"  # formated strings - python 3.6
    return json_form_request(url, params)


def get_vk_token(client_id, client_secret):
    params = {
        'client_id': client_id, 
        'client_secret': client_secret, 
        'grant_type': 'client_credentials'
    } 
    return request_to_vk(base_url=r"https://oauth.vk.com/", 
                         method="access_token", params=params)


def read_json(filename):
    json_data = '{}'  # меньше вложенности - круче
    # better to do this without exceptions handling (check path exists)
    try:
        with open(filename, 'r') as file:
            json_data = json.load(file)  # json can read directly from file
    except FileNotFoundError:
        print('There is no such file(')
    return json_data


if __name__ == '__main__':
    app_auth_data = read_json('app_auth_data.json')
    token = get_vk_token(app_auth_data['app_id'], app_auth_data['secure_key'])
    print(token)
    users_manual_params = {
        'user_id': '56329050', 
        'access_token': token['access_token'], 
        'v': '5.52',
        'name_case': 'Nom', 
        'fields': "first_name"
    }
    user = request_to_vk('users.get', params=users_manual_params)
    print(user)
