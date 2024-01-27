from config import *
from bot import Bot
from nextcord import Interaction, PartialInteractionMessage, Message, Embed, ButtonStyle
from nextcord.ui import View, Item, Button, button


class PageButtons(View):
    def __init__(self, bot: Bot, embeds: list[Embed]):
        super().__init__(timeout=None)
        self.bot = bot
        self.embeds = embeds
        
        self.value = 0
        self.children: list[Button]
        self.first, self.backward, self.page, self.forward, self.last = self.children
        self.page.label = f"{self.value + 1}/{len(self.embeds)}"
        
    async def on_error(self, exception: Exception, item: Item, interaction: Interaction):
        await self.bot.handle_interaction_error(interaction, exception)


    @button(label = "<<", style=ButtonStyle.blurple, disabled=True)
    async def first_button(self, button: Button, interaction: Interaction):
        self.value = 0
        await self.update(interaction)

    @button(label = "<", style=ButtonStyle.blurple, disabled=True)
    async def backward_button(self, button: Button, interaction: Interaction):
        if self.value >= 1:
            self.value -= 1
        else:
            self.value = 0
        await self.update(interaction)
        
    @button(label="1/X", style=ButtonStyle.grey, disabled=True)
    async def page_button(self, button: Button, interaction: Interaction):
        pass

    @button(label = ">", style=ButtonStyle.blurple)
    async def forward_button(self, button: Button, interaction: Interaction):
        if self.value <= len(self.embeds) - 1:
            self.value += 1
        await self.update(interaction)
        
    @button(label = ">>", style=ButtonStyle.blurple)
    async def last_button(self, button: Button, interaction: Interaction):
        self.value = len(self.embeds) - 1
        await self.update(interaction)


    async def update(self, interaction: Interaction):
                
        self.page.label = f"{self.value + 1}/{len(self.embeds)}"
        
        if self.value <= 0:
            self.disable(self.first, self.backward)
        else:
            self.enable(self.first, self.backward)
            
        if self.value >= len(self.embeds) - 1:
            self.disable(self.last, self.forward)
        else:
            self.enable(self.last, self.forward)
            
        await interaction.response.edit_message(embed=self.embeds[self.value], view=self)
            
        
    
    def disable(self, *buttons: Button):
        for b in buttons:
            b.disabled = True
        
    def enable(self, *buttons: Button):
        for b in buttons:
            b.disabled = False


