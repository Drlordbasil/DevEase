
from api_calls.openai_api import api_calls
from agents.career_generator import CareerGenerator
class IdeaGenerator:
    def __init__(self):
        pass

    def generate_idea(self, update_callback):
        career = CareerGenerator().generate_career(update_callback)
        
        try:
            system_message=career
            User_message = """
            Based on the career path of becoming an entrepreneurial Python developer specialized in AI, I need a project idea that:

            - Aligns with the career trajectory of leveraging neural networks for generating video, images, or content.
            - Embodies innovation and entrepreneurial spirit, with potential for significant financial return.
            - Can be realistically initiated and scaled using Python and AI technologies to achieve profitability swiftly.

            The project should demonstrate practical application of AI in creating or enhancing value-added services or products, contributing to rapid wealth accumulation.
            """

            
            idea = api_calls(User_message, system_message)

            update_callback(f"Generated Idea: {idea}")
            return idea
        except Exception as e:
            update_callback(f"Error generating idea: {str(e)}")
            return ""
