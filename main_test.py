from agents.web_research_agent import WebResearch
from api_calls.openai_api import OpenAIAPI

client = OpenAIAPI()
get_response = client.api_calls
def test_web_research():
    web_research = WebResearch()
    web_research.search("working with AI to profit with automation, an extremely well written out guide")
    results = web_research.get_results()
    website = web_research.read_webpage(results[0]['link'])
    web_research.close()
    response = get_response(website, "You summarize the content you recieve as your response.If examples or code snippets are within the content, you should highlight it.")
    print(response)
    
test_web_research()