#! /usr/bin/python3
import sys
import re
from library import gogoanime, check_json
from library.command import *

res_patrn = re.compile(r"(\d{3,4}|\d{3,4}x\d{3,4})")
res_cus_ep = re.compile(r"\d*:\d*|[^-,]\d+")
res_exclude = re.compile(r"\d+,|(\d+-\d+,)+|$(,\d+)")
Quality = "720"
index_list = len(sys.argv)
start = None
end = None
exclude = []
if index_list > 5:
    print("Too much parameters...")
    exit()
if __name__ == "__main__":
    try:
        if sys.argv[1].lower() == "search":
            gogoanime(check_json(), "", "720").search_anime()
        elif sys.argv[1].lower() == 'login':
            check_json()
            print('Process completed!')
            exit()
        else:
            for x in range(index_list):
                if res_patrn.match(sys.argv[x]):
                    Quality = sys.argv[x]
                elif res_cus_ep.match(sys.argv[x]):
                    start, end = custom_command(sys.argv[x])
                elif res_exclude.match(sys.argv[x]):
                    exclude = exclude_command(sys.argv[x])
            gogoanime(check_json(), sys.argv[1],
                      Quality, start, end, exclude).parse()
    except KeyboardInterrupt:
        print("\n \n \nOperation Cancelled")
    except IndexError:
        print(f'Invalid command\nCheck out README for more clear instruction...')
