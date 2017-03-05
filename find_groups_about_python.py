import vk
import json
import example_of_using_vk_module


def get_groups_about_python(vk_api, file_for_ids_writing):
    groups_about_python = vk_api.groups.search(q='python', count=200, sort=3, market=0, v=5.62)['items']
    required_groups_ids = []
    unwished_tags = {'кожа', 'кожи', 'skin', 'курсовая', 'лабораторная', 'ищем'}
    for group in groups_about_python:
        for tag in unwished_tags:
            if not group['is_closed'] and group['name'].lower().find(tag.lower()) == -1:
                break
            else:
                required_groups_ids.append(group['id'])
    with open(file_for_ids_writing, 'w') as write_file:
        json.dump({'ids': required_groups_ids}, write_file)


if __name__ == "__main__":
    app_auth_data, user_auth_data = example_of_using_vk_module.get_auth_data_for_token()

    session = vk.AuthSession(app_id=app_auth_data['app_id'], user_login=user_auth_data['login'],
                             user_password=user_auth_data['password'])
    api = vk.API(session)
    get_groups_about_python(api, 'groups_ids_file.json')
