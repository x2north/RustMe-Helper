import discord
from discord.ext import commands
import configs.electricity as schemes
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

class ChoseType(discord.ui.View):
    @discord.ui.select(
        placeholder="Выберите тип...",
        max_values=1,
        options=[
            discord.SelectOption(label="Турели", emoji="<:autoturret:1276204794201247775>", value="0"),
            discord.SelectOption(label="ПВО", emoji="<:samsite:1276204787372920936>", value="1"),
            discord.SelectOption(label="Лампы", emoji="<:ceilinglight:1280968936447279249>", value="2"),
            discord.SelectOption(label="Обогреватели", emoji="<:electricheater:1280968927601492029>", value="3"),
            discord.SelectOption(label="Ферма", emoji="<:planter:1281028248767037442>", value="4")
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        match select.values[0]:
            case "0":
                await interaction.response.send_message(view=ChoseNumberTurret(),ephemeral=True)
            case "1":
                await interaction.response.send_message(view=ChoseNumberPVO(),ephemeral=True)
            case "2":
                embed = discord.Embed(title="Система света", description="Лампы в расте имеют вход и выход энергии, это позволяет делать цепь подключения без использования разветвителей.", color=discord.Colour.yellow())
                await interaction.response.send_message(content=schemes.light,embed=embed,ephemeral=True)
                logger.info(f"{interaction.user.name} использовал схемы электрики")
            case "3":
                embed = discord.Embed(title="Система обогрева", description="Обогреватели в расте имеют вход и выход энергии, это позволяет делать цепь подключения без использования разветвителей.", color=discord.Colour.dark_red())
                await interaction.response.send_message(content=schemes.heater,embed=embed,ephemeral=True)
                logger.info(f"{interaction.user.name} использовал схемы электрики")
            case "4":
                embed = discord.Embed(title="Система фермы", description="Разбрызгиватели в расте имеют вход и выход воды, это позволяет делать цепь подключения без использования разделителя. \n\n │ - электричество, провод.\n\n║ - вода, труба. \n\n **Не работает на телефоне!**", color=discord.Colour.blurple())
                await interaction.response.send_message(content=schemes.farm, embed=embed, ephemeral=True)
                logger.info(f"{interaction.user.name} использовал схемы электрики")
            
        
class ChoseNumberTurret(discord.ui.View):
    @discord.ui.select(
        placeholder="Выберите количество...",
        max_values=1,
        options=[
            discord.SelectOption(label="1", emoji="<:autoturret:1276204794201247775>", value="1"),
            discord.SelectOption(label="2", emoji="<:autoturret:1276204794201247775>", value="2"),
            discord.SelectOption(label="3", emoji="<:autoturret:1276204794201247775>", value="3"),
            discord.SelectOption(label="4", emoji="<:autoturret:1276204794201247775>", value="4"),
            discord.SelectOption(label="5", emoji="<:autoturret:1276204794201247775>", value="5"),
            discord.SelectOption(label="6", emoji="<:autoturret:1276204794201247775>", value="6"),
            discord.SelectOption(label="7", emoji="<:autoturret:1276204794201247775>", value="7"),
            discord.SelectOption(label="8", emoji="<:autoturret:1276204794201247775>", value="8"),
            discord.SelectOption(label="9", emoji="<:autoturret:1276204794201247775>", value="9")
        ]
    )
    async def select2_callback(self, select, interaction: discord.Interaction):
        logger.info(f"{interaction.user.name} использовал схемы электрики")
        match select.values[0]:
            case "1":
                await interaction.response.send_message(content=schemes.turret1,ephemeral=True)
                
            case "2":
                await interaction.response.send_message(content=schemes.turret2,ephemeral=True)
            
            case "3":
                await interaction.response.send_message(content=schemes.turret3,ephemeral=True)
                
            case "4":
                await interaction.response.send_message(content=schemes.turret4,ephemeral=True)
            
            case "5":
                await interaction.response.send_message(content=schemes.turret5,ephemeral=True)
                
            case "6":
                await interaction.response.send_message(content=schemes.turret6,ephemeral=True)
                
            case "7":
                await interaction.response.send_message(content=schemes.turret7,ephemeral=True)
                
            case "8":
                await interaction.response.send_message(content=schemes.turret8,ephemeral=True)
                        
            case "9":
                await interaction.response.send_message(content=schemes.turret9,ephemeral=True)   
        

class ChoseNumberPVO(discord.ui.View):
    @discord.ui.select(
        placeholder="Выберите количество...",
        max_values=1,
        options=[
            discord.SelectOption(label="1", emoji="<:samsite:1276204787372920936>", value="1"),
            discord.SelectOption(label="2", emoji="<:samsite:1276204787372920936>", value="2"),
            discord.SelectOption(label="3", emoji="<:samsite:1276204787372920936>", value="3"),
            discord.SelectOption(label="4", emoji="<:samsite:1276204787372920936>", value="4")
        ]
    )
    async def select2_callback(self, select, interaction: discord.Interaction):
        logger.info(f"{interaction.user.name} использовал схемы электрики")
        match select.values[0]:
            case "1":
                await interaction.response.send_message(content=schemes.pvo1,ephemeral=True)
                
            case "2":
                await interaction.response.send_message(content=schemes.pvo2,ephemeral=True)
            
            case "3":
                await interaction.response.send_message(content=schemes.pvo3,ephemeral=True)
                
            case "4":
                await interaction.response.send_message(content=schemes.pvo4,ephemeral=True)
          
                

class electr_calc(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        
    @discord.Cog.listener()
    async def on_ready(self) -> None:
        logger.debug("Cog electr_calc loaded")
        
    @discord.slash_command(description="Схемы электрики.")
    async def scheme(self, interaction) -> None:
        await interaction.response.send_message(view=ChoseType(),ephemeral=True)

def setup(bot: discord.Bot) -> None:
    bot.add_cog(electr_calc(bot))
