from agents.web_research_agent import WebResearch

class CollaborationManager:
    def __init__(self, agents):
        self.agents = agents
    
    def generate_idea(self):
        web_research_query = "AI-based project ideas for Python developers that automate profit generation using AI technologies."
        web_research_results = self.perform_web_research(web_research_query)
        idea = self.agents["IdeaGenerator"].generate_idea(web_research_results)
        return idea
    
    def get_ceo_feedback(self, agent_name, idea, code):
        return self.agents["CEO"].review_employee(agent_name, idea, code)
    
    def get_true_false(self, code):
        return self.agents["CEO"].is_code_ready(code)
    
    def generate_feedback(self, code):
        return self.agents["FeedbackGenerator"].generate_feedback(code)
    
    def analyze_code(self, code):
        return self.agents["CodeExecutor"].analyze_code(code)
    
    def refine_code(self, code, feedback):
        return self.agents["CodeRefiner"].refine_code(code, feedback)

    def perform_web_research(self, query):
        web_research = WebResearch()
        web_research.search_google(query)
        results = web_research.get_google_results()
        web_research.close()
        return results

    def generate_script(self, task, code, idea, ceo_feedback):
        return self.agents["AdaptiveScripter"].create_script(task, code, idea, ceo_feedback)

    def run_script(self, script):
        return self.agents["AdaptiveScripter"].run_script(script, self.agents["CodeExecutor"].current_code_output)

    def save_code(self, code):
        return self.agents["FileManager"].save_mod_file(code)