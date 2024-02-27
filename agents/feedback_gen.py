from api_calls.openai_api import api_calls

# start feedback history for callback
if 'feedback_history' not in locals():
    feedback_history = []

class RefinementFeedbackGenerator:
    def __init__(self):
        pass

    def generate_feedback(self,code, update_callback):
        try:
            system_message = """
            As an expert in code review and refinement, your task is to generate constructive feedback for the provided Python code. Your feedback should be detailed, pinpointing both strengths and areas for improvement, with a focus on enhancing code quality, efficiency, and readability. Your role is crucial in aiding AI team members to elevate their coding practices. Consider aspects such as code structure, adherence to Python conventions, optimization opportunities, and potential bugs. Aim to foster a collaborative environment that encourages learning and continuous improvement.

            Guidelines for feedback:
            - Highlight specific lines or sections that are well-written or innovative.
            - Suggest concrete improvements for any identified issues.
            - Recommend best practices for Python programming, such as the use of functions, classes, naming conventions, and documentation.
            - Offer resources or examples when possible to illustrate your suggestions.
            """
            user_message = f"""
            I am submitting the following Python code for review and am seeking detailed, constructive feedback to enhance its quality. My goal is to improve the code's efficiency, readability, and adherence to Pythonic principles. Please provide targeted feedback that identifies both the strengths and weaknesses of the code, along with specific suggestions for improvement. Here is the code:

            {code}

            Your feedback should include comments on the code structure, use of Python conventions, optimization opportunities, and any potential bugs or issues. I welcome recommendations on best practices and resources for further learning.
            """
            
            feedback = api_calls(user_message, system_message)
            update_callback(f"Generated Feedback: {feedback}")
            return feedback
        except Exception as e:
            update_callback(f"Error generating feedback: {str(e)}")
            return ""