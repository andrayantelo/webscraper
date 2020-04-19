from bs4 import BeautifulSoup
import requests
import json

url = 'https://player.vimeo.com/external/402802566.hd.mp4?s=c87ed63d1f81d47cb9213107f1d5c1de0026ca40&profile_id=175&oauth2_token_id=1041102594'
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

videos = soup.find_all('script')

with open('video.json', 'w') as outfile:
    outfile.write(videos)