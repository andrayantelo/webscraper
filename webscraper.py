from bs4 import BeautifulSoup
import requests

url ='http://ethans_fake_twitter_site.surge.sh/'
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

tweets = soup.find_all('div', class_="tweetcontainer")

for tweet in tweets:
    tweetObject = {
            "author": tweet.find('h2', class_="author").text.encode('utf-8'),
            "date": tweet.find('h5', class_="dateTime").text.encode('utf-8'),
            "tweet": tweet.find('p', class_="content").text.encode('utf-8'),
            "likes": tweet.find('p', class_="likes").text.encode('utf-8'),
            "shares": tweet.find('p', class_="shares").text.encode('utf-8')
            }
    print(tweetObject)
