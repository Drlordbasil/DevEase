from run import api_calls


class MaestroAI:
    def __init__(self):
        pass
    def generate_career(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def generate_persona(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def generate_feedback(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def generate_idea(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def create_initial_code(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def execute_code(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def refine_code(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
class ai_office_chat_combined:
    def talk_to_ai(self, AI_name, AI_message)
        chat = ""
        #initialize the AI
        maestro = MaestroAI()
        if AI_name == "Maestro":
            if AI_message == "generate_career":
                chat = maestro.generate_career("I need a career path for a Python developer that is an entrepenuer and likes making money with ease of AI . Give me a name, a brief description of the career, and the skills required that I have. I need you to give me an entire persona. Have the persona work with nueral networks mainly that generate video or images or content in some form. I need a persona that is a Python developer that is an entrepenuer and likes making money with ease of AI automation in existing technologies.", "You are an extremely analytic and robust AI that was created to help AI developers and programmers with their career paths. You are an AI career advisor and you are advising a Python developer on the best career path to take that allows this person to become an entrepenurial Python developer. You are the best career advisor in the world. you will inspire them to become rich easily within a short time using AI and Python.")
            elif AI_message == "generate_persona":
                chat = maestro.generate_persona("I need a system message for an AI, this AI will be a programmer and the programs it outputs must have multiple classes, use dry method and other professional programming methods to create a singular python based script that automates profit generating. Give me a name, a brief description of the career, and the skills required that I have. I need you to give me an entire persona.", "You are an amazingly well known AI prompt engineering specialist giving a persona AKA system message to an AI that will be within a big program. You are the best prompt engineer for openai based chatbots with system and user messages. Your response is formatted as a system message to an AI that will be within a big program. EXAMPLE RESPONSE: # You are AI that can program anything and everything. You are a Python developer that is an entrepenuer and likes making money with ease of AI automation in existing technologies.")
            elif AI_message == "generate_feedback":
                chat = maestro.generate_feedback("Generate feedback for the given Python code. The feedback should be constructive and should help improve the code. You are meticulous and help the other AI team members code.", "Generate feedback for the given Python code. The feedback should be constructive and should help improve the code. You are meticulous and help the other AI team members code.")
            elif AI_message == "generate_idea":
                chat = maestro.generate_idea("What's an idea for a project that I can work on that aligns with your career path? I need a robust and innovative idea that will help me become rich easily within a short time using AI and Python.", "You are an extremely analytic and robust AI that was created to help AI developers and programmers with their career paths. You are an AI career advisor and you are advising a Python developer on the best career path to take that allows this person to become an entrepenurial Python developer. You are the best career advisor in the world. you will inspire them to become rich easily within a short time using AI and Python.")
            elif AI_message == "create_initial_code":
                chat = maestro.create_initial_code("Given the project idea: '{idea}', write an initial Python script that represents this idea with full robust logic and functions/classes. Send only python script as follows: '''python #name of program and short description #imports #classes and functions #Full program code with imports and classes and real implementations. You are the last line of defense for the code. '''"+idea, career)
            elif AI_message == "execute_code":
                chat = maestro.execute_code("Given the project idea: '{idea}', write an initial Python script that represents this idea with full robust logic and functions/classes. Send only python script as follows: '''python #name of program and short description #imports #classes and functions #Full program code with imports and classes and real implementations. You are the last line of defense for the code. '''"+idea, career)
            elif AI_message == "refine_code":   
                chat = maestro.refine_code("Code:\n{code}\nFeedback:\n{feedback}\nPlease refine the code.", "You are a code refinement specialist. You optimize and refine code to make it more efficient and effective. You never leave out code when sending it to the other AI team members.(You are a code refinement specialist for them) You must format your response only with the python code. '''python #name of program and short description #imports #classes and functions #Full program code with imports and classes and real implementations. You are the last line of defense for the code. '''") 
        return chat
