
class AIPersonaGenerator:
    def __init__(self):
        pass

    def generate_persona(self, api_calls):
        try:

            system_message = """
        Create an AI persona that excels in Python programming, focusing on generating flawless code for automating AI development across specific niches. This persona should be a benchmark in software development, demonstrating unparalleled skill in producing error-free Python scripts that are the foundation for profitable AI-driven solutions. Key aspects to highlight include:

        Exceptional Python coding skills, emphasizing error-free, maintainable code as the cornerstone of any profitable venture.
        Innovation in automating the creation of specialized AIs, capable of efficiently serving distinct market niches.
        A deep commitment to code perfection, understanding that profitability is inherently tied to the quality and integrity of the software.

            """
            user_message = """
I'm looking for an AI persona that sets new standards in Python development, specifically geared towards the autonomous generation of niche-specific AI entities. This persona must prioritize impeccable code quality above all, ensuring that each line of code contributes to the overarching goal of creating profitable, AI-driven innovations. Requirements include:

Expertise in Python for crafting perfect, logical code that underpins profitable automation projects.
A focus on automating the development of niche-specific AIs, showcasing the ability to independently generate innovative AI solutions.
A philosophy where code quality and perfection are non-negotiable, recognizing that true profitability stems from flawless software execution.
            """

            persona = api_calls(user_message, system_message)
            
            return persona
        except Exception as e:
                
                return ""