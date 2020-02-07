import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import choice
from itertools import cycle
import pandas as pd

PROXIES = ['50.117.15.220:21312', '100.42.16.196:21263', '38.102.129.98:21327', '38.93.239.121:21258', '38.103.26.5:21244']
DF_COLUMNS = ['name', 'link', 'views', 'average_view_duration', 'watch_time_minutes', 'average_percentage_viewed', 'watch_time_hours']

def read_playlists_csv(filename):
    playlists = pd.read_csv(filename)
    return playlists.rename(columns={'traffic_source_detail': 'name'})

def save_playlists_csv(playlists, filename):
    playlists.to_csv("output/"+filename+".csv", index=False)
    return True

def empty_playlists_df():
    return pd.DataFrame(columns=DF_COLUMNS)

def find_all_playlists(playlists, filename):
    """
    Find official playlists for an entire csv of playlist names in parallel
    Args:
        names (Iterable): List of playlist names
    Returns:
        List: list of links to the official playlists
    """

    playlists_updated = empty_playlists_df()
    proxies = PROXIES
    proxy_pool = cycle(proxies)

    for idx, playlist in playlists.iterrows():
        playlist['link'] = find_playlist([playlist['name'], next(proxy_pool)])
        playlists_updated = playlists_updated.append(pd.Series(playlist, index=DF_COLUMNS))
        print("Playlist ", idx)
        sleep(2) # delay for 2 seconds

    return save_playlists_csv(playlists_updated, filename)

def trim_args(args):
    name, proxy = args

    name = name.replace("Mix -", "").replace('&', '%26')
    trimmed_name = str(name).strip().lower()

    return (trimmed_name, proxy)

# get a random proxy from a list of proxies
def get_proxy():
    return choice(PROXIES)

def find_playlist(args):
    """
    Find official playlist link given a playlist name on YT
    args (tuple):
        args[0] (str): name of the playlist
    Returns:
        String: playlist_id - link to the playlist on YT
    """
    name, proxy = trim_args(args)

    base_string = "https://www.youtube.com/results?search_query="
    query_string = name
    url = base_string+query_string

    # if no proxy is provided, get a random proxy to use
    if not proxy:
        proxy = get_proxy()

    r = requests.get(url, proxies={'http': proxy})

    page = r.text
    soup=bs(page,'html.parser')

    link_list=[]

    for link in soup.findAll('div',attrs={'class':'yt-lockup-content'}):
        title_link = link.find('a',attrs={'class':'yt-uix-tile-link'})

        if ('/watch?v=' in title_link['href']):
            link_obj = {
                'title': title_link['title'].strip().lower(),
                'channel_name': get_channel_name(link.find('a',attrs={'class':'yt-uix-sessionlink spf-link'})),
                'link': title_link['href'].split('?v=')[1]
            }

            link_list.append(link_obj)

    links = score_links(link_list, name)

    return links

def get_channel_name(tag):
    try:
        channel_name = str(tag).split('>')[1].split('<')[0]
    except:
        channel_name = ''

    return str(channel_name).strip().lower().replace('&amp;', '&')

def score_links(link_list, name):
    if not link_list:
        return None

    scores_arr = []
    best_link = {'score': 0, 'link': link_list[0]['link']}
    for link in link_list:
        score = 0
        score += score_title(link['title'], name)
        score += score_channel(link['channel_name'])

        if score > best_link['score']:
            best_link['score'] = score
            best_link['link'] = link['link']

    return best_link['link']

def score_title(title, name):
    mix_name = "mix - " + name
    if mix_name == title:
        return 100
    elif name in title and 'mix' in title:
        return 70
    return 0

def score_channel(channel_name):
    # if it is a youtube official channel
    if channel_name == "youtube":
        return 100
    elif channel_name == "":
        return 50

    return 0
