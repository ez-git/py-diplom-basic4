import file_manager
from progress.bar import IncrementalBar
import requests
import time
from urllib.parse import quote


class YaUploader:

    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.ya_host = 'https://cloud-api.yandex.net:443'
        self.headers = {'Authorization': f'OAuth {self.ya_token}'}

    def make_directory(self):
        print('Checking Ya.Disk directory...')
        uri = '/v1/disk/resources'
        path = 'vk_backup'
        response = requests.put(
            self.ya_host + uri + '?path=' + path, headers=self.headers)
        if response.status_code not in [200, 201, 409]:
            path = None
            print(response.json()['message'])
        return path

    def is_exists(self, file_name, path):
        uri = '/v1/disk/resources'
        response = requests.get(self.ya_host
                                + uri
                                + f"?&path={path}/{file_name}",
                                headers=self.headers)
        return response.status_code == 200

    def send_photo(self, photo_data, path):
        uri = '/v1/disk/resources/upload'
        extension = file_manager.parse_extension(photo_data['link'])
        file_name = f"{str(photo_data['likes'])}.{extension}"
        if self.is_exists(file_name, path):
            file_name = f"{str(photo_data['likes'])}" \
                        f"_{str(time.time()).split('.')[0]}.{extension}"

        response = requests.post(self.ya_host
                                 + uri
                                 + f"?url={quote(photo_data['link'], safe='')}"
                                   f"&path={path}/{file_name}",
                                 headers=self.headers)

        if response.status_code == 202:
            async_link = response.json()['href']
            while True:
                response = requests.get(async_link, headers=self.headers)
                if response.status_code == 200:
                    status = response.json()['status']
                    if status == 'success':
                        break
                    elif status == 'failed':
                        file_name = ''
                        break
                else:
                    file_name = ''
                    print(response.json()['message'])
                    break
                time.sleep(1)
        else:
            file_name = ''
            print(response.json()['message'])
        return file_name

    def upload(self, photos_to_upload):
        path = self.make_directory()
        if path is not None:
            uploaded_photos = []
            bar = IncrementalBar('Uploading...', max=len(photos_to_upload))
            for photo_data in photos_to_upload:
                bar.next()
                file_name = self.send_photo(photo_data, path)
                if file_name != '':
                    uploaded_photos += [{'file_name': file_name,
                                         'size': photo_data['size']}]
            bar.finish()
            print('Updating files list...')
            file_manager.add_files_data_to_list(uploaded_photos)
