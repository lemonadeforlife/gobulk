#! /usr/bin/python3
import re
import json
import sys
from pathlib import Path
from library import *

# Enter your token.json location here
with open(f'token.json', 'r') as f:
    data = json.load(f)
    email = data['email']
    password = data['password']
    headers_value = data['user-agent']

res_patrn = re.compile(r'(\d{3,4}|\d{3,4}x\d{3,4})')
res_cus_ep = re.compile(r'\d*:\d*|\d')
res_exclude = re.compile(r'\d+,|(\d+-\d+,)+|$(,\d+)')
Quality = '720'
index_list = len(sys.argv)
if index_list > 5:
    print('Too much parameters...')
    exit()
if __name__ == '__main__':
    try:
        if sys.argv[1].lower() == 'search':
            gogoanime('', '720').search_anime()
        else:
            for x in range(index_list):
                if res_patrn.match(sys.argv[x]):
                    Quality = sys.argv[x]
                elif res_cus_ep.match(sys.argv[x]):
                    start, end = custom_command(sys.argv)
                elif res_exclude.match(sys.argv[x]):
                    exclude = exclude_command(sys.argv[x])
            gogoanime(sys.argv[1], Quality, start, end, exclude).parse()
    except KeyboardInterrupt:
        print('\n \n \nOperation Cancelled')
