import spacy

class NLPCommandParser:
    def __init__(self, command_map):
        self.command_map = command_map  # dict of keywords -> real commands
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, text):
        """Parse the text and return the corresponding command."""
        doc = self.nlp(text.lower())

        for token in doc:
            if token.lemma_ in self.command_map:
                return self.command_map[token.lemma_]
                
        return None

    def extract_song_query(self, text):
        doc = self.nlp(text)  # ← DON'T lowercase

        # Try longest noun chunk excluding weak pronouns
        noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks if chunk.text.lower() not in ("you", "me")]
        if noun_chunks:
            best_chunk = max(noun_chunks, key=lambda c: len(c.split()))
            if len(best_chunk.split()) > 1:
                return best_chunk.lower()

        # Try named entities (song titles, artists)
        entities = [ent.text.strip() for ent in doc.ents if ent.label_ in ("WORK_OF_ART", "PERSON", "ORG")]
        if entities:
            return max(entities, key=lambda e: len(e.split())).lower()

        return None
