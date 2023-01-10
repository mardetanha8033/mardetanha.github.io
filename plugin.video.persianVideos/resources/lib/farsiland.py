import requests
import json
import re
import sys
import xbmcplugin
from bs4 import BeautifulSoup
import xbmc
import xbmcgui
import resources.lib.config as config
from urllib.parse import quote_plus, parse_qsl
from urllib.parse import urlencode, quote_plus
import urllib.parse
from resources.lib.play import play_video
from resources.lib.utils import get_request, get_soup, get_json, get_list, get_results, add_dir, add_dird, next_pag
handle = int(sys.argv[1])


def get_categories(name, url, icon, fanart, description, foldername,  page):
    xbmcplugin.setPluginCategory(handle, foldername)
    xbmcplugin.setContent(handle, 'tvshows')
    soup = get_soup(url)
    item_list = soup.find_all('article', {'class': 'item tvshows'})
    for item in item_list:
        name = item.text
        icon = item.img['src']
        link = item.a['href']
        add_dir(name, link, 'episode_cat', icon, '', '', '', isFolder=True)
    for name, url in next_pag(url):
        try:
            add_dir(name, url, 'shows_list', '', '', '')
        except:
            break


def get_episode_list(name, url, icon, description):
    soup = get_soup(url)
    item_list = soup.find_all('ul', {'class': 'episodios'})
    for x in item_list:
        list_item = x.find_all('div', {'class': 'episodiotitle'})
        for item in list_item:
            name = item.a.text
            link = item.a['href']
            add_dird(name, link, 'episodes', icon, '', '', '', isFolder=False)


def get_video_list(name, url, icon, description):
    soup = get_soup(url)
    item_list = soup.find_all('article', {'class': 'item movies'})
    for item in item_list:
        name = item.text
        icon = item.img['src']
        link = item.a['href']
        add_dird(name, link, 'episodes', icon, '', '', '', isFolder=False)
    """ for name, url in pagination(url):
        add_dir(name, url, 'season_cat', '', '', '') """
    for name, url in next_pag(url):
        try:
            add_dir(name, url, 'season_cat', '', '', '')
        except:
            break


def get_video(name, url, icon, description):
    #item_list = []
    soup = get_soup(url)
    item_list = soup.find('div', {'id': 'fakeplayer'}).input.attrs
    description = soup.find('div', {'class': 'wp-content'}).text.strip()
    data = {
        'id': item_list['value'],
    }
    respon = requests.post('https://farsiland.com/intro7/',
                           headers=config.headers, data=data).text
    soupd = BeautifulSoup(respon, 'html.parser')
    item_lists = soupd.find_all('li', {'class': 'dooplay_player_option'})
    for item in item_lists:
        data_2 = {
            'action': 'doo_player_ajax',
            'post': item['data-post'],
            'nume': item['data-nume'],
            'type': item['data-type']
        }
        response = requests.post(
            'https://farsiland.com/wp-admin/admin-ajax.php', headers=config.headers, data=data_2).text
        #soupc = get_soup(response)
        json_data = json.loads(response)
        links = json_data['embed_url']
        req = requests.get(links, headers=config.headers)
        soupc = BeautifulSoup(req.content, 'html.parser')
        script = soupc.find_all('script', type='text/javascript')
        gh = re.search('(?<=jw = )(.*)', str(script)).group(1)
        json_d = json.loads(gh)
        link = json_d['file']
        #link = urllib.parse.unquote(urllib.parse.unquote(libn))
        link2 = json_d['file2']
        #link = urllib.parse.quote(link, safe=':/')
        #link2 = urllib.parse.quote(link2, safe=':/')

    #link = get_multilink(item_list)
    play_video(name, link, icon, description)


def shows_main():
    xbmcplugin.setPluginCategory(handle, 'Farsiland')
    add_dir('New Movies', config.new_movies, 'season_cat', '', '',
            'New Movies', foldername='New Movies', isFolder=True)
    add_dir('Old Movies', config.old_movies, 'season_cat', '', '',
            'Old Movies', foldername='Old Movies', isFolder=True)
    add_dir('New Series', config.new_series, 'shows_list', '', '',
            'New Series', foldername='New Series', isFolder=True)
    add_dir('Old Series', config.old_series, 'shows_list', '', '',
            'Old Series', foldername='Old Series', isFolder=True)
