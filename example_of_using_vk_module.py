import vk
import json
import time


def read_json(filename):
    try:
        with open(filename, 'r') as read_file:
            json_data = json.load(read_file)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}
    return json_data


def json_data_check(json_data, keys):
    if json_data == {}:
        for key in keys:
            print('Input %s:' % key)
            json_data[key] = input()
    return json_data


def get_auth_data_for_token():
    app_auth_data = read_json('app_auth_data.json')
    app_auth_data = json_data_check(app_auth_data, ['app_id', 'secure_key'])
    user_auth_data = read_json('my_login_and_password.json')
    user_auth_data = json_data_check(user_auth_data, ['login', 'password'])
    return app_auth_data, user_auth_data


if __name__ == '__main__':
    app_auth_data, user_auth_data = get_auth_data_for_token()

    session = vk.AuthSession(app_id=app_auth_data['app_id'], user_login=user_auth_data['login'],
                             user_password=user_auth_data['password'])
    api = vk.API(session)
    my_vk_page_info = api.users.get(user_ids=56329050, fields=['contacts', 'sex', 'universities'])
    print(*my_vk_page_info)
