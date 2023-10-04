# base_bot.py

class BaseBot:
    def __init__(self, embedder):
        self.embedder = embedder

    def add_data(self, data_type, data_content):
        """Add data to the system."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def query(self, question):
        """Query the system with a specific question."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def start(self):
        """Start the bot's functionality."""
        raise NotImplementedError("This method should be implemented by subclasses.")
