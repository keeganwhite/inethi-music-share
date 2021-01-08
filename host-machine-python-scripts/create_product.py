import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
import json
import requests


def main():
    """
    Uses the inethi-music-share-api to upload songs to the WooCommerce store
    """
    load_dotenv()
    global_folder_path = os.getenv('GLOBAL_FOLDER_PATH')
    local_folder_path = os.getenv('LOCAL_FOLDER_PATH')
    temp_file_path_all = os.getenv('TEMP_FILE_LOCATION_ALL')
    api_endpoint = os.getenv('API_ENDPOINT')
    list_of_song_files = [f for f in listdir(temp_file_path_all) if isfile(join(temp_file_path_all, f))]
    list_of_song_files.sort(key=os.path.getctime)  # oldest to newest
    headers = {'Content-type': 'application/json'}
    body = {
        "global_file_path": global_folder_path,
        "local_file_path": local_folder_path,
        "file_names": list_of_song_files
    }
    post_request = requests.post(api_endpoint, headers=headers, data=json.dumps(body))


if __name__ == '__main__':
    main()
