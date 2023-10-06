# base_bot.py

class BaseBot:
    def __init__(self, embedder):
        self.embedder = embedder

    def add_data(self, data_type, data_content):
        """Add data to the system."""
        # Use the embedder to process and add the data
        self.embedder.add(data_type, data_content)

    def query(self, question):
        """Query the system with a specific question."""
        # Use the embedder to process the query and get a response
        response = self.embedder.query(question)
        return response

    def start(self):
        """Start the bot's functionality."""
        raise NotImplementedError("This method should be implemented by subclasses.")
