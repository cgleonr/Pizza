from core.command_router import CommandRouter


def test_command_registration_and_handling(capsys):
    """Test command registration and handling in CommandRouter."""
    router = CommandRouter()

    def test_func():
        print("Test function executed")

    router.register("test", test_func)
    router.handle("test")

    captured = capsys.readouterr()
    assert "Test function executed" in captured.out