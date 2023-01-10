import sys
import requests
import xbmcplugin
import xbmc
import xbmcgui
import json
import re
from urllib.parse import quote_plus, parse_qsl
import resources.lib.config as config
from bs4 import BeautifulSoup


def get_request(page):
    return requests.get(page, headers=config.headers).text


def get_soup(page):
    return BeautifulSoup(get_request(page), 'html.parser')


def get_list(page):
    return requests.get(page, headers=config.manoto_headers).text


def get_json(page):
    return json.loads(get_list(page))


def get_results(page):
    return get_json(page)['details']['list']


def ifilm_request(page):
    return requests.get(page, headers=config.ifilm_headers).text


def ifilm_soup(page):
    return BeautifulSoup(ifilm_request(page), 'html.parser')


def add_dir(name, url, mode, icon, fanart, description, page='', foldername='', addcontext=False, isFolder=True):
    u = sys.argv[0]+'?name='+quote_plus(name)+'&url='+quote_plus(url)+'&mode='+quote_plus(mode)+'&icon='+quote_plus(
        icon) + '&fanart='+quote_plus(fanart)+'&description='+quote_plus(description)+'&page='+str(page)+'&foldername='+quote_plus(foldername)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'fanart': fanart, 'icon': icon, 'thumb': icon, 'poster': icon})
    liz.setInfo(type='video', infoLabels={'title': name, 'plot': description})
    if addcontext:
        contextMenu = []
        liz.addContextMenuItems(contextMenu)
    xbmcplugin.addDirectoryItem(handle=int(
        sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)


def add_dird(name, url, mode, icon, fanart, description, page='', foldername='', addcontext=False, isFolder=True):
    u = sys.argv[0]+'?name='+quote_plus(name)+'&url='+quote_plus(url)+'&mode='+quote_plus(mode)+'&icon='+quote_plus(
        icon) + '&fanart='+quote_plus(fanart)+'&description='+quote_plus(description)+'&page='+str(page)+'&foldername='+quote_plus(foldername)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'fanart': fanart, 'icon': icon, 'thumb': icon, 'poster': icon})
    liz.setInfo(type='video', infoLabels={'title': name, 'plot': description})
    liz.setProperty('IsPlayable', 'true')
    if addcontext:
        contextMenu = []
        liz.addContextMenuItems(contextMenu)
    xbmcplugin.addDirectoryItem(handle=int(
        sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)


def next_pag(_url):
    item_list = []
    soup = get_soup(_url)
    for x in soup.findAll('div', {'class': 'resppages'}):
        a = x.find_all('a')
        """ if len(a) > 0:
            a = a[1]
        else:
            a = a[0] """
        for item in a:

            link = item['href']
            name = 'Next Page'
            item_list.append([name, link])
    return item_list
