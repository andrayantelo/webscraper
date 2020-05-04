"""
    turn

    playlist = [ {'sources': [{},{}], 'image':'www.slkfjad.com', 'title': 'hello' }, ...]

    into
    [{'file': 'www.hello.com', 'title': 'art'}, {'file': 'www.world.com', 'title': 'art2'}]
"""
from bs4 import BeautifulSoup
from yaml import safe_load
import requests
import json
import re
import sys
import html
import os

pattern = re.compile("var jwPlaylists = \"(.*?)\";")

def get_title(soup):
    return soup.title.text

def get_playlist(soup):
    scripts = soup.find_all('script')

    script = [s for s in scripts if s.string and "jwPlaylists" in s.string]
    script = script[0]

    m = re.search("jwPlaylists = (.*?]);", script.string)
    playlist = safe_load(m.group(1))
    return playlist

def get_best_videos(playlist):
    videos = []
    for p in playlist:
        video = {}
        video['title'] = p['title']
        best = max(p['sources'], key=lambda f: f['height']*f['width'])
        video['file'] = best['file']
        videos.append(video)
    return videos

def download_videos(videos, lesson_title):
    # make a directory to keep the videos in
    video_directory = '../../Drawing/nma_lessons/'
    video_directory = os.path.join(video_directory, lesson_title)
    os.makedirs(video_directory, exist_ok=True)
    # for each video, download it and put it in the directory

def main():

    with open('source.txt', 'r') as f:
        urls = f.readlines()

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(html.unescape(response.text), "html.parser")
        playlist = get_playlist(soup)
        videos = get_best_videos(playlist)
        print(videos)

if __name__ == "__main__":
    main()
