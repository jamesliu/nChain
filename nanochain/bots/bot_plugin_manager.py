# bot_plugin_manager.py

class BotPluginManager:
    def __init__(self):
        self.bot_plugins = {}

    def register_bot(self, platform_name, bot_class):
        """Register a new bot plugin."""
        if platform_name in self.bot_plugins:
            raise ValueError(f"Bot for platform {platform_name} already registered.")
        self.bot_plugins[platform_name] = bot_class

    def get_bot(self, platform_name):
        """Get a specific bot by platform name."""
        return self.bot_plugins.get(platform_name, None)
