

def register(router):
    """Register commands with the command router."""
    def say_hello():
        """Say hello to the user."""
        print("Hello from Hello Plugin")

    # Register commands with the router
    router.register("hello", say_hello)