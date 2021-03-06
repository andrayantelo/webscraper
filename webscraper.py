from bs4 import BeautifulSoup
import requests
import json

url ='http://ethans_fake_twitter_site.surge.sh/'
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

tweets = soup.find_all('div', class_="tweetcontainer")
tweet_arr = []

for tweet in tweets:
    tweetObject = {
            "author": tweet.find('h2', class_="author").text,
            "date": tweet.find('h5', class_="dateTime").text,
            "tweet": tweet.find('p', class_="content").text,
            "likes": tweet.find('p', class_="likes").text,
            "shares": tweet.find('p', class_="shares").text
            }
    tweet_arr.append(tweetObject)
    data = json.dumps(tweet_arr) 
    with open('twitterData.json', 'w') as outfile:
        outfile.write(data)
