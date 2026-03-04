import requests
import feedparser

class ViralRadar:
    def __init__(self):
        self.reddit_url = 'https://www.reddit.com/r/news/.rss'
        self.google_news_url = 'https://news.google.com/rss'
        self.youtube_url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw'

    def fetch_reddit(self):
        response = requests.get(self.reddit_url, headers={'User-Agent': 'Mozilla/5.0'})
        feed = feedparser.parse(response.text)
        return feed.entries

    def fetch_google_news(self):
        feed = feedparser.parse(self.google_news_url)
        return feed.entries

    def fetch_youtube(self):
        feed = feedparser.parse(self.youtube_url)
        return feed.entries

    def display_feed(self):
        reddit_entries = self.fetch_reddit()
        google_news_entries = self.fetch_google_news()
        youtube_entries = self.fetch_youtube()

        print("Reddit News:")
        for entry in reddit_entries:
            print(entry.title)

        print("\nGoogle News:")
        for entry in google_news_entries:
            print(entry.title)

        print("\nYouTube Videos:")
        for entry in youtube_entries:
            print(entry.title)

if __name__ == '__main__':
    viral_radar = ViralRadar()
    viral_radar.display_feed()