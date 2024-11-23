import discord
from discord.ext import commands
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

class help(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
    
    @discord.Cog.listener()
    async def on_ready(self) -> None:
        logger.debug("Cog help loaded")
    
    
    @discord.slash_command(description="Покажет страницу помощи.")
    async def help(self, interaction) -> None:
        if interaction.user.guild_permissions.administrator:
            embed = discord.Embed(title="Помощь", color=discord.Colour.red())
            embed.add_field(name="Команды для участника", value="`/help` | Покажет эту страницу\n`/browse` | Откроет меню поиска РП\n`/offer` | Подать свой рп на рассмотрение\n`/calc` | Калькулятор взрывчатки\n`/scheme` | Схемы электричества\n`/tea` | Информация о чаях\n`/wipes` | Таблица вайпов\n`/recycle` | Таблица переработки компонентов\n`/find_team` | Поиск команды",inline=False)
            embed.add_field(name="Команды для администратора", value="`/browsemessage` | Отправит в выбраный канал статичное сообщение открытия меню поиска РП.\n`/set_news_channel` | Установить канал для рассылки новостей **RustMe Helper**\n`/set_team_channel` Установит канал для рассылки поиска команды",inline=False)
            embed.set_footer(text="RustMe Helper не является официальным продуктом RustMe, не утвержден RustMe.")
        else:
            embed = discord.Embed(title="Помощь", color=discord.Colour.red())
            embed.add_field(name="Команды для участника", value="`/help` | Покажет эту страницу\n`/browse` | Откроет меню поиска РП\n`/offer` | Подать свой рп на рассмотрение\n`/calc` | Калькулятор взрывчатки\n`/scheme` | Схемы электричества\n`/tea` | Информация о чаях\n`/wipes` | Таблица вайпов\n`/recycle` | Таблица переработки компонентов\n`/find_team` | Поиск команды",inline=False)
            embed.set_footer(text="RustMe Helper не является официальным продуктом RustMe, не утвержден RustMe.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot: discord.Bot) -> None:
    bot.add_cog(help(bot))
