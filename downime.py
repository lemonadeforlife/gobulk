#! /usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from pathlib import Path
import os
import time

home = str(Path.home())
# Enter your token.json location here
with open(f'{home}/Documents/gobulk/token.json', 'r') as f:
    data = json.load(f)
    email = data['email']
    password = data['password']
    headers_value = data['user-agent']


class gogoanime():
    def __init__(self, link: str, quality: str, start_ep: int = None, end_ep: int = None, exclude_episode: set = None):
        self.link = link
        self.quality = quality
        self.start_ep = start_ep
        self.end_ep = end_ep
        self.exclude_episode = exclude_episode

    def check_url(self):
        gogo_patrn = re.compile(
            r'https://gogoanime\.[a-zA-Z]{2,3}/category/.+')
        gogo_match = gogo_patrn.match(self.link)
        if gogo_match:
            if requests.get(self.link).status_code == 200:
                return True
        else:
            return False

    def search_anime(self):
        sites = ['gogoanime.tel', 'gogoanime.ee', 'gogoanime.lu']
        for site in sites:
            if requests.get(f'https://{site}').status_code == 200:
                site_url = site
                break
        else:
            raise Exception("Invalid url or URL no longer exist...")
        anime_name = input('Enter anime name$ ')
        search = f'https://{site_url}/search.html?keyword={anime_name}'
        r = requests.get(search).text
        soup = BeautifulSoup(r, 'lxml')
        unsort_list = soup.find('ul', class_='items')
        items = unsort_list.find_all('li')
        for index, item in enumerate(items):
            name = item.find('p', class_="name").text.strip()
            release_data = item.find('p', class_='released').text.strip()
            print(f'[{index}] Anime Name: {name} | Year: {release_data}')
        choose_anime = input("Which anime do you want to select? ")
        find_link = items[int(choose_anime)].find('a', href=True)
        s_link = 'https://gogoanime.tel'+find_link['href']
        print(
            "Enter your preferred resolution?[Press 'Enter' to keep default:720p]")
        quality = input('$ ')
        if quality == '':
            self.quality = '720'
        else:
            self.quality = quality
        print(
            "Do you want specify download range?[Press 'Enter' to skip default:All]")
        ep_range = input('$ ')
        if ep_range == '':
            self.start_ep = None
            self.end_ep = None
        else:
            self.start_ep, self.end_ep = custom_command(ep_range)
        print(
            'Do you want to exclude any episode?[Press "Enter" to skip default:None]')
        exclude_ep = input('$ ')
        if exclude_ep == '':
            self.exclude_episode = None
        else:
            self.exclude_episode = exclude_command(exclude_ep)
        self.link = s_link
        self.parse()

    def anime_info(self, name: bool = False):
        url = requests.get(self.link).text
        soup = BeautifulSoup(url, 'lxml')  # Base url page
        anime_info = soup.find('div', class_="anime_info_episodes")
        anime_name = anime_info.find('h2').text.strip()  # Anime name
        anime_body = soup.find('div', class_='anime_video_body')
        episode_page_index = anime_body.find('ul', id="episode_page")
        episode_page = episode_page_index.find('a', class_='active')
        episode = episode_page.text
        start, end = episode.split('-')
        if name == False:
            return int(end)
        else:
            return str(anime_name)

    def write_url(self, url: str, ep, type='w'):
        if type == 'a':
            link = '\n' + url
        else:
            link = url
        with open(f'{home}/Desktop/{self.anime_info(name=True)}.txt', f'{type}') as f:
            f.write(link)
        directory = f"{home}/Videos/Anime/{self.anime_info(True)}"
        command = f'nohup uget-gtk --category-index=2 --quiet --folder="{directory}" --filename="EP{str(ep).zfill(2)}" "{url}" > /dev/null 2>&1 &'
        os.system(command)

    def parse(self):
        if self.check_url() != True:
            raise Exception("Invalid Url or Url doesn't exitst")
        link_ptrn = self.link.replace(
            'category/', '') + '-episode-{}'
        """
        Created a request session so that we can login and access the gogoanime download
        """
        with requests.Session() as s:
            headers = {'user-agent': headers_value}
            login_url = 'https://gogoanime.tel/login.html'
            c_token = s.get(login_url, headers=headers)
            soup = BeautifulSoup(c_token.content, 'lxml')
            meta = soup.find('meta', attrs={'name': "csrf-token"})
            key = meta['content']
            payload = {
                '_csrf': key, 'email': email, 'password': password}
            les_go = s.post(login_url, data=payload, headers=headers)
            count = 0
            if self.start_ep == None:
                start_num = 1
            else:
                start_num = self.start_ep
            if self.end_ep == None:
                end_num = self.anime_info() + 1
            else:
                end_num = self.end_ep + 1
            for x in range(start_num, end_num):
                if self.exclude_episode != None and x in set(self.exclude_episode):
                    continue
                else:
                    site = link_ptrn.format(x)
                    site_html = s.get(site).text
                    html_soup = BeautifulSoup(site_html, 'lxml')
                    lst_download = html_soup.find('div', class_='list_dowload')
                    jucy_load = lst_download.find('div', class_='cf-download')
                    link_baby = jucy_load.find_all('a', href=True)
                    lis_res = ''
                    Found = False
                    while Found == False:
                        for link in link_baby:
                            lis_res += link.text.strip() + '\n'
                            if self.quality in link.text.strip():
                                if count == 0:
                                    self.write_url(link['href'], x)
                                    count += 1
                                else:
                                    self.write_url(link['href'], x, 'a')
                                    count += 1
                                Found = True
                                break
                        if self.quality not in link.text.strip():
                            print("Couldn't found the resolution")
                            print(
                                f'List of Available downloads(Enter the height or resolution):\n{lis_res}')
                            self.quality = input('Resolution$ ')
        print(f"""All Download Links were successfully written
File Saved as: {self.anime_info(name=True)}.txt
Directory: {home}/Documents/gobulk""")


def custom_command(com):
    if com.find(':') != -1:
        start, end, *ignore = com.split(':')
        if start == '':
            start_ep = None
        else:
            start_ep = int(start)
        if end == '':
            end_ep = None
        else:
            end_ep = int(end)
    else:
        try:
            start_ep = int(com)
            end_ep = int(com) + 1
        except Exception:
            print(f'{com} is invalid')
            exit()
    return start_ep, end_ep


def exclude_command(com):
    exclude = []
    if com.find(',') != -1:
        for num in com.split(','):
            if num == '':
                continue
            elif num.find('-') != -1:
                num1, num2 = num.split('-')
                for n in range(int(num1), int(num2)+1):
                    exclude.append(n)
            else:
                try:
                    exclude.append(int(num))
                except Exception:
                    print(
                        f'Error::   Exclude Value: {num}\nWhich was ignored and continued')
    return sorted(set(exclude))


res_patrn = re.compile(r'(\d{3,4}|\d{3,4}x\d{3,4})')
res_cus_ep = re.compile(r'\d*:\d*|\d')
res_exclude = re.compile(r'\d+,|(\d+-\d+,)+|$(,\d+)')
Quality = '720'
index_list = len(sys.argv)
start = None
end = None
exclude = None
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
