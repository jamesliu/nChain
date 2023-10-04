from nanochain.bots.base_bot import BaseBot

def test_base_bot_methods():
    bot = BaseBot(None)
    
    # Test that base methods raise NotImplementedError
    try:
        bot.add_data(None, None)
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass
    
    try:
        bot.query(None)
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass
    
    try:
        bot.start()
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass

# Additional tests can be added for other functionalities
