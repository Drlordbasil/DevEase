# competitive_analysis_gen.py

class CompetitiveAnalysisGenerator:
    def __init__(self):
        pass

    def fetch_competitive_analysis(self, api_calls, project_description):
        try:
            system_message = """
            As a competitive analysis expert, your task is to evaluate the described project in the context of the current market and competitive landscape. Your analysis should identify key competitors, highlight competitive advantages and disadvantages, and suggest strategic opportunities for differentiation and leadership.

            Guidelines for analysis:
            - Identify direct and indirect competitors.
            - Assess competitors' strengths and weaknesses.
            - Highlight unique selling points and potential areas for improvement.
            - Recommend strategies for competitive differentiation.
            """
            user_message = f"""
            DevEase is exploring the following project: {project_description}. Please conduct a comprehensive competitive analysis to understand how this project could position DevEase in the market, considering existing competitors and potential market opportunities.

            """
            
            analysis = api_calls(user_message, system_message)
            
            return analysis
        except Exception as e:
            print(f"Error fetching competitive analysis: {str(e)}")
            return ""
