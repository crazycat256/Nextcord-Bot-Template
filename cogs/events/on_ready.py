from config import *
from utils import *
from bot import Bot
from nextcord import Activity, ActivityType
from nextcord.ext.commands import Cog
from nextcord.ext import commands
import os

class OnReady(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
    
        # Fetch the owner(s) of the bot
        if not (self.bot.owner_id or self.bot.owner_ids):
            app = await self.bot.application_info()
            if app.team:
                self.bot.owner_ids = {m.id for m in app.team.members}
            else:
                self.bot.owner_id = app.owner.id

        # Initialise the bot
        if not self.bot.initialised:
            self.bot.initialised = True
            
            # Get the last modified time of every cog file
            self.bot.loaded_cogs = {cog: os.path.getmtime(module_to_file(cog)) for cog in get_cogs()}

        # Set the bot's status
        await self.bot.change_presence(activity=Activity(type=ActivityType.playing, name="something..."))
        
        self.bot.logger.info("We have logged in as", self.bot.user)




def setup(bot: Bot):
    bot.add_cog(OnReady(bot))
