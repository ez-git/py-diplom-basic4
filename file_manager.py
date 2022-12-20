import json
import os


def parse_extension(link):
    index = link.find('?')
    if index == -1:
        extension = link.split('.')[-1]
    else:
        extension = link[:index].split('.')[-1]
    return extension


def add_files_data_to_list(uploaded_photos):
    LIST_FULL_PATH = 'files_list.json'
    if os.path.exists(LIST_FULL_PATH):
        with open(LIST_FULL_PATH, 'r') as files_list:
            files = json.load(files_list)
            [files.append(x) for x in uploaded_photos if x not in files]
        with open('files_list.json', 'w') as files_list:
            json.dump(files, files_list)
    else:
        with open(LIST_FULL_PATH, 'w') as files_list:
            json.dump(uploaded_photos, files_list)
