# telegram_bot_plugin.py
from base_bot import BaseBot
import requests

class TelegramBot(BaseBot):
    API_URL = "https://api.telegram.org/bot{}/{}"

    def __init__(self, embedder, config):
        super().__init__(embedder)
        self.config = config
        self.last_update_id = None

    def send_message(self, chat_id, text):
        """Send a response back to the user on Telegram."""
        url = self.API_URL.format(self.config.TELEGRAM_TOKEN, "sendMessage")
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

    def start(self):
        """Specific implementation to start the Telegram bot."""
        while True:
            updates = self.get_updates()
            for update in updates:
                chat_id = update['message']['chat']['id']
                text = update['message']['text']
                response = self.process_message(text)
                self.send_message(chat_id, response)

    def get_updates(self):
        """Get new messages from Telegram."""
        url = self.API_URL.format(self.config.TELEGRAM_TOKEN, "getUpdates")
        params = {'timeout': 100, 'offset': self.last_update_id}
        response = requests.get(url, params=params).json()
        if response.get('result'):
            self.last_update_id = response['result'][-1]['update_id'] + 1
        return response.get('result', [])

if __name__ == "__main__":
    from nchain.config.config_module import Config
    from nchain.embedders.sentence_transformers_embedder import SentenceTransformersEmbedder as Embedder 
    config = Config()
    embedder = Embedder()
    telegram_bot = TelegramBot(embedder, config)
    
    telegram_bot.start()