

class CommandRouter:
    """A simple command router to handle commands in a chat application."""
    def __init__(self):
        """Initialize the command router with an empty command registry."""
        # Dictionary to hold command names and their corresponding functions
        # The keys are the command names in lowercase to ensure case-insensitivity
        # The values are the functions that will be executed when the command is called
        # This allows for easy registration and lookup of command handlers
        self.commands = {}

    def register(self, name, func):
        """Register a command with a name and a function to execute"""
        # Convert the command name to lowercase to ensure case-insensitivity
        self.commands[name.lower()] = func

    def handle(self, command:str):
        """Handle a command by executing the corresponding function"""
        # Strip any leading or trailing whitespace and convert to lowercase
        command = command.strip().lower()
        # Check if the command exists in the registry
        if command in self.commands:
            # Execute the corresponding function and return its result
            return self.commands[command]()
        else:
            # If the command is not found, return an error message
            # This could be replaced with a more sophisticated error handling mechanism
            print(f"Unknown command: {command}")