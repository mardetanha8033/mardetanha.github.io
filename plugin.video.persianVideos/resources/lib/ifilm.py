import sys
import xbmcplugin
import re
import xbmc
import xbmcgui
import resources.lib.config as config
from resources.lib.play import play_manoto
from resources.lib.utils import ifilm_request, ifilm_soup, add_dir, add_dird

handle = int(sys.argv[1])


def ifilm_shows_list(name, url, icon, fanart, description, foldername,  page):
    xbmcplugin.setPluginCategory(handle, foldername)
    xbmcplugin.setContent(handle, 'tvshows')
    if page == '':
        page = 1

    soup = ifilm_soup(f'{url}&page={page}')
    item_list = soup.find_all('a', {'class': 'inner-panel'})

    #item_list = soup.find_all('a', {'class': 'inner-panel'})[5:]
    for item in item_list:
        #name = item.text.strip()
        name = item.find(['h3', 'h6']).text.strip()
        link = config.ifilm_base + item['href']
        poster = config.ifilm_base + \
            item.find('img', {'class': 'fill-box'})['src']
        add_dir(name, link, 'ifilm_season_cat', poster,
                fanart, '', isFolder=True)

    if len(item_list) > 0:
        page = int(page) + 1
        add_dir('Next Page', url, 'ifilm_shows_list', '', '', 'Next Page',
                foldername=foldername, page=page, isFolder=True)
    else:
        xbmcplugin.endOfDirectory(handle)


def ifilm2_shows_list(name, url, icon, fanart, description, foldername,  page):
    xbmcplugin.setPluginCategory(handle, foldername)
    xbmcplugin.setContent(handle, 'tvshows')
    if page == '':
        page = 1

    soup = ifilm_soup(f'{url}&page={page}')
    item_list = soup.find_all('a', {'class': 'inner-panel'})

    #item_list = soup.find_all('a', {'class': 'inner-panel'})[5:]
    for item in item_list:
        #name = item.text.strip()
        name = item.find(['h3', 'h6']).text.strip()
        link = config.ifilm2_base + item['href']
        poster = config.ifilm2_base + \
            item.find('img', {'class': 'fill-box'})['src']
        add_dir(name, link, 'ifilm2_season_cat', poster,
                fanart, '', isFolder=True)

    if len(item_list) > 0:
        page = int(page) + 1
        add_dir('Next Page', url, 'ifilm2_shows_list', '', '', 'Next Page',
                foldername=foldername, page=page, isFolder=True)
    else:
        xbmcplugin.endOfDirectory(handle)


def ifilm_episodes(name, url, icon, description):
    response = ifilm_request(url)
    soup = ifilm_soup(url)
    serial_id = url.split('?')[0]
    serial_id = serial_id.split('/')[-1]

    serial_episode = re.findall(r'(?<=var inter_ = ).*?(?=;)', response)[0]
    for num in range(int(serial_episode)):
        icon = f'http://preview.presstv.ir/ifilm/{serial_id}/{num+1}.png'
        icon = icon.replace('?', '')
        name = 'Episode ' + str(num+1)
        description = soup.find(
            'div', {'class': 'Fulltext_panel'}).text.strip().replace('X', '')
        link = f'Https://vod.ifilmtv.ir/hls/{serial_id}/,{num+1},{num+1}_320,.mp4.urlset/master.m3u8'
        mp4_link = f'https://preview.presstv.ir/ifilm/{serial_id}/{num+1}.mp4'
        link = link.replace('?', '')
        add_dird(name, link, 'ifilm_episodes', icon, icon,
                 description, '', isFolder=False)


def ifilm2_episodes(name, url, icon, description):
    response = ifilm_request(url)
    soup = ifilm_soup(url)
    serial_id = url.split('?')[0]
    serial_id = 'da' + serial_id.split('/')[-1]

    serial_episode = re.findall(r'(?<=var inter_ = ).*?(?=;)', response)[0]
    for num in range(int(serial_episode)):
        icon = f'http://preview.presstv.ir/ifilm/{serial_id}/{num+1}.png'
        icon = icon.replace('?', '')
        name = 'Episode ' + str(num+1)
        description = soup.find(
            'div', {'class': 'Fulltext_panel'}).text.strip().replace('X', '')
        link = f'Https://vod.ifilmtv.ir/hls/{serial_id}/,{num+1},{num+1}_320,.mp4.urlset/master.m3u8'
        mp4_link = f'https://preview.presstv.ir/ifilm/{serial_id}/{num+1}.mp4'
        link = link.replace('?', '')
        add_dird(name, link, 'ifilm_episodes', icon, icon,
                 description, '', isFolder=False)


def ifilm_episode(name, url, icon, description):

    link = url
    play_manoto(name, link, icon, description)


def ifilm_menu():
    xbmcplugin.setPluginCategory(handle, 'ifilm')
    add_dir('ifilm Series', config.ifilm_series, 'ifilm_shows_list', '', '',
            'Latest ifilm Series', foldername='ifilm Series', isFolder=True)
    add_dir('ifilm 2 Series', config.ifilm2_series, 'ifilm2_shows_list', '', '',
            'Latest ifilm 2 Series', foldername='ifilm Series', isFolder=True)
