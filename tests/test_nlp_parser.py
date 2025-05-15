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

def test_nlp_parser_extract_song_query():
    command_map = {
        "play": "spotify_play",
        "pause": "spotify_pause",
        "song": "spotify_play_song"
    }

    parser = NLPCommandParser(command_map)

    assert parser.extract_song_query("Play Bohemian Rhapsody") == "bohemian rhapsody"
    assert parser.extract_song_query("Can you play Shape of You?") == "shape of you"
    assert parser.extract_song_query("I'd like to hear some jazz") == "some jazz"
    assert parser.extract_song_query("Play something") == "something"
    assert parser.extract_song_query("Just play") is None