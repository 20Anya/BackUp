import requests
from tqdm import tqdm
import os

def main():
    class VK:
        def __init__(self, access_token, user_id, owner_id, version='5.131'):
            self.version = version
            self.owner_id = owner_id
            self.user_id = user_id
            self.base_url = 'https://api.vk.com/method/'
            self.access_token = access_token
            self.params = {
                'access_token': self.access_token,
                'v': self.version,
                'user_id': self.user_id,
                'owner_id': self.owner_id
            }

        def photos_get(self, album_id='profile', count=1):
            url = f'{self.base_url}photos.get'
            params = {**self.params,
                      'album_id': album_id,
                      'extended': 1,
                      'photo_sizes': 1,
                      'count': count
                      }
            response = requests.get(url, params=params)
            images_dict = response.json()
            return images_dict

    def max_photos(photos):
        max_photo = {}
        for i, photo in enumerate(photos['response']['items']):
            for sizes in photo['sizes']:
                if sizes['type'] == 'z':
                    max_photo[i+1] = {photo['id']: {'user_likes': photo['likes']['user_likes'],
                                          'type': sizes['type'],
                                          'url': sizes['url'],
                                          'date': photo['date']
                                          }}
                elif sizes['type'] == 'y':
                    max_photo[i+1] = {photo['id']: {'user_likes': photo['likes']['user_likes'],
                                      'type': sizes['type'],
                                      'url': sizes['url'],
                                      'date': photo['date']
                                      }}
        return max_photo
        
    vk = VK(ваш токен вк, ваш id, id странички с которой нужны фотки)
    
    images_inf = max_photos(vk.photos_get())  #  изменила url на inf
    photo_inf = {}
    for a, b in images_inf.items():
        for id_, inf in b.items():
            likes = inf['user_likes']
            date = inf['date']
            url = inf['url']
            filename = f'{likes}_{date}.jpg'
            photo_inf[filename] = url
    
    if not os.path.exists("image"):
        os.mkdir("image")
        
    for photo_name, photo_url in photo_inf.items():
        with open(f'image/{photo_name}', 'wb') as file:
            res = requests.get(photo_url)
            file.write(res.content)

    class YandexDisk:
        def __init__(self, token):
            self.headers = {
                'Authorization': f'OAuth {token}'
            }

            response = requests.put(url='https://cloud-api.yandex.net/v1/disk/resources',
                                    headers=self.headers,
                                    params={'path': 'Картинки с ВК'})

        def upload_folder(self):
            upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            params = {
                'path': f'Картинки с ВК/{filename}',
            }
            response = requests.get(upload_url,
                                    params=params,
                                    headers=self.headers)
            upload_link = response.json()['href']

            with open(f'image/{filename}', 'rb') as file:
                response = requests.put(upload_link, files={'file': file})

            for i in tqdm(range(100)):
                pass

    
    yandex = YandexDisk(ваш токен яндекс)
    yandex.upload_folder()

if __name__ == '__main__':
    main()
