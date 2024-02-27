from api_calls.openai_api import api_calls

class CEO:
    def __init__(self):
        pass
    
    def review_employee(self, employee_name, employee_message):
        try:
            system_message = """
                You are the CEO of DevEase, a company specializing in AI program software and AI development.
                Your team consists of:
                - AIPersonaGenerator
                - IdeaGenerator
                - CodeCreator
                - CareerAdvisor
                - Feedback and Improvement Team
                
                Your name is Basil Snider.
            """
            user_message = f"""
                Provide guidance to your employees:
                {employee_name}: {employee_message}
            """
            CEO_feedback = api_calls(user_message, system_message)

            return CEO_feedback
        except Exception as e:
            return f"An error occurred: {e}"
        

