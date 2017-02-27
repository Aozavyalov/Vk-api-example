import requests
import json
import re


def request_to_vk(method, params, request=None):
    if request:
        request = request + '%s?%s' % (method, params)
    else:
        request = 'https://api.vk.com/method/%s?%s' % (method, params)
    response = requests.get(request)
    return response.json()


def get_vk_token(client_id, client_secret):
    method = 'access_token'
    params_str = generate_params_string(
        {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'})
    token = request_to_vk(request='https://oauth.vk.com/', method=method, params=params_str)
    return token


def read_json(filename):
    try:
        with open(filename, 'r') as rf:
            json_data = rf.read()
    except FileNotFoundError:
        json_data = '{}'
        print('There is no such file(')
    return json.loads(json_data)


def generate_params_string(params):
    result = ''
    for parameter in params:
        if type(params[parameter]) == list:
            result += '%s=' % parameter
            for key in params[parameter]:
                result += '%s,' % key
            result = result[:-1] + '&'
        else:
            result += '%s=%s&' % (parameter, params[parameter])
    print(result[:-1])
    return result[:-1]


if __name__ == '__main__':
    app_auth_data = read_json('app_auth_data.json')
    token = get_vk_token(app_auth_data['app_id'], app_auth_data['secure_key'])
    print(token)
    users_get_params = {'user_ids': ['56329050'], 'access_token': token['access_token'], 'v': '5.52',
                        'name_case': 'Nom', 'fields': ['first_name']}
    user = request_to_vk('users.get', generate_params_string(users_get_params))
    print(user)
