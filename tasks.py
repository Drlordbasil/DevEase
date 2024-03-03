import os
import asyncio
import subprocess
import json
from api_calls.openai_api import OpenAIAPI

class VirtualTeamProject:
    def __init__(self, config_path='./config.json', workspace_dir='./workspace'):
        self.api = OpenAIAPI()
        self.config_path = config_path
        self.workspace_dir = workspace_dir
        self.tasks_config = self.load_tasks_config()

    async def async_init(self):
        self.project_name = await self.generate_dynamic_name("project")
        self.project_path = os.path.join(self.workspace_dir, self.sanitize_name(self.project_name))
        await self.create_directory(self.workspace_dir)
        await self.create_directory(self.project_path)
        print(f"Project '{self.project_name}' initialized within workspace at '{self.project_path}'.")
        self.initialize_git_repository()

    def load_tasks_config(self):
        with open(self.config_path, 'r') as file:
            return json.load(file)

    async def generate_dynamic_name(self, entity_type):
        prompt = self.tasks_config.get(entity_type, {}).get('prompt', "Generate a concise, unique name.")
        loop = asyncio.get_event_loop()
        dynamic_name = await loop.run_in_executor(None, self.api.api_calls, prompt, prompt)
        return self.sanitize_name(dynamic_name.strip()) or f"Dynamic{entity_type.capitalize()}"
    async def perform_and_save_task(self, task_name, extension):
        task_config = self.tasks_config.get(task_name, {})
        # Enhanced prompting mechanism for more actionable outputs
        prompt = f"Generate {extension} code to {task_config.get('description', 'achieve the task')}. Focus on: {task_config.get('prompt')}"
        loop = asyncio.get_event_loop()
        output = await loop.run_in_executor(None, self.api.api_calls, prompt, prompt)
        filename = self.sanitize_name(await self.generate_dynamic_name(task_name))
        filepath = os.path.join(self.project_path, f"{filename}.{extension}")
        await self.save_output(filepath, output)
        print(f"'{task_name}' task completed and saved as '{filepath}'.")


    def sanitize_name(self, name):
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '')
        return name[:40].strip()

    async def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def initialize_git_repository(self):
        subprocess.run(["git", "init"], cwd=self.project_path)
        subprocess.run(["git", "add", "."], cwd=self.project_path)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.project_path)

    async def run_project_workflow(self):
        for task in self.tasks_config['tasks']:
            await self.perform_and_save_task(task['name'], task['extension'])
            self.commit_task(task['name'])

    async def save_output(self, filepath, output):
        with open(filepath, 'w') as file:
            file.write(output)

    def commit_task(self, task_name):
        subprocess.run(["git", "add", "."], cwd=self.project_path)
        subprocess.run(["git", "commit", "-m", f"Complete {task_name}"], cwd=self.project_path)

async def main():
    config_path = './config.json'
    workspace_dir = './workspace'
    virtual_team = VirtualTeamProject(config_path=config_path, workspace_dir=workspace_dir)
    await virtual_team.async_init()
    await virtual_team.run_project_workflow()

if __name__ == "__main__":
    asyncio.run(main())
