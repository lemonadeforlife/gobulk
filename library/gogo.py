import os
import sys
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from library.login import login
from library.command import custom_command, exclude_command
from library.dm import download_manager
home = str(Path.home())


class gogoanime():
    def __init__(self, cred_path: str, link: str, quality: str, start_ep: int = None, end_ep: int = None, exclude_episode: set = None):
        self.link = link
        self.quality = quality
        self.start_ep = start_ep
        self.end_ep = end_ep
        self.exclude_episode = exclude_episode
        self.cred_path = cred_path

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
        if items == []:
            print(f"{'*'*5} Couldn't find anything as:[{anime_name}] {'*'*5}")
            exit()
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
            return anime_name

    def write_url(self, url, ep, type='w'):
        if type == 'w':
            link = url
        else:
            link = '\n'+url
        try:
            os.mkdir(f'{home}/Documents/gobulk/')
        except FileExistsError:
            pass
        with open(f'{home}/Documents/gobulk/{self.anime_info(name=True)}.txt', f'{type}') as f:
            f.write(link)
        download_manager(
            url, f'{home}/Videos/Anime/{self.anime_info(True)}', ep, 2).aria2c
        print(
            f'{self.anime_info(name=True)} [EP:{ep}]-> Url has been written successfully')

    def parse(self):
        if self.check_url() != True:
            raise Exception("Invalid Url or Url doesn't exitst")
        link_ptrn = self.link.replace(
            'category/', '') + '-episode-{}'
        """
        Created a request session so that we can login and access the gogoanime download
        """
        with requests.Session() as s:
            headers = {'user-agent': login(self.cred_path).headers}
            login_url = 'https://gogoanime.tel/login.html'
            c_token = s.get(login_url, headers=headers)
            soup = BeautifulSoup(c_token.content, 'lxml')
            meta = soup.find('meta', attrs={'name': "csrf-token"})
            key = meta['content']
            payload = {
                '_csrf': key, 'email': login(self.cred_path).email, 'password': login(self.cred_path).password}
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
Directory: {home}/Desktop""")
