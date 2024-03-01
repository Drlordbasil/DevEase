# customer_feedback_gen.py

class CustomerFeedbackGenerator:
    def __init__(self):
        pass

    def fetch_customer_feedback(self, api_calls, feature_description):
        try:
            system_message = """
            As a customer feedback specialist, your role is to generate realistic and constructive feedback for the described software feature. Consider aspects such as usability, functionality, innovation, and how the feature meets user needs. Your feedback should provide actionable insights for improvement and enhancement, focusing on increasing customer satisfaction and engagement.

            Guidelines for feedback:
            - Evaluate the feature's user interface and experience.
            - Consider the feature's usefulness and practicality.
            - Suggest improvements for better alignment with user expectations.
            - Assess the feature's innovation and how it stands out from competitors.
            """
            user_message = f"""
            The following feature is being developed by DevEase: {feature_description}. Based on an initial review, please provide detailed customer feedback that highlights the feature's strengths and areas for improvement. The goal is to enhance the feature's appeal to users and ensure it effectively addresses their needs.

            """
            
            feedback = api_calls(user_message, system_message)
            
            return feedback
        except Exception as e:
            print(f"Error fetching customer feedback: {str(e)}")
            return ""
