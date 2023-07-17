import discord
import settings
# import database
# from models.account import Account
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger(__name__)

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
        #self.foo = True
        self.stop()
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def Stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Stopping challenge")
        #self.foo = False
        self.stop()
        
    @discord.ui.button(label="Restart", style=discord.ButtonStyle.blurple)
    async def Restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Restarting challenge")
        self.stop()
        

def run():
    intents = discord.Intents.all()
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f'Guild ID: {settings.GUILD_ID_TEST}')
        logger.info(f'CHANNEL ID: {settings.CHANNEL_ID}')
        logger.info(f"Bot is ready!")
        
        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)
       
        embed = discord.Embed(
            colour=discord.Colour.dark_teal(),
            title="Welcome to Maouque 1st CTF Challenge",
            description="Use /challenge command to begin",
        )
        embed.set_author(name="Maouque", url = "")
        #Small image on top right
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1078399381226659961/1096251403984437278/greenNek0.jpg")
        #Big image 
        embed.set_image(url="https://cdn.discordapp.com/attachments/1078399381226659961/1101183284681134090/IMG_0202.png")
        
        guild = bot.get_guild(settings.GUILD_ID_TEST)  # Replace YOUR_GUILD_ID with the ID of your server
        if guild is not None:
            channel = guild.get_channel(settings.CHANNEL_ID)  # Replace YOUR_CHANNEL_ID with the ID of the channel you want the bot to send the message to
            if channel is not None:
                await channel.send(embed=embed)
            else:
                print("Channel not found.")
        else:
            print("Guild not found.")
        
                
    @bot.tree.command()
    async def challenge(interaction: discord.Interaction):

        view = SimpleView(timeout = 60)
        
        await interaction.response.send_message(view=view)
        message = await interaction.original_response()
        view.message = message
        await view.wait()
        await view.disable_all_items()

    @bot.tree.command()
    async def aboutme(interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.Colour.dark_teal(),
            title="About Me",
            description="Hi my name is ...",
        )
        embed.set_footer(text="this is the footer")
        embed.set_author(name="Maouque", url = "")
        
        #Small image on top right
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1078399381226659961/1096251403984437278/greenNek0.jpg")
        
        #Big image 
        embed.set_image(url="https://cdn.discordapp.com/attachments/1078399381226659961/1101183284681134090/IMG_0202.png")
        embed.add_field(name="Github", value="https://github.com/vtran0314/")
        
        embed.insert_field_at(1, name = "LinkedIn", value ="https://www.linkedin.com/in/vinh-tran314/")
        
        await interaction.response.send_message(embed=embed)
    
    
      
    bot.run(settings.TOKEN, root_logger=True)
    
if __name__ == "__main__":
    run()
    
    
