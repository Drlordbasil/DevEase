from api_calls.openai_api import api_calls



class CEO:
    def __init__(self):
        pass
        # review the employee using CEO persona
    def review_employee(self, employee_name, employee_message):
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
            You're name is Basil Snider, the CEO of DevEase.
            
                """
            user_message = f"""
    give your employees guidance
    {employee_name}: {employee_message}

        """
            CEO_feedback = api_calls(user_message, system_message)
            return CEO_feedback
        except:
             # Handle the exception here
            pass

