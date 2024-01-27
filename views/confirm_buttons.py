from config import *
from bot import Bot
from nextcord import Interaction, ButtonStyle
from nextcord.ui import View, Item, Button, button


class ConfirmButtons(View):
    def __init__(self, bot: Bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.value = None
        
        
    async def on_error(self, exception: Exception, item: Item, interaction: Interaction):
        await self.bot.handle_interaction_error(interaction, exception)


    @button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, button: Button, interaction: Interaction):
        self.value = False
        self.stop()

    @button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button: Button, interaction: Interaction):
        self.value = True
        self.stop()


