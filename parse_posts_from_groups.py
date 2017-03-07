import example_of_using_vk_module
import vk
import time
import json


def check_date_of_posts(posts):
    checked_posts = []
    for post in posts:
        if time.strftime('%j%Y', time.gmtime(post['date'])) == time.strftime('%j%Y'):
            checked_posts.append(post)
    return checked_posts


def is_posts_in_file(filename, posts):
    posts_from_file = example_of_using_vk_module.read_json(filename)
    for post in posts_from_file:
        if post in posts:
            posts.remove(post)
    return posts


def parse_posts(vk_api, ids, file_for_writing_posts):
    new_posts = {}
    with open(file_for_writing_posts, 'a') as write_file:
        for id in ids:
            print(id)
            new_posts[id] = []
            temp_posts = vk_api.wall.get(owner_id=-id, owners_only=1, count=100, v=5.62)['items']
            temp_posts = check_date_of_posts(temp_posts)
            offset = len(temp_posts)
            new_posts[id].extend(temp_posts)
            while offset == 100 and time.strftime('%j%Y', time.gmtime(temp_posts[-1]['date'])) == time.strftime('%j%Y'):
                temp_posts = vk_api.wall.get(owner_id=-id, owners_only=1, count=100, offset=offset, v=5.62)['items']
                temp_posts = check_date_of_posts(temp_posts)
                new_posts[id].extend(temp_posts)
                offset += len(temp_posts)
            new_posts = is_posts_in_file(file_for_writing_posts, new_posts)
            time.sleep(1)
        json.dump(new_posts, write_file)
    return new_posts


if __name__ == '__main__':
    ids = example_of_using_vk_module.read_json('groups_ids_file.json')['ids']
    app_auth_data, user_auth_data = example_of_using_vk_module.get_auth_data_for_token()

    session = vk.AuthSession(app_id=app_auth_data['app_id'], user_login=user_auth_data['login'],
                             user_password=user_auth_data['password'])
    api = vk.API(session)
    parse_posts(api, ids, 'posts.json')
