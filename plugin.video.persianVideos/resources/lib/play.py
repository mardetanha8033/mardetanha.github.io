import requests
import json
import re
import sys
import xbmcplugin
from bs4 import BeautifulSoup
import xbmc
import xbmcgui
from urllib.parse import quote_plus, parse_qsl
from urllib.parse import urlencode, quote_plus
import urllib.parse
from resources.lib.utils import get_json, add_dir
handle = int(sys.argv[1])


def play_video(name, url, icon, description):
    liz = xbmcgui.ListItem(name)
    liz.setInfo('video', {'title': name, 'plot': description})
    liz.setArt({'thumb': icon, 'icon': icon})
    liz.setPath(url)
    #xbmc.Player().play(url, liz)
    xbmcplugin.setResolvedUrl(handle, True, liz)


def play_manoto(name, url, icon, description):
    liz = xbmcgui.ListItem(name)
    liz.setProperty('inputstream', 'inputstream.adaptive')
    liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
    #liz.setProperty('inputstream.adaptive.max_bandwidth',  'max')
    liz.setInfo('video', {'title': name, 'plot': description})
    liz.setArt({'thumb': icon, 'icon': icon})
    liz.setPath(url)
    #xbmc.Player().play(url, liz)
    xbmcplugin.setResolvedUrl(handle, True, liz)


def play_live(name, url, icon, description):
    json_data = get_json(url)
    icon = 'https://raw.githubusercontent.com/bbk79/xbmc-addons/master/plugin.video.manoto/resources/fhd.png'
    link = json_data['details'].get('liveUrl')
    add_dir(name, link, 'playy_live', icon, icon,
            description, '', isFolder=False)


def play_livve(name, url, icon, description):
    liz = xbmcgui.ListItem(name)
    liz.setInfo('video', {'title': name, 'plot': description})
    liz.setArt({'thumb': icon, 'icon': icon})
    xbmc.Player().play(url, liz)
