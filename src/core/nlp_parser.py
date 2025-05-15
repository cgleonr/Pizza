import spacy

class NLPCommandParser:
    def __init__(self, command_map):
        self.command_map = command_map  # dict of keywords -> real commands
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, text):
        doc = self.nlp(text.lower())

        for token in doc:
            if token.lemma_ in self.command_map:
                return self.command_map[token.lemma_]

        return None
