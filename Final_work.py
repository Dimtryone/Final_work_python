import requests
from urllib.parse import urlencode
import webbrowser
from urllib.parse import urlparse
import json
import os
import shutil



class VKCustomer:
    path = os.getenv('HOMEPATH') + '\\Netology_Tok\\Tokens.txt'
    print(path)
    with open(path, 'r', encoding='utf-8') as file:
        parametrs = list(map(str.strip, file.readlines()))
    APP_ID = int(parametrs[5])
    URL_BASE = 'https://api.vk.com/method/'
    URL_REDIRECT = 'https://oauth.vk.com/blank.html'
    URL_AUTH = 'https://oauth.vk.com/authorize/'
    METHOD_GET_PHOTOS = 'photos.get'
    FRIENDS = 'friends'
    PHOTOS = 'photos'
    AUDIO = 'audio'
    WALL = 'wall'
    SCOPE_LIST: list[str] = [FRIENDS, PHOTOS, AUDIO, WALL]
    SCOPE: str = ','.join(SCOPE_LIST)
    PROTOCOL_VERSION = '5.131'

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = ''
        self.link_photo = {}

    def get_token(self):
        param = {
            "client_id": self.APP_ID,
            "redirect_uri": self.URL_REDIRECT,
            "display": 'page',
            "scope": self.SCOPE,
            "response_type": "token"
        }
        print('')
        webbrowser.open('?'.join((self.URL_AUTH, urlencode(param))), new=1)
        url_back = input('вставьте скопированную строку из открывшейся страницы:')
        strange = urlparse(url_back)
        str_with_token = strange[5]
        list_with_token = str_with_token.split('&')
        token = list_with_token[0]
        token = token.replace('access_token=', '')
        self.token = token
        print('токен сохранен')


    def __get_url__(self, name_method) -> str:
        return f'{self.URL_BASE}{name_method}'

    def get_photos(self):
        url = self.__get_url__(self.METHOD_GET_PHOTOS)
        album_ID = ['wall', 'profile', 'saved']
        param = {
            'access_token': self.token,
            'owner_id': self.user_id,
            'album_id': album_ID[1],
            'extended': '1',
            'photo_sizes': '1',
            'v': self.PROTOCOL_VERSION
        }
        response = requests.get(url, param)
        if response.status_code == 200:
            photos = response.json()
            for_save_image = {}
            for item in photos['response']['items']:
                max_size = 0
                url_images = []
                for i in item['sizes']:
                    size = i['width']
                    if max_size < size:
                        max_size = size
                        url_image = i['url']
                        url_images.clear()
                        url_images.append(url_image)
                for_save_image[max_size] = url_images[0]
            self.link_photo = for_save_image
            print('Ссылка на фото самого большого размера сохранена')
        else:
            print('Обратитесь в поддержку, фото не удалось получить')

    def save_photo(self):
        link = self.link_photo
        for key, value in link.items():
            file_name = str(key)
            url = value
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(file_name, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                print('Image sucessfully Downloaded: ', file_name)
            else:
                print('Image Couldn\'t be retreived')


class YaUploader:
    path = os.getenv('HOMEPATH') + '\\Netology_Tok\\Tokens.txt'
    print(path)
    with open(path, 'r', encoding='utf-8') as file:
        parametrs = list(map(str.strip, file.readlines()))
    YaDisk_Token = parametrs[3]
    URL_UPLOAD = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'

    def __init__(self, name_file: str):
        self.token = YaDisk_Token
        self.path = ''
        self.name_file = name_file

    def _get_path_to_file(self):
        import os
        BASE_DIR = os.getcwd()
        self.path = os.path.join(BASE_DIR, self.name_file)
        return self.path

    def _get_url_upload(self):
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': self.name_file, 'overwrite': True}
        response = requests.get(self.URL_UPLOAD, headers=headers, params=params)
        if response.status_code == 200:
            url_upload = response.json().get('href')
            return url_upload
        else:
            message = 'Error connect with server'
            return message

    def upload(self):
        url_upload = self._get_url_upload()
        if url_upload == 'Error connect with server':
            message = 'не удалось получить ссылку для загрузки файла'
            print(message)
            return message
        file_path = self._get_path_to_file()
        with open(file_path, 'rb') as file:
            response = requests.put(url_upload, data = file )
            if response.status_code == 201:
                print('файл успешно загружен')
            else:
                print('файл не загружен')


example_user_ID = 2481318

vk_client = VKCustomer(example_user_ID)
vk_client.get_token()
vk_client.get_photos()
vk_client.save_photo()

YaDisk = YaUploader('847')


print('the end')


#OWNER_ID = '2481318'
#URL_PHOTOS = 'api.vk.com/method/photos.get'
#METHOD_GET_PHOTOS = 'photos.get'
#PROTOCOL_VERSION: str = "5.131"
#params = {'access_token':TOKEN_MY, 'owner_id': OWNER_ID, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1, 'V': PROTOCOL_VERSION}
#response = requests.get(url=URL_PHOTOS, params=params)
#print(response.json())
