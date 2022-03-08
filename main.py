import requests
import datetime
import json
from progress.bar import Bar


class VkDownloader:
    def __init__(self, owner_id):
        with open('token.txt', 'r') as file_object:
            self.token = file_object.read().strip()
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id' : owner_id,
            'album_id' : 'profile',
            'extended' : '1',
            'access_token': self.token,
            'v':'5.131'
        }
        res = requests.get(URL, params=params).json()['response']['items']
        self.likes = []
        dates = []
        sizes = []
        self.sizes2 = []
        self.foto = []
        for r in res:
            self.likes.append(str(r['likes']['count']))
            sizes.append(r['sizes'])
            dates.append(datetime.date.fromtimestamp(r['date']))
        index_dict = []
        last_encounters = {}
        for i, item in enumerate(self.likes):
            if item not in last_encounters:
                last_encounters[item] = None
            else:
                last_encounters[item] = i
                index_dict.append(i)
        for ind in index_dict:
            self.likes[ind] = f'{self.likes[ind]}_{dates[ind]}'
        for s in sizes:
            self.foto.append(s[-1]['url'])
            self.sizes2.append(s[-1]['type'])

    def token_ya_method(self, token_ya):
        with open(token_ya, 'r') as file_object:
            self.token_y = file_object.read().strip()
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth ' + self.token_y}
        with Bar('Processing', max=len(self.foto)) as bar:
            for u, f in zip(self.foto, self.likes):
                params = {'url': u, "path": f'new_foto/{f}.jpg', "disable_redirects": "true"}
                response = requests.post(url, params=params, headers=headers)
                bar.next()
            bar.finish()
        with open("data_file.json", "w") as write_file:
            for d, z in zip(self.likes, self.sizes2):
                data = [{"file_name": d, "size": z}]
                json.dump(data, write_file)
        return print(f'\nФайлы скачены')


if __name__ == '__main__':
    downloader = VkDownloader('552934290')
    uploader = downloader.token_ya_method('token_ya.txt')



