import difflib

class CommandMatcher:
    """
    A class to match commands with their respective handlers.
    Uses Python's built-in difflib.get_close_matches for fuzzy matching.
    This class is designed to be used with a list of command names.
    """
    def __init__(self, command_names):
        """
        Initializes the CommandMatcher with a list of command names.
        """
        self.command_names = command_names

    def match(self, input_text):
        """
        Matches the input text with the command names.
        Returns the matched command name or None if no match is found.
        """
        input_text = input_text.lower().strip()

        for command in self.command_names:
            if command in input_text:
                return command
        
        # Fuzzy match as fallback
        close = difflib.get_close_matches(input_text, self.command_names, n=1, cutoff=0.6)
        if close:
            return close[0]
        
        return None