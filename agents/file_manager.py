# agents/file_manager.py
from api_calls.openai_api import OpenAIAPI
import os
import shutil

class FileManager:
    def __init__(self, project_dir=None):
        self.project_dir = project_dir or os.path.join(os.getcwd(), "workspace")
        self.openai_api = OpenAIAPI()

    def create_project_directory(self, project_name=None):
        if not project_name:
            project_name = self.name_project_directory()
        project_path = os.path.join(self.project_dir, project_name)
        os.makedirs(project_path, exist_ok=True)
        self.project_dir = project_path
        return project_name

    def name_project_directory(self):
        prompt = """
        You are an AI assistant tasked with generating a name for a new project directory.
        
        Here are the guidelines for generating the project directory name:
        1. Create a concise and descriptive name that reflects the purpose of the project.
        2. Use snake_case naming convention for the directory name.
        3. Avoid using spaces or special characters in the directory name.
        4. Respond with only the directory name, without any additional text or explanations.
        
        Generate a name for the new project directory, following the provided guidelines.
        """

        name = self.openai_api.api_calls(prompt, "You are an AI assistant that generates concise and descriptive names for new project directories.")
        return name.strip()

    def read_project_structure(self, project_path=None):
        if not project_path:
            project_path = self.project_dir

        structure = []
        for root, dirs, files in os.walk(project_path):
            level = root.replace(project_path, "").count(os.sep)
            indent = " " * 4 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 4 * (level + 1)
            for file in files:
                structure.append(f"{subindent}{file}")
        return "\n".join(structure)

    def create_project_directory(self, project_name):
        project_path = os.path.join(self.project_dir, project_name)
        os.makedirs(project_path, exist_ok=True)
        self.project_dir = project_path

    def open_file(self, file_name):
        file_path = os.path.join(self.project_dir, file_name)
        try:
            with open(file_path, "r") as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

    def create_file(self, file_name, content=""):
        file_path = os.path.join(self.project_dir, file_name)
        with open(file_path, "w") as file:
            file.write(content)

    def read_file(self, file_name):
        file_path = os.path.join(self.project_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read()
            return content
        else:
            return None

    def update_file(self, file_name, content):
        file_path = os.path.join(self.project_dir, file_name)
        with open(file_path, "w") as file:
            file.write(content)

    def delete_file(self, file_name):
        file_path = os.path.join(self.project_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    def list_files(self):
        return os.listdir(self.project_dir)

    def get_project_structure(self):
        structure = []
        for root, dirs, files in os.walk(self.project_dir):
            level = root.replace(self.project_dir, "").count(os.sep)
            indent = " " * 4 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 4 * (level + 1)
            for file in files:
                structure.append(f"{subindent}{file}")
        return "\n".join(structure)

    def name_file(self, code):
        prompt = f"""
        You are an AI assistant tasked with generating file names based on the provided code snippets.
        
        Here are the guidelines for generating file names:
        1. Analyze the code snippet to determine its purpose or functionality.
        2. Create a concise and descriptive file name that reflects the code's purpose.
        3. Use snake_case naming convention for the file name.
        4. Determine the appropriate file extension based on the programming language or type of code.
        - For Python code, use the ".py" extension.
        - For HTML code, use the ".html" extension.
        - For CSS code, use the ".css" extension.
        - For JavaScript code, use the ".js" extension.
        - For other types of code, use the appropriate extension.
        5. Respond with only the file name and extension, without any additional text or explanations.
        
        Code snippet:
        ```
        {code}
        ```
        
        Generate a file name with extension for the above code snippet, following the provided guidelines.
        Your response should be in the format: <filename>.<extension>
        """

        name = self.openai_api.api_calls(prompt, "You are an AI assistant that generates concise and descriptive file names with appropriate extensions based on the provided code snippets.")
        return name.strip()

    def save_mod_file(self, content, file_name=None):
        if not file_name:
            file_name = self.name_file(content)
        file_path = os.path.join(self.project_dir, file_name)
        try:
            with open(file_path, "w") as f:
                f.write(content)
            return file_name
        except Exception as e:
            return f"An error occurred while saving the file: {e}"

    def rename_file(self, old_file_name, new_file_name):
        old_file_path = os.path.join(self.project_dir, old_file_name)
        new_file_path = os.path.join(self.project_dir, new_file_name)
        if os.path.isfile(old_file_path):
            os.rename(old_file_path, new_file_path)

    def copy_file(self, source_file_name, destination_file_name):
        source_file_path = os.path.join(self.project_dir, source_file_name)
        destination_file_path = os.path.join(self.project_dir, destination_file_name)
        if os.path.isfile(source_file_path):
            shutil.copyfile(source_file_path, destination_file_path)

    def move_file(self, source_file_name, destination_file_name):
        source_file_path = os.path.join(self.project_dir, source_file_name)
        destination_file_path = os.path.join(self.project_dir, destination_file_name)
        if os.path.isfile(source_file_path):
            shutil.move(source_file_path, destination_file_path)