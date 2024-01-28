from config import *
from bot import Bot
from nextcord import Interaction, Embed, ButtonStyle, TextInputStyle
from nextcord.ui import View, Item, Button, Modal, TextInput, button


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
        
    @button(label="1/X", style=ButtonStyle.grey)
    async def page_button(self, button: Button, interaction: Interaction):
        modal = JumpToPageModal(self, len(self.embeds))
        await interaction.response.send_modal(modal)
        await modal.wait()
        

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



class JumpToPageModal(Modal):
    
    def __init__(self, page_buttons: PageButtons, max_value: int):
        super().__init__("Jump to page", timeout=60)
        self.page_buttons = page_buttons
        self.max_value = max_value
        
        self.field = TextInput(
            label="Page number",
            style=TextInputStyle.short,
            placeholder="Enter a number between 1 and " + str(max_value),
            required=True,
            min_length=1,
            max_length=len(str(max_value)),
        )
        self.add_item(self.field)
        
    async def on_error(self, exception: Exception, interaction: Interaction):
        await self.page_buttons.bot.handle_interaction_error(interaction, exception)
        
    async def callback(self, interaction: Interaction):
        
        if self.field.value.isdigit():
            
            value = int(self.field.value) - 1
            if value >= 0 and value < self.max_value:
                
                self.stop()
                self.page_buttons.value = value
                await self.page_buttons.update(interaction)
            
    
    