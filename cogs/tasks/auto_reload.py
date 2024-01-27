from config import *
from utils import *
from bot import Bot
from nextcord.ext.commands import Cog
from nextcord.ext import tasks
import os, time

# This cog automatically reloads the cogs when they are modified
# Note: this reloads ONLY the cogs, not views, utils, etc...
# If you want to reload everything, restart the bot
class AutoReload(Cog):
    """This task automatically reloads the cogs when they are modified
    Note: this reloads ONLY the cogs, not views, utils, etc...
    If you want to reload everything, restart the bot
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.last_reload = 0
        
        # Don't start the task if th AUTO_RELOAD variable is set to False
        if AUTO_RELOAD:
            self.auto_reload.start()
    
    @tasks.loop(seconds=1)
    async def auto_reload(self):
        
        # Wait until all the cogs are loaded
        await self.bot.wait_until_ready()
        
        # Initialize the last reload time
        if self.last_reload == 0:
            self.last_reload = time.time()
        
        # Prevents the bot from reloading too often
        if time.time() - self.last_reload < 5:
            return

        # Get all the cogs
        cogs = get_cogs()
        
        # Get the cogs that need to be loaded, unloaded and reloaded
        cogs_to_load = cogs - set(self.bot.loaded_cogs.keys())
        cogs_to_unload = set(self.bot.loaded_cogs.keys()) - cogs
        cogs_to_reload = set()
        for cog in cogs:
            file_path = module_to_file(cog)
            if os.path.getmtime(file_path) != self.bot.loaded_cogs.get(cog) and cog not in cogs_to_load | cogs_to_unload:
                cogs_to_reload.add(cog)
                self.bot.loaded_cogs[file_path] = os.path.getmtime(file_path)
                
        # Load, unload and reload the cogs 
        if cogs_to_load or cogs_to_unload or cogs_to_reload:
            self.last_reload = time.time()
            
            # Build the message to log
            msg = "Changes detected, "
            if cogs_to_load:
                msg += f"loading {len(cogs_to_load)} new cogs, "
            if cogs_to_unload:
                msg += f"unloading {len(cogs_to_unload)} cogs, "
            if cogs_to_reload:
                msg += f"reloading {len(cogs_to_reload)} cogs, "
            msg = msg.removesuffix(", ")
            self.bot.logger.info(msg)
            
            # Try to load all the cogs that need to be loaded
            for cog in cogs_to_load:
                try:
                    self.bot.load_extension(cog)
                    self.bot.logger.debug("Loaded " + cog)
                except Exception as e:
                    self.bot.logger.warning("Failed to load " + cog + ": " + str(e))
            
            # Unload all the cogs that need to be unloaded
            for cog in cogs_to_unload:
                self.bot.unload_extension(cog)
                self.bot.logger.debug("Unloaded " + cog)
            
            # Try to reload all the cogs that need to be reloaded
            for cog in cogs_to_reload:
                try:
                    self.bot.reload_extension(cog)
                    self.bot.logger.debug("Reloaded " + cog)
                except Exception as e:
                    self.bot.logger.warning("Failed to reload " + cog + ": " + str(e))
            
            # Update the last modified time of every cog file
            self.bot.loaded_cogs = {cog: os.path.getmtime(module_to_file(cog)) for cog in cogs}
                
            
    @auto_reload.error
    async def on_error(self, exception: Exception):
        await self.bot.handle_task_error(exception, "auto_reload")



def setup(bot: Bot):
    bot.add_cog(AutoReload(bot))