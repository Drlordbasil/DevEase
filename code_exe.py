
import subprocess


class CodeExecutor:
    """
    A class that executes code, finds installed packages, reads scripts, and checks directory contents.
    """

    def execute_code(self,code):
        """
        Executes the given code and provides feedback.

        Args:
            code (str): The code to be executed.
            update_callback (function): A callback function to update the feedback.

        Returns:
            str: The feedback generated during code execution.
        """
        try:
            with open("Scripts/temp_code.py", "w") as file:
                file.write(code)
            #subprocess.run(["pip", "install", imports], capture_output=True, text=True)
            result = subprocess.run(["python", "Scripts/temp_code.py"], capture_output=True, text=True, timeout=15)
            code_output = result.stdout
            return code_output
        except subprocess.TimeoutExpired:
            return "The code took too long to execute."
        except Exception as e:
            return str(e)

    def find_pip_installed_packages(self):
        """
        Finds the list of installed packages using pip.

        Returns:
            str: The list of installed packages.
        """
        result = subprocess.run(["pip", "list"], capture_output=True, text=True)
        return result.stdout

    def read_current_scripts(self, filename):
        """
        Reads the content of a script file.

        Args:
            filename (str): The name of the script file.

        Returns:
            str: The content of the script file.
        """
        with open(filename, "r") as file:
            return file.read()

    def check_directory_contents(self):
        """
        Checks the contents of the current directory.

        Returns:
            str: The list of directory contents.
        """
        result = subprocess.run(["ls"], capture_output=True, text=True)
        return result.stdout

    