
import os
# Configuration Module
class Config:
    def __init__(self):
        # Load environment variables using dotenv (you might need to install the python-dotenv package)
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        # self.TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"  # Placeholder for the example
