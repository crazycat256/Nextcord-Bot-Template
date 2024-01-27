from config import *
from utils import *
from bot import Bot
from nextcord import Interaction, SlashApplicationCommand, SlashApplicationSubcommand, UserApplicationCommand, MessageApplicationCommand
from nextcord.ext.commands import Cog
import logging


class CommandsLogger(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = Logger("commands", "logs/commands.log", print_level=logging.ERROR)

    @Cog.listener("on_application_command_completion")
    async def on_application_command_completion(self, interaction: Interaction):
        
        if isinstance(interaction.application_command, (SlashApplicationCommand, SlashApplicationSubcommand)):
            command = "/" + get_command(interaction.data)
            self.logger.info(f"{interaction.user} ({interaction.user.id}) : \"{command.strip()}\"")
            
        elif isinstance(interaction.application_command, UserApplicationCommand):
            command = f"{interaction.application_command.name} target_id:{interaction.data['target_id']}"
            self.logger.info(f"{interaction.user} ({interaction.user.id}) : \"{command.strip()}\"")
            
        elif isinstance(interaction.application_command, MessageApplicationCommand):
            resolved = list(interaction.data["resolved"]["messages"].values())[0]
            command = f"{interaction.application_command.name} author_id:{resolved['author']['id']} channel_id:{resolved['channel_id']} message_id_id:{interaction.data['target_id']}"
            self.logger.info(f"{interaction.user} ({interaction.user.id}) : \"{command.strip()}\"")
        
        else:
            await self.bot.logger.error("Unknown application command type: ", type(interaction.application_command))


def setup(bot: Bot):
    bot.add_cog(CommandsLogger(bot))