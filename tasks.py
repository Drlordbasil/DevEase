from api_calls.openai_api import api_calls 
from agents.idea_generator import IdeaGenerator

class TaskGenerator:
    def __init__(self):
        self.idea_gen = IdeaGenerator()

    def generate_task(self):
        idea = self.idea_gen.generate_idea()
        profitability_score = self._assess_profitability(idea)
        if profitability_score > 1.0:  # Assuming scores > 1 indicate high profitability
            task = f"Develop a solution based on: {idea}, which is assessed to be highly profitable."
        else:
            task = "Generated idea does not meet profitability criteria. Generating a new idea."
            print(profitability_score)
            return self.generate_task()  # Recursively generate a new task if not profitable enough
        


        return task

    def _assess_profitability(self, idea):
        system_message = "You are a profitability estimate expert that only returns a score between 0.0 to 2.0, analyzing the idea for your assessment. Only respond with the score number, nothing else."
        user_message = idea
        score = api_calls(user_message,system_message)  # Simplified API call
        print (score)
        return float(score)


