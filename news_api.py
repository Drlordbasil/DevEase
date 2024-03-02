import requests

class NewsFetcher:
    def __init__(self, api_key='817ce253061849c6abfdced81f961994', country='us'):
        """
        Initializes the NewsFetcher with a default API key and country.

        Args:
        - api_key (str): The API key for the NewsAPI. Default is 'Your_Default_API_Key'.
        - country (str): The country code for fetching news. Default is 'us'.
        """
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2/top-headlines'
        self.country = country

    def _construct_url(self):
        """Constructs the URL for the API request based on the country and API key."""
        return f"{self.base_url}?country={self.country}&apiKey={self.api_key}"

    def get_news(self):
        """Retrieves the top headlines for the specified country.

        Returns:
            list: A list of dictionaries containing information about each headline.
        """
        try:
            url = self._construct_url()
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
            news_data = response.json()
            return news_data.get('articles', [])
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve news: {e}")
            return []


