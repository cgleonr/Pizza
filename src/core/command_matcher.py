import difflib

class CommandMatcher:
    """
    A class to match commands with their respective handlers.
    Uses Python's built-in difflib.get_close_matches for fuzzy matching.
    This class is designed to be used with a list of command names.
    """
    def __init__(self, command_names, aliases=None):
        """
        Initializes the CommandMatcher with a list of command names.
        """
        self.command_names = command_names
        self.aliases = aliases


    def match(self, input_text):
        """
        Matches the input text with the command names.
        Returns the matched command name or None if no match is found.
        """
        input_lower = input_text.lower().strip()

        # 1. Exact alias match
        if input_lower in self.aliases:
            return self.aliases[input_lower]
        
        # 2. Substring match against command names
        for cmd in self.command_names:
            if cmd.lower() in input_lower:
                return cmd
        
        # 3. Fuzzy match
        close = difflib.get_close_matches(input_lower, self.command_names, n=1, cutoff=0.6)
        if close:
            return close[0]
        
        # 4. No match found
        return None