import discord
import settings
from discord.ext import commands
from discord import app_commands


logger = settings.logging.getLogger("bot")

class SimpleView(discord.ui.View):
    
    # def __init__(self, message):
    #     self.message = message
    
    foo : bool = None
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

            
    async def on_timeout(self) -> None:
        await self.message.channel.send("Timeout")
        await self.disable_all_items()
    
    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def Start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Starting challenge")
        self.foo = True
        self.stop()
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def Stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Stopping challenge")
        self.foo = False
        self.stop()
        
    @discord.ui.button(label="Restart", style=discord.ButtonStyle.blurple)
    async def Restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Restarting challenge")
        self.stop()
    '''
    #To-do:
     *Change grey out all buttons on click to only grey out clicked button.
     *This button should be tracked so that user can't choose the same button twice.
     ** For example: if start clicked, the start should not be clicked twice, which lead to start same process multiple times
    '''
