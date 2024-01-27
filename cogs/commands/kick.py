from config import *
from utils import *
from views import *
from bot import Bot
from nextcord import Interaction, User, Member, Permissions, slash_command, user_command
from nextcord.ext.commands import Cog



class KickCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Kick a member", guild_ids=GUILD_IDS, default_member_permissions=Permissions(kick_members=True))
    async def kick(self, interaction: Interaction, target: Member, reason: str = "No reason provided"):
        
        # Check if the target is the interaction's author
        if target.id == interaction.user.id:
            await error(interaction, "You can't kick yourself")
        
        # Check if the interaction's author can kick the target
        elif interaction.user.top_role.position <= target.top_role.position and interaction.user.id != interaction.guild.owner_id:
            await error(interaction, "You can't kick someone with a top role higher or equal to yours")
        
        # Check if the target is kickable
        elif interaction.guild.me.top_role.position <= target.top_role.position or target.id == interaction.guild.owner_id:
            await error(interaction, "I can't kick someone with a top role higher or equal to mine")
        
        else:
            # Create a confirmation view
            view = ConfirmButtons(self.bot, timeout=60)
            
            # Send the confirmation message
            msg = await interaction.send(f"Are you sure you want to kick {target.mention}?", view=view, ephemeral=True)
            
            # Wait for the view to be interacted with
            await view.wait()
            
            # If the iteraction's author confirmed the action, kick the target
            if view.value:
                await target.kick(reason=reason)
                await msg.edit(view=None)
                await success(interaction, f"Successfully kicked {target.mention} for {reason}")
            
            # Else, cancel the action
            else:
                await msg.edit("OK, canceled", view=None)
                
    @user_command(name="Kick", guild_ids=GUILD_IDS, default_member_permissions=Permissions(kick_members=True))
    async def user_kick(self, interaction: Interaction, target: User):
        member = interaction.guild.get_member(target.id)
        if member is None:
            await error(interaction, "This user is not in the server")
        else:
            await self.kick(interaction, member)

def setup(bot: Bot):
    bot.add_cog(KickCommand(bot))