import news_api
from api_calls.openai_api import api_calls
from agents.CEO_persona import CEO
from agents.idea_generator import IdeaGenerator
# Import other agents as needed

class TaskGenerator:
    def __init__(self, ceo_agent, idea_agent, news_agent, tech_trends_agent=None, customer_feedback_agent=None, competitive_analysis_agent=None):
        self.ceo_agent = ceo_agent
        self.idea_agent = idea_agent
        self.news_api = news_agent
        self.tech_trends_agent = tech_trends_agent
        self.customer_feedback_agent = customer_feedback_agent
        self.competitive_analysis_agent = competitive_analysis_agent

    def generate_task(self):
        idea = self.idea_agent.generate_idea(api_calls, "Software Development")  # Assuming 'career' is specified here for simplicity
        news_insight = self.news_api.get_news()

        task = self._create_task_based_on_insights(idea, news_insight['articles'][0]['title'])  # Simplified to use the title of the first article

        if self.tech_trends_agent:
            # Assuming we're using the same news_api.get_news() for simplicity
            tech_insight = self.news_api.get_news()
            task = self._enhance_task_with_tech_insights(task, tech_insight['articles'][1]['title'])

        if self.customer_feedback_agent:
            # Similarly, using news_api.get_news() to simulate customer feedback for simplicity
            customer_feedback = self.news_api.get_news()
            task = self._enhance_task_with_customer_feedback(task, customer_feedback['articles'][2]['title'])

        self.report_to_ceo(task)
        return task

    def _create_task_based_on_insights(self, idea, news_insight):
        task_description = f"Develop a solution for: '{idea}', considering recent developments: '{news_insight}'."
        return {"task": "New Development Task", "details": task_description}

    def _enhance_task_with_tech_insights(self, task, tech_insight):
        enhanced_details = task['details'] + f" Incorporate latest technology trends: '{tech_insight}'."
        return {"task": task['task'], "details": enhanced_details}

    def _enhance_task_with_customer_feedback(self, task, customer_feedback):
        enhanced_details = task['details'] + f" Address customer feedback: '{customer_feedback}'."
        return {"task": task['task'], "details": enhanced_details}

    def report_to_ceo(self, task):
        employee_name = "TaskGenerator"
        employee_message = task['details']
        self.ceo_agent.review_employee(employee_name, employee_message, self.update_callback)

    def update_callback(self, message):
        print(message)

# Example usage
if __name__ == "__main__":
    ceo_agent = CEO()
    idea_agent = IdeaGenerator(api_calls, "Software Development")  # This assumes the IdeaGenerator is initialized with necessary arguments
    task_generator = TaskGenerator(ceo_agent, idea_agent, news_api)
    task_generator.generate_task()
