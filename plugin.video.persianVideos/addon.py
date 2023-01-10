import sys
import xbmcplugin
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, parse_qsl
from urllib.parse import urlencode, quote_plus
import urllib.parse
from resources.lib import config
from resources.lib.utils import add_dir
from resources.lib.play import play_live, play_video, play_livve
from resources.lib.manoto import get_shows_list, get_season, get_episodes, manoto_menu, play_episode
from resources.lib.farsiland import get_categories, get_video_list, get_episode_list, shows_main, get_video
from resources.lib.irani_tv import get_tv_list, get_tv_episodes, tv_menu, play_tv
from resources.lib.ifilm import *

handle = int(sys.argv[1])


def main_menu():
    xbmcplugin.setPluginCategory(handle, 'Main Menu')
    add_dir('Farsiland', '', 'shows_main', config.farsiland_icon, config.farsiland_fanart,
            'Persian Movies and Series', isFolder=True)
    add_dir('Manoto', '', 'manoto_menu', config.manoto_icon, config.manoto_fanart,
            'Manoto TV Programs', isFolder=True)
    add_dir('Persian Series', '', 'tv_main', '',
            config.tv_fanart, 'Persian Series', isFolder=True)
    add_dir('ifilm', '', 'ifilm_main', config.ifilm_logo,
            config.ifilm_fanart, 'ifilm Series', isFolder=True)


def router():

    #---System Arguments---#

    p = dict(parse_qsl(sys.argv[2][1:]))
    mode = p.get('mode', 'main_menu')
    name = p.get('name', '')
    url = p.get('url', '')
    icon = p.get('icon', '')
    fanart = p.get('fanart', '')
    description = p.get('description', '')
    page = p.get('page', '')
    foldername = p.get('foldername', '')

    #---Modes---#

    if mode == 'main_menu':
        main_menu()

    elif mode == 'shows_main':
        shows_main()

    elif mode == 'manoto_menu':
        manoto_menu()
    elif mode == 'tv_main':
        tv_menu()
    elif mode == 'ifilm_main':
        ifilm_menu()

    elif mode == 'shows_list':
        get_categories(name, url, icon, fanart, description, foldername, page)

    elif mode == 'manoto_shows_list':
        get_shows_list(name, url, icon, fanart, description, foldername, page)
    elif mode == 'ifilm_shows_list':
        ifilm_shows_list(name, url, icon, fanart,
                         description, foldername, page)
    elif mode == 'ifilm2_shows_list':
        ifilm2_shows_list(name, url, icon, fanart,
                          description, foldername, page)

    elif mode == 'tv_show_list':
        get_tv_list(name, url, icon, fanart, description, foldername)

    elif mode == 'manoto_season_cat':
        get_season(name, url, icon, description)
    elif mode == 'manoto_episode_cat':
        get_episodes(name, url, icon, description)
    elif mode == 'ifilm_season_cat':
        ifilm_episodes(name, url, icon, description)
    elif mode == 'ifilm2_season_cat':
        ifilm2_episodes(name, url, icon, description)
    elif mode == 'tv_episode_cat':
        get_tv_episodes(name, url, icon, description)

    elif mode == 'season_cat':
        get_video_list(name, url, icon, description)

    elif mode == 'episode_cat':
        get_episode_list(name, url, icon, description)
    elif mode == 'tv_episodes':
        play_tv(name, url, icon, description)

    elif mode == 'episodes':
        get_video(name, url, icon, description)

    elif mode == 'manoto_episodes':
        play_episode(name, url, icon, description)

    elif mode == 'ifilm_episodes':
        ifilm_episode(name, url, icon, description)

    elif mode == 'live':
        play_live(name, url, icon, description)

    elif mode == 'playy_live':
        play_livve(name, url, icon, description)
    elif mode == 'play_video':
        play_video(name, url, icon, description)

    #---End the Directory---#

    xbmcplugin.endOfDirectory(handle)

#---Addon Begins Here---#


if __name__ == '__main__':
    router()
