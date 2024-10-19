import requests
from tqdm import tqdm

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
        for photo in photos['response']['items']:
            for sizes in photo['sizes']:
                if sizes['type'] == 'z':
                    max_photo[photo['id']] = {'user_likes': photo['likes']['user_likes'],
                                              'type': sizes['type'],
                                              'url': sizes['url'],
                                              'date': photo['date']
                                              }
                elif sizes['type'] == 'y':
                    max_photo[photo['id']] = {'user_likes': photo['likes']['user_likes'],
                                              'type': sizes['type'],
                                              'url': sizes['url'],
                                              'date': photo['date']
                                              }
        return max_photo
        
    vk = VK(ваш токен вк, ваш id, id странички с которой нужны фотки)
    images_url = max_photos(vk.photos_get())
    for a, b in images_url.items():
        likes = b['user_likes']
        date = b['date']
        filename = f'{likes}_{date}'

    res = requests.get(images_url)
    with open(f'image/{filename}', 'wb') as f:
        f.write(res.content)

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
