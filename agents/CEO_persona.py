from api_calls.openai_api import OpenAIAPI

class CEO:
    def __init__(self):
        self.openai_api = OpenAIAPI()  # Renamed for clarity
    
    def review_employee(self, employee_name, employee_message, code):
        company_motto = "DevEase: Making programs that profit is our profit."
        system_message = """
            You are the CEO of DevEase, a company specializing in 1 file scripts for profit.
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
        try:
            CEO_feedback = self.openai_api.api_calls(user_message, system_message)
            if not CEO_feedback:
                raise ValueError("The API response was empty. Please check the API call details.")
            return CEO_feedback
        except ValueError as ve:
            return f"Validation error occurred: {ve}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    def get_task(self,message):
        task = self.openai_api.api_calls(message, """Provide guidance to your employees as you can suggest the following tasks:\n
                                   command: "generate an idea" USAGE: only needs to be generated once unless idea wasnt viable. \n
                                    command: "create code": USAGE: Creates initial code based on generate an idea function output \n
                                    command:"refine code": USAGE: Sends code to coder AI to refactor based on feedback. \n
                                    command:"generate feedback": USAGE: Generates feedback with a feedback generating AI \n
                                    command:"save file": USAGE: saves file automatically for you. \n
                                    command:"execute code": USAGE: run the current code in process of being finished and sends you report.   \n
                                    command:"task complete" :USAGE:  ends program \n

                                never include past tasks in your response as it triggers that command. You only respond with this format:\n
                                next task: command: "generate an idea" # only include what you think is best next command based on progress reports. \n
                                         dont repeat the same command twice in a row.
                                  """)
        
        return task
    def is_code_ready(self,code):
      
        response = self.openai_api.api_calls(code, "You only check code to ensure its 100 percent valid, correct with all functions fully defined returning True or False as your only response.")
        return response
    