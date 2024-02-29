
import requests
def get_news():
    url = ('https://newsapi.org/v2/top-headlines?'
            'country=us&'
            'apiKey=817ce253061849c6abfdced81f961994')
    news_report = requests.get(url)
    return news_report.json()
