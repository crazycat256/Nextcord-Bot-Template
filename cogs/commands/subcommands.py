from config import *
from utils import *
from bot import Bot
from nextcord import Interaction, slash_command
from nextcord.ext.commands import Cog

class SubCommandsCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="command", description="A command", guild_ids=GUILD_IDS)
    async def command(self, interaction: Interaction):
        pass # Will never be called because it has subcommands
    
    
    @command.subcommand(name="subcommand1", description="The first subcommand")
    async def subcommand1(self, interaction: Interaction):
        await success(interaction, "Hello from subcommand1")
    
    @command.subcommand(name="subcommand2", description="The second subcommand")
    async def subcommand2(self, interaction: Interaction):
        pass # Will never be called because it has a subcommand
    
    @subcommand2.subcommand(name="subsubcommand1", description="The first sub-subcommand")
    async def subsubcommand1(self, interaction: Interaction):
        await success(interaction, "Hello from sub-subcommand1")
        
    @subcommand2.subcommand(name="subsubcommand2", description="The second sub-subcommand")
    async def subsubcommand2(self, interaction: Interaction):
        await success(interaction, "Hello from sub-subcommand2")

    
    

def setup(bot: Bot):
    bot.add_cog(SubCommandsCommand(bot))