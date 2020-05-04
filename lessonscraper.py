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
import logging

pattern = re.compile("var jwPlaylists = \"(.*?)\";")
logging.basicConfig(level=logging.DEBUG)

def get_title(soup):
    title = soup.title.text
    return title.replace(' - New Masters Academy', '')

def sanitize(filename):
    filename = re.sub(r'\W+', '_', filename)
    return filename

def get_playlist(soup):
    # returns list of videos
    scripts = soup.find_all('script')

    script = [s for s in scripts if s.string and "jwPlaylists" in s.string]
    script = script[0]
    
    m = re.search("jwPlaylists = (.*?]);", script.string)
    if not m:
        title = get_title(soup)
        logging.warning("jwPlaylists not found for %s", title)
        return []
    # safe_load reads Json and gives you back python
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
    logging.info("Found %s videos", len(videos))
    return videos

def download_videos(videos, lesson_title):
    # make a directory to keep the videos in
    video_directory = '../../Drawing/nma_lessons/'
    video_directory = os.path.join(video_directory, lesson_title)
    os.makedirs(video_directory, exist_ok=True)
    # for each video, download it and put it in the directory
    for video in videos:
        logging.info("Start %s", video['file'])
        r = requests.get(video['file'])
        try:
            r.raise_for_status()
        except:
            logging.warning("Unable to download video: %s", video['file'])
            continue   
        filename = sanitize(video['title'])
        filepath = os.path.join(video_directory, filename)
        with open(filepath, 'wb') as f:
           f.write(r.content)
        logging.info("End %s", video['file'])

def main():

    with open('source.txt', 'r') as f:
        urls = f.readlines()

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(html.unescape(response.text), "html.parser")
        playlist = get_playlist(soup)
        videos = get_best_videos(playlist)
        lesson_title = sanitize(get_title(soup))
        download_videos(videos, lesson_title)

if __name__ == "__main__":
    main()
