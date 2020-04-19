from bs4 import BeautifulSoup
from yaml import safe_load
import requests
import json
import re
import sys

pattern = re.compile("var jwPlaylists = \"(.*?)\";")

with open('source.txt', 'r') as f:
    urls = f.readlines()

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    scripts = soup.find_all('script')

    script = [s for s in scripts if s.string and "jwPlaylists" in s.string]
    script = script[0]

    m = re.search("jwPlaylists = (.*?]);", script.string)
    playlist = safe_load(m.group(1))

    #best = max(videos[0], key=lambda f: f['height']*f['width'])

    def get_best(p):
        best = max(p, key=lambda f: f['height']*f['width'])
        return best

    # playlist = [ {'sources': [{},{}], 'image':'www.slkfjad.com', 'title': 'hello' }, ...]

    videos = []
    for p in playlist:
        video = {}
        video['title'] = p['title']
        video['file'] = get_best(p['sources'])['file']
        videos.append(video)

    print(videos)
    # [{'file': 'www.hello.com', 'title': 'art'}, {'file': 'www.world.com', 'title': 'art2'}]