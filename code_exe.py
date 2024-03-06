import subprocess
import logging
import os
from radon.complexity import cc_visit
from radon.metrics import mi_visit, mi_rank
from flake8.api import legacy as flake8

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeExecutor:
    def __init__(self, workspace="workspace"):
        self.workspace = workspace
        self.code = ""
        os.makedirs(self.workspace, exist_ok=True)  # Ensure workspace directory exists

    def execute_python_code(self, code):
        """
        Executes Python code and returns output. This is a placeholder for execution logic.
        """
        # Execution logic here...
        return "Execution results..."

    def analyze_code(self, code):
        """
        Analyzes Python code for complexity, maintainability, and style guide adherence.
        """
        try:
            # Complexity analysis
            complexity = cc_visit(code)
            maintainability_index = mi_visit(code, True)
            rank = mi_rank(maintainability_index)

            # Linting
            flake8_style_guide = flake8.get_style_guide(ignore=['E501'])
            report = flake8_style_guide.check_files([code])

            analysis_results = {
                'complexity': complexity,
                'maintainability_index': maintainability_index,
                'maintainability_rank': rank,
                'linting_errors': report.get_statistics('E'),
                'linting_warnings': report.get_statistics('W'),
            }
            return analysis_results
        except Exception as e:
            logging.error(f"Code analysis error: {e}")
            return f"An error occurred during code analysis:\n{str(e)}"

    def read_file(self, file_path):
        """
        Reads a file from the workspace directory.
        """
        full_path = os.path.join(self.workspace, file_path)
        try:
            with open(full_path, "r") as file:
                self.code = file.read()
            return self.code
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def write_file(self, file_path, code):
        """
        Writes a file to the workspace directory.
        """
        full_path = os.path.join(self.workspace, file_path)
        try:
            with open(full_path, "w") as file:
                file.write(code)
            return f"File written successfully: {full_path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def extract_marked_down_python_code(self, markdown):
        """
        Extracts Python code blocks from Markdown text.
        """
        try:
            self.code = markdown.split("```python")[1].split("```")[0].strip()
            return self.code
        except IndexError as e:
            logging.error("Python code block not found in Markdown")
            return "Python code block not found in Markdown."
    def current_code_output(self, code):
        try:
            result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=15)
            return result.stdout
        except Exception as e:
            return f"Error running script: {str(e)}"
        
