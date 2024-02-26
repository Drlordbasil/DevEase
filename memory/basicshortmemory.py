import json

import json

class BasicShortMemory:
    """
    A class representing a basic short-term memory.

    Attributes:
        memory (list): A list to store user and system messages.

    Methods:
        add_to_memory(user_message, sys_message): Adds a user and system message pair to the memory.
        search_memory(user_message, sys_message): Searches the memory for a matching user or system message.
        get_memory(): Returns the current memory.
        clear_memory(): Clears the memory.
        save_memory(filename): Saves the memory to a file.
        load_memory(filename): Loads the memory from a file.
    """

    def __init__(self):
        self.memory = []

    def add_to_memory(self, user_message, sys_message):
        """
        Adds a user and system message pair to the memory.

        Args:
            user_message (str): The user message to be added.
            sys_message (str): The system message to be added.

        Raises:
            ValueError: If user_message or sys_message is not a string.
        """
        if not isinstance(user_message, str) or not isinstance(sys_message, str):
            raise ValueError("user_message and sys_message must be strings")

        self.memory.append({"user": user_message, "system": sys_message})

    def search_memory(self, user_message, sys_message):
        """
        Searches the memory for a matching user or system message.

        Args:
            user_message (str): The user message to search for.
            sys_message (str): The system message to search for.

        Returns:
            str or None: The matching system message if found, or the matching user message if found,
            or None if no match is found.

        Raises:
            ValueError: If user_message or sys_message is not a string.
        """
        if not isinstance(user_message, str) or not isinstance(sys_message, str):
            raise ValueError("user_message and sys_message must be strings")

        for i in range(len(self.memory) - 1, -1, -1):
            if self.memory[i]["user"] == user_message:
                return self.memory[i]["system"]
        for i in range(len(self.memory) - 1, -1, -1):
            if self.memory[i]["system"] == sys_message:
                return self.memory[i]["user"]
        return None

    def get_memory(self):
        """
        Returns the current memory.

        Returns:
            list: The current memory.
        """
        return self.memory

    def clear_memory(self):
        """
        Clears the memory.
        """
        self.memory = []

    def save_memory(self, filename):
        """
        Saves the memory to a file.

        Args:
            filename (str): The name of the file to save the memory to.

        Raises:
            ValueError: If filename is not a string.
        """
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")

        with open(filename, "w") as file:
            json.dump(self.memory, file)

    def load_memory(self, filename):
        """
        Loads the memory from a file.

        Args:
            filename (str): The name of the file to load the memory from.

        Raises:
            ValueError: If filename is not a string.
        """
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")

        try:
            with open(filename, "r") as file:
                self.memory = json.load(file)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{filename}'.")
