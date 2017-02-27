import requests
import json

def request_to_vk():

    pass


def auth_vk():

    pass


def get_vk_token():

    pass


def read_json(filename):
    try:
        with open(filename, 'r') as rf:
            json_data = rf.read()
    except FileNotFoundError:
        json_data = '{}'
        print('There is no such file(')
    return json.loads(json_data)


if __name__ == '__main__':
    file_name = 'vk-api-schema/responses.json'
    responses = read_json(file_name)

    print(*responses['definitions'], sep='\n')
