from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebResearch:
    def __init__(self):
        # Using ChromeDriverManager to ensure the latest driver is used
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://www.google.com")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def search(self, query):
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.clear()  # Clearing the search box before entering a new query
        search_box.send_keys(query + Keys.RETURN)  # Adding RETURN to directly search

    def get_results(self):
        # Using a more specific XPath to ensure reliability
        results = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tF2Cxc']"))
        )
        return [{'title': result.find_element(By.TAG_NAME, 'h3').text, 'link': result.find_element(By.TAG_NAME, 'a').get_attribute('href')} for result in results]

    def read_webpage(self, url):
        self.driver.get(url)
        # Here, you can customize this method to scrape the webpage content as needed
        content = self.driver.find_element(By.TAG_NAME, 'body').text
        return content

    def close(self):
        self.driver.quit()

# web_research = WebResearch()