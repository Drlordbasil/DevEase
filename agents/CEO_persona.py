from api_calls.openai_api import api_calls

class CEO:
    def __init__(self):
        pass

    def create_initial_code(self, idea, update_callback, employee_name, employee_message, code):
        try:
            system_message = """
                You are a CEO of a company made up of a team of AI that follows:
                - AIPersonaGenerator
                - IdeaGenerator
                - CodeCreator
                - CareerAdvisor
                - feedback and improvement team
            You will always make decisions for the company to properly function and make profit.
            Your company's name is DevEase: The AI program software and AI development company.

            """
            user_message = f"""
give your employees guidance
{employee_name}: {employee_message}
   The current idea is: {idea}
    the current code is: {code}
    """
            CEO_feedback = api_calls(user_message, system_message)
            return CEO_feedback
        except Exception as e:
            update_callback(f"Error creating initial code: {str(e)}")
            return ""
# Path: agents/idea_generator.py
        