from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from api_calls.openai_api import OpenAIAPI

class WebResearch:
    def __init__(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.openai_client = OpenAIAPI()

    def search_google(self, query):
        self.driver.get("https://www.google.com")
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(query + Keys.RETURN)

    def search_api(self, query, api_url):
        response = requests.get(api_url, params={"q": query})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code: {response.status_code}")

    def get_google_results(self):
        results = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tF2Cxc']"))
        )
        return [{'title': result.find_element(By.TAG_NAME, 'h3').text, 'link': result.find_element(By.TAG_NAME, 'a').get_attribute('href')} for result in results]

    def get_api_results(self, api_response):
        results = api_response.get("results", [])
        return [{'title': result.get('title'), 'link': result.get('url')} for result in results]

    def read_webpage(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = ' '.join([p.get_text() for p in soup.find_all('p')])
            return content
        else:
            raise Exception(f"Failed to load webpage: {url}")

    def analyze_content(self, content, query):
        system_prompt = f"You are an AI assistant that analyzes web content to provide insights and summaries related to a given query."
        user_prompt = f"Analyze the following content in the context of the query '{query}':\n\n{content}\n\nProvide a summary of the key points and insights related to the query."
        response = self.openai_client.api_calls(user_prompt, system_prompt)
        return response

    def search_and_analyze(self, query):
        self.search_google(query)
        search_results = self.get_google_results()
        
        summaries = []
        for result in search_results:
            try:
                content = self.read_webpage(result['link'])
                summary = self.analyze_content(content, query)
                summaries.append({"title": result['title'], "summary": summary})
            except Exception as e:
                print(f"Error analyzing content: {str(e)}")
        
        return summaries

    def close(self):
        self.driver.quit()