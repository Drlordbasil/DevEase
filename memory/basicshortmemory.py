class Memory:
    ''' A basic short-term memory class that stores user and system message pairs.
    
    
    
    '''
    def __init__(self, max_size=5000):
        self.max_size = max_size
        self.memory = []

    def add_message_pair(self, user_message, sys_message):
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

        if len(self.memory) > self.max_size:
            self.memory.pop(0)
