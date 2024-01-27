from config import *
from views import *
from bot import Bot
from nextcord import Interaction, Embed, slash_command
from nextcord.ext.commands import Cog



class PagesCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Test command for PageButtons", guild_ids=GUILD_IDS)
    async def pages(self, interaction: Interaction):
        
        # Create a list of embeds
        embeds = [
            Embed(title="Page 1", description="This is the first page"),
            Embed(title="Page 2", description="This is the second page"),
            Embed(title="Page 3", description="This is the third page"),
            Embed(title="Page 4", description="This is the fourth page"),
            Embed(title="Page 5", description="This is the fifth page"),
            Embed(title="Page 6", description="This is the sixth page"),
            Embed(title="Page 7", description="This is the seventh page"),
            Embed(title="Page 8", description="This is the eighth page"),
            Embed(title="Page 9", description="This is the ninth page"),
            Embed(title="Page 10", description="This is the tenth page"),
        ]
        
        # Initialize the view
        view = PageButtons(self.bot, embeds)
        
        # Send a message with the first embed and attach the view
        await interaction.send(embed=embeds[0], view=view, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(PagesCommand(bot))