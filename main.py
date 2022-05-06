
import time
from tqdm import tqdm
import requests
import datetime
import json


with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

URL = 'http://api.vk.com/method/photos.get'
params = {
    'access_token': token,
    'v': '5.131',
    'owner_id': input('Enter ids: '),
    'album_id': 'profile',
    'extended': '1',
    'photo_sizes': '0',
    'count': '5'
}
res = requests.get(URL, params=params).json()

def upload_files(token_ya = ' '):
    list1 = res['response']['items']
    list_of_likes = []
    my_list_json = []
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(token_ya)
    }
    new_folder = input('Folder name: ')
    create_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params_create_folder = {'path': f'disk:/{new_folder}/'}
    response_folder = requests.put(create_url, headers=headers, params=params_create_folder)

    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    with open('info.json', 'w') as new_file:
        for file in list1:
            new_dict = {}
            if file['likes']['count'] in list_of_likes:
                params_y = {
                    "url": '{}'.format(file['sizes'][-1]['url']),
                    "path": f"disk:/{new_folder}/{file['likes']['count']},{datetime.datetime.fromtimestamp(file['date']).strftime('%Y-%m-%d')}.jpg"
                }
                response = requests.post(upload_url, headers=headers, params=params_y)
                new_dict['file_name'] = f"{file['likes']['count']},{datetime.datetime.fromtimestamp(file['date']).strftime('%Y-%m-%d')}.jpg"
                new_dict['size'] = file['sizes'][-1]['type']
            else:
                params_y = {
                    "url": '{}'.format(file['sizes'][-1]['url']),
                    "path": f"disk:/{new_folder}/{file['likes']['count']}.jpg"
                }
                response = requests.post(upload_url, headers=headers, params=params_y)
                new_dict['file_name'] = f"{file['likes']['count']}.jpg"
                new_dict['size'] = file['sizes'][-1]['type']
            list_of_likes.append(file['likes']['count'])
            my_list_json.append(new_dict)
        json.dump(my_list_json, new_file, indent=1)
        for i in tqdm(list1):
            time.sleep(1)


upload_files(' ')