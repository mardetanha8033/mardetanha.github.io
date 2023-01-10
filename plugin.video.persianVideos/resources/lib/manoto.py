import sys
import xbmcplugin
import xbmc
import xbmcgui
import resources.lib.config as config
from resources.lib.play import play_manoto
from resources.lib.utils import get_request, get_soup, get_json, get_list, get_results, add_dir, add_dird, next_pag

handle = int(sys.argv[1])


def get_shows_list(name, url, icon, fanart, description, foldername,  page):
    xbmcplugin.setPluginCategory(handle, foldername)
    xbmcplugin.setContent(handle, 'tvshows')
    if page == '':
        page = 1

    item_list = get_results(f'{url}&pageNumber={page}')
    #item_list = get_results(url)
    for item in item_list:
        name = item.get('displayTitle', '')
        _id = item.get('id', '')
        icon = item.get('portraitImgIxUrl', '')
        fanart = item.get('portraitImgIxUrl', '')
        description = str(item.get('delimitedGenres', ''))  # slam edit
        season_url = f'https://dak1vd5vmi7x6.cloudfront.net/api/v1/publicrole/showmodule/serieslist?id={_id}'
        add_dir(name, season_url, 'manoto_season_cat', icon,
                fanart, description, isFolder=True)
    if len(item_list) > 0:
        page = int(page) + 1
        add_dir('Next Page', url, 'manoto_shows_list', '', '', 'Next Page',
                foldername=foldername, page=page, isFolder=True)
    else:
        xbmcplugin.endOfDirectory(handle)


def get_season(name, url, icon, description):
    results = get_results(url)
    #item_list = []
    for result in results:
        season_name = result.get('seasonNumber')
        if len(season_name) > 1:
            name = 'Season ' + season_name
        else:
            name = 'Season 0' + season_name
        #name = 'Season  ' + result.get('seasonNumber')
        season_id = result.get('id')
        link = f'https://dak1vd5vmi7x6.cloudfront.net/api/v1/publicrole/showmodule/episodelist?id={season_id}'
        add_dir(name, link, 'manoto_episode_cat',
                '', '', '', '', isFolder=True)


def get_episodes(name, url, icon, description):
    results = get_results(url)
    xbmc.log('results= '+str(results), xbmc.LOGINFO)
    item_list = []
    for result in results:
        episode_name = result.get('episodeNumber')
        if len(episode_name) > 1:
            name = 'Episode ' + episode_name
        else:
            name = 'Episode 0' + episode_name
        #name = 'Episode ' + result.get('episodeNumber')
        icon = result.get('landscapeImgIxUrl')
        description = result.get('showTitle')
        epis_id = result.get('id')
        link = f'https://dak1vd5vmi7x6.cloudfront.net/api/v1/publicrole/showmodule/episodedetails?id={epis_id}'
        add_dird(name, link, 'manoto_episodes', icon, icon,
                 description, '', isFolder=False)


def play_episode(name, url, icon, description):
    json_data = get_json(url)
    linkk = json_data['details'].get('videoM3u8Url')
    link = "".join(linkk.split())
    description = json_data['details'].get('episodeDescription')
    # I tryied to clean description string but still I have some unwanted br tags
    description = description.replace('<br>', '').replace('&nbsp;', '').replace('&zwnj;', '').replace('&hellip;', "").replace(
        '<p>', '').replace('<br />', '').replace('</p>', '').replace('&laquo;', '').replace('&raquo;', '')
    # I wanna use background and clearlogo from here into get_shows_list function
    background = json_data['details'].get('backgroundImgIxUrl')
    clearlogo = json_data['details'].get('overlayImgIxUrl')
    play_manoto(name, link, icon, description)


def manoto_menu():
    xbmcplugin.setPluginCategory(handle, 'Manoto')
    add_dir('Latest Episodes', config.manoto_catchup, 'manoto_episode_cat', '', '',
            'Latest Episodes', foldername='Latest Episodes', isFolder=True)
    add_dir('Manoto Original', config.manoto_original, 'manoto_shows_list', '', '',
            'Manoto Original', foldername='Manoto Original', isFolder=True)
    add_dir('Entertainment', config.manoto_entertainmnt, 'manoto_shows_list', '', '',
            'Entertainment', foldername='Entertainment', isFolder=True)
    add_dir('Drama', config.manoto_drama, 'manoto_shows_list', '', '',
            'Drama', foldername='Drama', isFolder=True)
    add_dir('Comedy', config.manoto_comedy, 'manoto_shows_list', '', '',
            'Comedy', foldername='Comedy', isFolder=True)
    add_dir('Latest Show', config.manoto_latest, 'manoto_shows_list', '', '',
            'Latest programs', foldername='Latest', isFolder=True)
    add_dir('Popular Show', config.manoto_popular, 'manoto_shows_list', '', '',
            'Popular programs', foldername='Popular', isFolder=True)
    add_dir('Alphabet Show', config.manoto_az, 'manoto_shows_list', '', '',
            'Alphabetical Order', foldername='Alphabet', isFolder=True)
    add_dir('Manoto Live', config.manoto_live, 'live', '', '',
            'Live Stream', foldername='Manoto Live', isFolder=True)
