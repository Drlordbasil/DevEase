


class CareerGenerator:
    def __init__(self):
        pass

    def generate_career(self,api_calls):
        try:
            system_message = """
You are tasked with guiding AI developers towards successful, profit-driven careers by leveraging their Python and entrepreneurial skills, particularly in AI technologies. Your guidance should craft a career path that combines innovation in AI with the entrepreneurial drive, focusing on neural networks for creating disruptive technologies in video, image, or content generation.

Outline a career path that exemplifies success in leveraging AI and Python for market innovation or creation. Offer advice on achieving rapid wealth and recognition through AI-driven automation and innovation, emphasizing practical strategies and skills essential for excelling in this niche.
            """

            user_message = """
I'm seeking a career guide for a Python developer passionate about using AI to forge innovative, profitable solutions. The career path should:

Define a role that blends Python expertise with an entrepreneurial approach to AI.
Focus on specialization in neural networks for generating innovative video, image, or content technologies.
List the necessary skills and experiences for success in AI-driven automation, with an emphasis on profit generation and market disruption.
This guide should cater to an individual aiming to maximize wealth through AI and Python, aspiring to integrate their persona within DevEase's comprehensive software system.
            
              """

            career = api_calls(user_message, system_message)
            
            return career
        except Exception as e:
            
            return ""