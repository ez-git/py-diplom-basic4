import requests
from ya_uploader import YaUploader


class VKBackupManager:

    def __init__(self):
        self.vk_service_token = ''
        self.vk_version = '5.131'
        self.vk_host = 'https://api.vk.com/'

    def get_user_id_by_name(self, vk_user):

        VK_METHOD = 'method/users.get'

        params = f'user_ids={vk_user}&access_token={self.vk_service_token}&v={self.vk_version}'
        response = requests.get(self.vk_host + VK_METHOD + '?' + params)
        json_response = response.json()
        return json_response['response'][0]['id']

    def get_vk_photos(self, vk_user, max_count_photo=5):

        VK_METHOD = 'method/photos.get'

        if vk_user.isdigit():
            vk_user_id = vk_user
        else:
            vk_user_id = self.get_user_id_by_name(vk_user)

        params = f'owner_id={vk_user_id}&album_id=profile&extended=1&photo_sizes=1' \
                 f'&offset=0&count=1000&access_token={self.vk_service_token}&v={self.vk_version}'

        response = requests.get(self.vk_host + VK_METHOD + '?' + params)
        json_response = response.json()
        photos_to_upload = []
        if json_response.get('error') is None:
            items = json_response['response']['items']
            print(f'Fonded {len(items)} photos')
            print('Receiving information...')
            for item in items:
                if len(photos_to_upload) < max_count_photo:
                    for size in item['sizes']:
                        if size['type'] == 'z':
                            photo_to_upload = {'likes': item['likes']['count'],
                                               'link': size['url'],
                                               'size': size['type']}
                            photos_to_upload += [photo_to_upload]
        else:
            print(f"{json_response['error']['error_msg']}")

        print('Photos to upload:', len(photos_to_upload))
        return photos_to_upload

    def make_backup(self, vk_user, number_of_photos, ya_token):
        print('Starting backup...')
        print('Receiving photos...')
        photos_to_upload = self.get_vk_photos(vk_user, number_of_photos)

        ya_uploader = YaUploader(ya_token)
        ya_uploader.upload(photos_to_upload)

        print('Backup completed')
