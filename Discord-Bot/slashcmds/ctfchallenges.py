import discord
import settings
import enum
from discord import app_commands
from app.buttons import *

logger = settings.logging.getLogger("bot")

class Choice(enum.Enum):
    caldera = "caldera"
    web = "web"
    forensic = "forensic"

class CTFChallenge(app_commands.Group):
    
    @app_commands.command()
    async def challname(self, interaction: discord.Interaction, choice: Choice):
        view = SimpleView(timeout = 60)

        await interaction.response.send_message(f"{choice.value}", view=view)
        message = await interaction.original_response()

        view.message = message
        
        await view.wait()

        await view.disable_all_items()

        
async def setup(bot):
    bot.tree.add_command(CTFChallenge(name="ctfchallenge", description="Choose a challange from a list of challanges"))
