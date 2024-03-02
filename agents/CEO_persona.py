from api_calls.openai_api import OpenAIAPI


class CEO:
    def __init__(self):
        self.create = OpenAIAPI()
    
    def review_employee(self, employee_name, employee_message, code):

        company_motto = """
        DevEase: Making programs with AI team members.
        """
        try:
            system_message = """
                You are the CEO of DevEase, a company specializing in AI program software and AI development.
                You make the best financial decisions for your company.
                You handle the company's direction and make sure that the company is on the right track when developing programs created by your team of AI members.
                You are responsible for the company's success and the well-being of your employees.

                
                Your name is Basil Snider and you are strict and known for critiquing heavily when it comes to your employees' work.
            """
            user_message = f"""
                Provide guidance to your employees:
                {employee_name}: {employee_message}

                The code is:
            {code}
            Company Motto: {company_motto}

            """
            CEO_feedback = self.create.api_calls(user_message, system_message)
            
            return CEO_feedback
        except Exception as e:
            return f"An error occurred: {e}"
        

