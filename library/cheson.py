import sys
from pathlib import Path
from .command import clear
import json
import os
home = str(Path.home())


def check_json():
    check_loc = Path(f'{home}/.config/gobulk/key.json')
    if check_loc.is_file() == True:
        location = f'{home}/.config/gobulk/key.json'
    else:
        folder = f'{home}/.config/gobulk'
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        in_mail = input('Enter your gogoanime email address$ ')
        in_password = input('\nEnter your gogoanime password$ ')
        in_headers = input('\nEnter headers$ ')
        clear()
        with open(f'{folder}/key.json', 'w') as f:
            data = {
                'email': in_mail,
                'password': in_password,
                'user-agent': in_headers
            }
            json.dump(data, f, indent=3)
            location = f'{home}/.config/gobulk/key.json'
    return location
