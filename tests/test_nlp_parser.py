from core.nlp_parser import NLPCommandParser

def test_nlp_parser_matches_lemmas():
    command_map = {
        "greet": "hello",
        "introduce": "hello",
        "say": "hello",
        "exit": "exit"
    }

    parser = NLPCommandParser(command_map)

    assert parser.parse("Can you greet me?") == "hello"
    assert parser.parse("Introduce yourself") == "hello"
    assert parser.parse("Say hello please") == "hello"
    assert parser.parse("Exit the program") == "exit"
    assert parser.parse("Shut down") is None  # No match expected
