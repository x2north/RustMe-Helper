import discord
from discord.ext import commands
import cogs.sulfur_calc as sulf
import cogs.expl_calc as exp
import cogs.raid_calc as raid
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


class MyView(discord.ui.View):
    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Выберите вариант...",
        options=[
            discord.SelectOption(label="Калькулятор взрывчатки", emoji="<:timed_explosive_charge:1276146408130609227>", value="0"),
            discord.SelectOption(label="Калькулятор перекрафта", emoji="<:gunpowder:1280434085604626535>", value="1"),
            discord.SelectOption(label="Калькулятор рейда", emoji="<:double_hqm_door:1286056093050605644>", value="2")
            ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        match select.values[0]:
            case '1':
                await interaction.response.send_message(view=sulf.MyView(), ephemeral=True)
            case '0':
                await interaction.response.send_message(view=exp.MyView(), ephemeral=True)
            case '2':
                 await interaction.response.send_message(view=raid.MyView(), ephemeral=True)

class calc(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
	
    @discord.Cog.listener()
    async def on_ready(self) -> None:
        logger.debug("Cog main_calc loaded")
        
    @discord.slash_command(aliases=["calculate","explosive","exp","calc"], description="Калькулятор взрывчатки")
    async def calc(self, interaction) -> None:
        await interaction.response.send_message(view=MyView(), ephemeral=True)

def setup(bot: discord.Bot) -> None:
    bot.add_cog(calc(bot))
