import discord
from discord.ext import commands
import json
import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',   # Blue
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[95m' # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        formatted_message = f"[{self.formatTime(record)}] | {color}{record.levelname}{self.RESET} | {record.getMessage()}"
        return formatted_message

    def formatTime(self, record, datefmt=None):
        return logging.Formatter.formatTime(self, record, datefmt='%Y-%m-%d %H:%M:%S')


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = ColoredFormatter("[%(asctime)s] | %(levelname)s | %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Recycle(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.slash_command(name="recycle", description="Показать информацию о компонентах и ресурсах после переработки")
    async def recycle_info(self, interaction):
        with open('configs/recycle.json', 'r', encoding='utf-8') as file:
            components_data = json.load(file)
        
        embeds = []
        embed = discord.Embed(title="Информация о переработке", color=discord.Colour.orange(), description="-# RustMe Helper\n\n")
        
        field_count = 0 

        for component in components_data["components"]:
            resources_str = "\n".join(f"- {resource} x{amount}" for resource, amount in component["resources"].items())
            
            if field_count == 25:
                embeds.append(embed)
                embed = discord.Embed(title="Продолжение информации", color=discord.Colour.orange(), description="-# RustMe Helper\n\n")
                field_count = 0 

            embed.add_field(name=component['name'], value=resources_str, inline=True)
            field_count += 1

        embeds.append(embed)
        
        for em in embeds:
            await interaction.response.send_message(embed=em, ephemeral=True)
        logger.info(f"{interaction.user.name} использовал таблицу переработки.")

def setup(bot: discord.Bot) -> None:
    bot.add_cog(Recycle(bot))
