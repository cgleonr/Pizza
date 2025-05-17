
import spacy

def ensure_spacy_model():
    """Ensure spaCy model is loaded, else download"""
    try:
        spacy.load("en_core_web_sm")
        print("✅ spaCy model already installed.")
    except OSError:
        print("⚠️ spaCy model not found. Installing...")
        from spacy.cli import download
        download("en_core_web_sm")

if __name__ == "__main__":
    ensure_spacy_model()
