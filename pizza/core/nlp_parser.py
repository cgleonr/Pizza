import spacy

class NLPCommandParser:
    def __init__(self, command_map):
        self.command_map = command_map  # dict of keywords -> real commands
        self.nlp = spacy.load("en_core_web_md")

    def parse(self, text):
        """Parse the text and return the corresponding command."""
        doc = self.nlp(text.lower())

        for token in doc:
            if token.lemma_ in self.command_map:
                return self.command_map[token.lemma_]
                
        return None

    def extract_song_query(self, text):
        doc = self.nlp(text)

        # Try to locate the verb 'play'
        for token in doc:
            if token.lemma_ in ["play", "listen to", "hear"]:
                after = text[token.idx + len(token.text):].strip(" ?.")
                if after:
                    return after.lower()

        return None
