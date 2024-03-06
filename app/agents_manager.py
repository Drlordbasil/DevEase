from agents.adaptive_scripter import AdaptiveScripter
from agents.code_creation import CodeCreator
from agents.code_refinement import CodeRefiner
from agents.feedback_gen import RefinementFeedbackGenerator
from code_exe import CodeExecutor
from agents.idea_generator import IdeaGenerator
from agents.file_manager import FileManager
from agents.CEO_persona import CEO
from app.collab_manager import CollaborationManager

class AgentManager:
    def __init__(self):
        self.setup_agents()
        self.setup_collaboration_manager()

    def setup_agents(self):
        self.file_manager = FileManager()
        self.idea_generator = IdeaGenerator()
        self.code_creator = CodeCreator()
        self.code_executor = CodeExecutor()
        self.code_refiner = CodeRefiner()
        self.adaptive_scripter = AdaptiveScripter()
        self.feedback_generator = RefinementFeedbackGenerator()
        self.CEO = CEO()

    def setup_collaboration_manager(self):
        self.agents = {
            "FileManager": self.file_manager,
            "IdeaGenerator": self.idea_generator,
            "CodeCreator": self.code_creator,
            "CodeExecutor": self.code_executor,
            "CodeRefiner": self.code_refiner,
            "AdaptiveScripter": self.adaptive_scripter,
            "FeedbackGenerator": self.feedback_generator,
            "CEO": self.CEO
        }
        self.collaboration_manager = CollaborationManager(self.agents)

    def get_collaboration_manager(self):
        return self.collaboration_manager

    def generate_idea(self):
        return self.collaboration_manager.generate_idea()

    def get_ceo_feedback(self, agent_name, idea_or_code, additional_info):
        return self.CEO.review_employee(agent_name, idea_or_code, additional_info)

    def get_ceo_task(self, message):
        return self.CEO.get_task(message)

    def is_code_ready(self, code):
        return self.CEO.is_code_ready(code)

    def analyze_code(self, code):
        return self.collaboration_manager.analyze_code(code)

    def refine_code(self, code, feedback):
        return self.collaboration_manager.refine_code(code, feedback)

    def save_code(self, code):
        return self.collaboration_manager.save_code(code)