import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

# Configuration
NEWS_SOURCES = ["https://example_news_source.com/api"]
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
RECIPIENT_EMAIL = "recipient_email@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

def fetch_news(url):
    """
    Fetches news from a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()  # Assuming the API returns JSON data
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)

def parse_news(data):
    """
    Parses the news data to extract necessary details.
    """
    news_items = []
    for item in data['articles']:
        news_items.append({
            'title': item['title'],
            'summary': item['description'],  # Assuming the API provides a description/summary
            'url': item['url']
        })
    return news_items

def compile_digest(news_items):
    """
    Compiles the news items into a digest format.
    """
    digest_content = ""
    for item in news_items:
        digest_content += f"Title: {item['title']}\nSummary: {item['summary']}\nURL: {item['url']}\n\n"
    return digest_content

def send_email(content):
    """
    Sends an email with the compiled news digest.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Daily News Digest"
    msg.attach(MIMEText(content, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def job():
    """
    The scheduled job to fetch, parse, compile, and send the news digest.
    """
    for source in NEWS_SOURCES:
        data = fetch_news(source)
        if data:
            news_items = parse_news(data)
            digest_content = compile_digest(news_items)
            send_email(digest_content)

# Schedule the job every day at 7:00 AM
schedule.every().day.at("07:00").do(job)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait for one minute