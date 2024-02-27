import subprocess
from agents.feedback_gen import RefinementFeedbackGenerator



class CodeExecutor:
    def execute_code(self, code, update_callback):
        
        try:
            with open("Scripts/temp_code.py", "w") as file:
                file.write(code)
            #subprocess.run(["pip", "install", imports], capture_output=True, text=True)
            result = subprocess.run(["python", "Scripts/temp_code.py"], capture_output=True, text=True, timeout=15)
            feedback = RefinementFeedbackGenerator().generate_feedback(code+result, update_callback)
            update_callback(f"Feedback: {feedback}")
            if result.returncode == 0:
                update_callback(f"Execution Output: {result.stdout}")
            else:
                update_callback(f"Execution Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            update_callback(f"Code execution timed out.")
            feedback = None
        except Exception as e:
            update_callback(f"An error occurred: {str(e)}")
            feedback = None
        finally:
            return feedback
    def find_pip_installed_packages(self):
        result = subprocess.run(["pip", "list"], capture_output=True, text=True)
        return result.stdout
        