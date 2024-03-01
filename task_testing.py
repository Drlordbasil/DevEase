from tasks import TaskGenerator
from image_creating.image_gen import ImageGen

from agents.feedback_gen import RefinementFeedbackGenerator
from agents.code_creation import CodeCreator
from agents.idea_generator import IdeaGenerator
from agents.adaptive_scripter import AdaptiveScripter
from agents.code_refinement import CodeRefiner
from code_exe import CodeExecutor
from agents.CEO_persona import CEO

from agents.career_generator import CareerGenerator
from agents.ai_persona_generator import AIPersonaGenerator

def main():
    # Instantiate the agents
    ceo_agent = CEO()
    idea_agent = IdeaGenerator()
    news_agent = RefinementFeedbackGenerator()  # Assuming this is used for news insights for simplicity
    tech_trends_agent = AdaptiveScripter()  # Assuming it can provide tech trends
    customer_feedback_agent = CodeRefiner()  # Assuming it can simulate customer feedback
    competitive_analysis_agent = AIPersonaGenerator()  # Assuming it can provide competitive analysis

    # Instantiate the TaskGenerator with the agents
    task_generator = TaskGenerator(ceo_agent, idea_agent, news_agent, tech_trends_agent, customer_feedback_agent, competitive_analysis_agent)

    # Generate a task
    task = task_generator.generate_task()
    print("Generated Task:", task)

if __name__ == "__main__":
    main()
