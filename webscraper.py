from bs4 import BeautifulSoup
import requests

url ='http://ethans_fake_twitter_site.surge.sh/'
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

tweet = soup.find_all('p', class_="content")

for el in tweet:

    print(el.text)
