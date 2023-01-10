import sys
import xbmcplugin
import xbmc
import xbmcgui
import resources.lib.config as config
from resources.lib.play import play_video
from resources.lib.utils import get_request, get_soup, get_json, get_list, get_results, add_dir, add_dird, next_pag

handle = int(sys.argv[1])


def get_tv_list(name, url, icon, fanart, description, foldername):
    xbmcplugin.setPluginCategory(handle, foldername)
    xbmcplugin.setContent(handle, 'tvshows')
    results = get_results(url)
    for item in results:
        name = item.get('name')
        url = item.get('url')
        fanart = item.get('fanart')
        poster = item.get('poster')
        add_dir(name, url, 'tv_episode_cat',
                poster, fanart, '', '', isFolder=True)


def get_tv_episodes(name, url, icon, description):
    results = get_results(url)
    for item in results:
        name = item.get('name')
        url = item.get('url')
        poster = item.get('poster')
        add_dird(name, url, 'tv_episodes', poster, '',
                 '', '', isFolder=False)


def play_tv(name, url, icon, description):
    link = url
    play_video(name, link, icon, '')


def tv_menu():
    xbmcplugin.setPluginCategory(handle, 'Persian Tv Series')
    add_dir('Latest Series', config.tv_url, 'tv_show_list', '', '',
            'Latest Series', foldername='Latest Series', isFolder=True)
