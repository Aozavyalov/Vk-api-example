import vk
import json
import example_of_using_vk_module
import time


def check_group_activity(id, vk_api):
    fl = True
    group_posts = vk_api.wall.get(owner_id=-id, owners_only=1, count=100, v=5.62)['items']
    if len(group_posts) == 0:
        fl = False
    day = int(time.strftime('%j')) - 1
    year = int(time.strftime('%Y'))
    for day in range(day, day - len(group_posts), -1):
        if len(group_posts) == 0:
            break
        if day < 0:
            str_date = '0%d%d' % (365 + day, year - 1)
        else:
            str_date = '0%d%d' % (day, year)
        for post in sorted(group_posts, key=lambda post: post['date'], reverse=True):
            post_date = time.strftime('%j%Y', time.gmtime(post['date']))
            if post_date == str_date:
                group_posts.remove(post)
            else:
                break
    if len(group_posts) > 0:
        fl = False
    return fl


def check_groups(list_of_groups, vk_api):
    for group in list_of_groups:
        if group['is_closed'] != 0 or 'deactivated' in group:
            fl = False
        else:
            time_of_request = time.time()
            fl = check_group_activity(group['id'], vk_api)
            if time.time() - time_of_request < 1:
                time.sleep(1 - (time.time() - time_of_request))
        if not fl:
            list_of_groups.remove(group)
    return list_of_groups


def get_groups_from_links(list_of_groups, vk_api):
    links, ids = [], []
    for group in list_of_groups:
        info_about_group = vk_api.groups.getById(group_id=group['id'], fields=['links'], v=5.62)[0]
        if 'links' in info_about_group:
            links.extend(info_about_group['links'])
        time.sleep(1)
    for link in links:
        if link['url'].find('vk.com/') != -1:
            ids.append(link['url'].split('vk.com/')[-1])
    list_of_groups.extend(vk_api.groups.getById(group_ids=ids, v=5.62))
    return list_of_groups


def write_data_to_json(file_for_writing, data):
    with open(file_for_writing, 'w') as write_file:
        json.dump({'ids': data}, write_file)


def get_groups_about_python(vk_api):
    groups_about_programming = vk_api.groups.search(q='программист', limit=1000, market=0, search_global=1,
                                                    filters=['page'], v=5.62)['items']
    groups_about_programming.extend(vk_api.groups.search(q='программирование', limit=1000, market=0, search_global=1,
                                                         filters=['page'], v=5.62)['items'])
    get_groups_from_links(groups_about_programming, vk_api)
    check_groups(groups_about_programming, vk_api)
    return groups_about_programming


if __name__ == "__main__":
    app_auth_data, user_auth_data = example_of_using_vk_module.get_auth_data_for_token()

    session = vk.AuthSession(app_id=app_auth_data['app_id'], user_login=user_auth_data['login'],
                             user_password=user_auth_data['password'], scope=262150)
    api = vk.API(session)
    groups_ids = example_of_using_vk_module.read_json('groups_ids_file.json')['ids']
    if len(groups_ids) == 0:
        groups = get_groups_about_python(api)
        print('%d groups founded' % len(groups))
        for group in groups:
            groups_ids.append(group['id'])
            print('http://vk.com/club%s' % group['id'])
        write_data_to_json('groups_ids_file.json', groups_ids)
    else:
        print('%d groups founded' % len(groups_ids))
        for id in groups_ids:
            print('http://vk.com/club%s' % id)
