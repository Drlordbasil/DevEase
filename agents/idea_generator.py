
import subprocess
from api_calls.openai_api import OpenAIAPI



def find_pip_installed_packages():
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return result.stdout
libraries = find_pip_installed_packages()
class IdeaGenerator:
    def __init__(self):
        self.create = OpenAIAPI()

    def generate_idea(self):
        
        career  = self.create.api_calls("create a career persona for an AI developer specializing in Python. This career must be focused on idea generation of projects.", "you are a career specialist")
        try:
            system_message=career
            User_message = f"""
            Using the career advice provided, your task is to generate a groundbreaking project idea for an entrepreneurial Python developer specializing in AI. This idea should leverage neural networks for creating innovative video, images, or content, encapsulating both innovation and the potential for substantial financial returns. The project must:

            Be rooted in Python and AI technologies, showcasing how these tools can be utilized for significant market impact.
            Have a "WOW" factor, with the potential to shock the world and contribute positively to society.
            Demonstrate practical AI applications for creating or enhancing value-added services or products, aiming for rapid monetization.
            dont overthink it, just be creative and think of something that would be cool to see in the world that is plausible for an AI to create.
            the idea should be something that is not already in the market, and it should be something that is not too far fetched.
            The idea must be able to be done within 3 responses from the AI.
            
            
            """

            
            idea = self.create.api_calls(User_message, system_message)

            
            return idea
        except Exception as e:
            return ""
