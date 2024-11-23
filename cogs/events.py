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

class events(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        
    @discord.Cog.listener()
    async def on_ready(self) -> None:
        logger.debug("Cog events loaded")
    
    @discord.Cog.listener()  
    async def on_guild_join(self, guild: discord.Guild):
        owner = guild.owner 
        inviter = None

        embed = discord.Embed(title="Спасибо что пригласили меня на сервер!", color=discord.Colour.red())
        embed.add_field(name="Команды для участника", value="`/help` | Покажет эту страницу.\n`/browse` | Откроет меню поиска РП.\n`/offer` | Подать свой рп на рассмотрение\n`/calc` | Калькулятор взрывчатки\n`/scheme` | Схемы электричества\n`/tea` | Информация о чаях",inline=False)
        embed.add_field(name="Команды для администратора", value="`/browsemessage` | Отправит в выбраный канал статичное сообщение открытия меню поиска РП.",inline=False)
        embed.set_footer(text="RustMe Helper не является официальным продуктом RustMe, не утвержден RustMe.")
        
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
            inviter = entry.user

        if owner:
            try:
                await owner.send(embed=embed)
            except discord.Forbidden:
                print(f"Не удалось отправить сообщение владельцу сервера {owner.name}.")

        if inviter and inviter != owner:
            try:
                await inviter.send(embed=embed)
            except discord.Forbidden:
                print(f"Не удалось отправить сообщение пользователю {inviter.name}.")


def setup(bot: discord.Bot) -> None:
    bot.add_cog(events(bot))
