from config import *
from bot import Bot
from nextcord import Interaction, ApplicationInvokeError
from nextcord.ext.commands import Cog


class OnAplicationCommandError(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @Cog.listener("on_application_command_error")
    async def on_application_command_error(self, interaction: Interaction, exception: ApplicationInvokeError):
        await self.bot.handle_interaction_error(interaction, exception.original)
             

            

def setup(bot: Bot):
    bot.add_cog(OnAplicationCommandError(bot))