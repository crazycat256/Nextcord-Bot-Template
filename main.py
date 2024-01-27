from config import *
from utils import *
from bot import Bot
import nextcord
from dotenv import load_dotenv
import os, logging




def main():
    
    # Create the bot
    bot = Bot(intents=nextcord.Intents.all())
    
    # Load the environment variables
    load_dotenv()
    
    # Get the token from the environment variables
    token = os.getenv("TOKEN")
    if not token:
        bot.logger.critical("No token found in the environment variables, please ensure that you have a .env file in the root directory of the project with a TOKEN variable")
        exit(1)
    
    # Create the logs folder if it doesn't exist
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # Create the nextcord debug logger
    nextcord_logger = Logger("nextcord", "logs/nextcord.log", level=logging.DEBUG, print_level=100)

    # Try to load all the cogs
    for cog in get_cogs():
        try:
            bot.load_extension(cog)
            bot.logger.debug("Loaded " + cog)
        except Exception as e:
            bot.logger.warning("Failed to load " + cog + ": " + str(e))
    
    try:
        bot.run(token)
    except nextcord.LoginFailure:
        bot.logger.critical("Invalid token, please ensure that the token in the .env file is valid")
        exit(1)
    

if __name__ == "__main__":
    main()

