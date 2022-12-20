from vk_backup_manager import VKBackupManager


if __name__ == '__main__':
    vk_user = input('Enter user ID or screen name: \n')
    number_of_photos = int(input('Enter the number of photos'
                                 ' you want to save (default = 5): \n') or 5)
    ya_token = input('Enter user Yandex.Poligon token: \n')

    vk_backup_manager = VKBackupManager()
    vk_backup_manager.make_backup(vk_user, number_of_photos, ya_token)
