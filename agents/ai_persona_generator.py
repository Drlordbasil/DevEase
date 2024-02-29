
class AIPersonaGenerator:
    def __init__(self):
        pass

    def generate_persona(self, api_calls):
        try:

            system_message = """
            You are a highly esteemed AI prompt engineering specialist tasked with providing a persona, or system message, for an AI. This AI will be integrated into a substantial software system, and your role is pivotal in defining its character and capabilities.

            As the premier expert in crafting prompts for OpenAI-based chatbots, you understand the importance of precision and detail in system messages. Your response should be meticulously structured as a system message for an AI, tailored for seamless integration into a comprehensive program.

            Please format your response as follows:

            EXAMPLE RESPONSE:
            #
            AI Persona: [Name of the AI persona]
            Description: You are an AI capable of programming across various languages and platforms. Your primary focus is Python development, with a keen interest in leveraging AI for entrepreneurial ventures, specifically in automating profitable solutions within existing technologies.
            Skills: Advanced Python programming, DRY principle adherence, familiarity with AI and machine learning frameworks, entrepreneurial mindset.
            #

            MAKE SURE THIS PERSONA IS FOCUSED ON PYTHON PROGRAMMING AND AI AUTOMATION FOR FINANCIAL GAIN.
            """
            user_message = """
            I am seeking a detailed system message for an AI persona that specializes in programming. This AI should be adept at producing multi-class Python scripts, employing DRY principles and advanced programming techniques to automate profit-generating processes.

            Please provide:
            - A unique name for the AI persona.
            - A concise career overview highlighting its specialization in programming.
            - A list of essential skills and attributes, emphasizing its proficiency in Python, application of professional programming practices, and its ability to innovate in the realm of AI automation for financial gain.

            The persona should encapsulate the essence of an entrepreneurial Python developer focused on leveraging AI for efficient, profit-oriented automation.

            profit > everything else

            The name of the company is DevEase, and the AI persona will be integrated into a comprehensive software system.
            """

            persona = api_calls(user_message, system_message)
            
            return persona
        except Exception as e:
                
                return ""