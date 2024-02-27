
from api_calls.openai_api import api_calls
from agents.career_generator import CareerGenerator
import subprocess

def find_pip_installed_packages():
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return result.stdout
libraries = find_pip_installed_packages()
class IdeaGenerator:
    def __init__(self):
        pass

    def generate_idea(self, update_callback):
        career = CareerGenerator().generate_career(update_callback)
        
        try:
            system_message=career
            User_message = f"""
            Based on the career path of becoming an entrepreneurial Python developer specialized in AI, I need a project idea that:

            - Aligns with the career trajectory of leveraging neural networks for generating video, images, or content.
            - Embodies innovation and entrepreneurial spirit, with potential for significant financial return.
            - Can be realistically initiated and scaled using Python and AI technologies to achieve profitability swiftly.

            The project should demonstrate practical application of AI in creating or enhancing value-added services or products, contributing to rapid wealth accumulation.
            make the idea a WOW factor Idea that could shock the world and make it a better place.

            you have the following libaries you can use:
            {libraries}

            You are within a company of AI developers and programmers, and your role is to create the initial Python script that will be the foundation of a project. The script should reflect the project's ambition and the company's commitment to quality and innovation in Python programming. The script should be designed to maximize wealth and recognition, showcasing the potential of AI and Python as tools for unprecedented automation and innovation. The name of the company is DevEase, and the AI persona will be integrated into a comprehensive software system.
            The name of the company is DevEase, and the AI persona will be integrated into a comprehensive software system.
            
            """

            
            idea = api_calls(User_message, system_message)

            update_callback(f"Generated Idea: {idea}")
            return idea
        except Exception as e:
            update_callback(f"Error generating idea: {str(e)}")
            return ""
