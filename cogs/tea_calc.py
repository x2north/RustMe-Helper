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

def load_data(tea):
    with open('configs/teas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['teas'][f'{tea}']
    
    
    
def calc_pure(berries, number):
    cberries = [int(num) * 16 * int(number) for num in berries]
        
    return cberries

def calc_adv(berries, number):
    cberries = [int(num) * 4 * int(number) for num in berries]
        
    return cberries

def calc_basic(berries, number):
    cberries = [int(num) * int(number) for num in berries]
        
    return cberries


class teaView(discord.ui.View):
    @discord.ui.select(
        min_values=1,
        placeholder="Выберите чай...",
        options=[
            discord.SelectOption(label="Рудный чай", emoji="<:pure_ore_tea:1279541266119524535>", value="0"),
            discord.SelectOption(label="Древесный чай", emoji="<:pure_wood_tea:1279541430338977793>", value="1"),
            discord.SelectOption(label="Чай на добычу металлолома", emoji="<:pure_scrap_tea:1279541350831751262>", value="2"),
            discord.SelectOption(label="Чай на максимальное здоровье", emoji="<:pure_max_health_tea:1279541171680579647>", value="3"),
            discord.SelectOption(label="Антирадиационный чай", emoji="<:pure_antirad_tea:1279541093314330685>", value="4"),
            discord.SelectOption(label="Целебный чай", emoji="<:pure_healing_tea:1279540975911436339>", value="5")
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        modal = MyModal(select, title="Калькулятор чаев")
        await interaction.response.send_modal(modal=modal)



class MyModal(discord.ui.Modal):
    def __init__(self, select, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.select = select

        for i in self.select.values:
            match i:
                case "0":
                    self.add_item(discord.ui.InputText(label="Рудный чай", placeholder="Введите кол-во (число, ex.: 4)"))
                    teaType = 'FarmTea'
                case "1":
                    self.add_item(discord.ui.InputText(label="Древесный чай", placeholder="Введите кол-во (число, ex.: 4)"))
                    teaType = 'TreeTea'
                case "2":
                    self.add_item(discord.ui.InputText(label="Чай на добычу металлолома", placeholder="Введите кол-во (число, ex.: 4)"))
                    teaType = 'ScrapTea'
                case "3":
                    self.add_item(discord.ui.InputText(label="Чай на максимальное здоровье", placeholder="Введите кол-во (число, ex.: 4)"))
                    teaType = 'HPTea'
                case "4":
                    self.add_item(discord.ui.InputText(label="Антирадиационный чай", placeholder="Введите кол-во (число, ex.: 4)"))
                    teaType = 'RadiationTea'
                case "5":
                    self.add_item(discord.ui.InputText(label="Целебный чай", placeholder="Введите кол-во (число, ex.: 4)"))
                    teaType = 'RegenTea'
        
        data = load_data(teaType)
        self.teaType = teaType
        self.description = data['description']
        self.pure = data['pure']
        self.advanced = data['advanced']
        self.basic = data['basic']
        
                    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        yellowberrie = "<:yellowberrie:1279540744176275487>"
        blueberrie = "<:blueberrie:1279540659723960325>"
        redberrie = "<:redberrie:1279540766611607616>"
        whiteberrie = "<:whiteberrie:1279540721627430912>"
        greenberrie = "<:greenberrie:1279540698785251328>"
        
        
        embed = discord.Embed(title="Результат", description=f"{self.description}", color=discord.Colour.gold())
        match self.teaType:
            case 'FarmTea':
                pattern = f"{yellowberrie} | {blueberrie} | {yellowberrie} | {blueberrie}"
                berries = [2, 2, 0, 0, 0] #yellow | blue | red | green | white
            case 'TreeTea':
                pattern = f"{redberrie} | {blueberrie} | {redberrie} | {blueberrie}"
                berries = [0, 2, 2, 0, 0] #yellow | blue | red | green | white
            case 'ScrapTea':
                pattern = f"{yellowberrie} | {whiteberrie} | {yellowberrie} | {whiteberrie}"
                berries = [2, 0, 0, 0, 2] #yellow | blue | red | green | white
            case 'HPTea':
                pattern = f"{redberrie} | {redberrie} | {redberrie} | {yellowberrie}"
                berries = [1, 0, 3, 0, 0] #yellow | blue | red | green | white
            case 'RadiationTea':
                pattern = f"{redberrie} | {redberrie} | {greenberrie} | {greenberrie}"
                berries = [0, 0, 2, 2, 0] #yellow | blue | red | green | white
            case 'RegenTea':
                pattern = f"{redberrie} | {redberrie} | {redberrie} | {redberrie}"
                berries = [0, 0, 4, 0, 0] #yellow | blue | red | green | white
                
        bpure = calc_pure(berries, self.children[0].value)
        badv = calc_adv(berries, self.children[0].value)
        bbasic = calc_basic(berries, self.children[0].value)
        
        mpure = []
        madv = []
        mbasic = []
        
        if bpure[0] > 0:
            mpure.append(f"{yellowberrie} x{bpure[0]}\n")
        if bpure[1] > 0:
            mpure.append(f"{blueberrie} x{bpure[1]}\n")
        if bpure[2] > 0:
            mpure.append(f"{redberrie} x{bpure[2]}\n")
        if bpure[3] > 0:
            mpure.append(f"{greenberrie} x{bpure[3]}\n")
        if bpure[4] > 0:
            mpure.append(f"{whiteberrie} x{bpure[4]}\n")

        if badv[0] > 0:
            madv.append(f"{yellowberrie} x{badv[0]}\n")
        if badv[1] > 0:
            madv.append(f"{blueberrie} x{badv[1]}\n")
        if badv[2] > 0:
            madv.append(f"{redberrie} x{badv[2]}\n")
        if badv[3] > 0:
            madv.append(f"{greenberrie} x{badv[3]}\n")
        if badv[4] > 0:
            madv.append(f"{whiteberrie} x{badv[4]}\n")

        if bbasic[0] > 0:
            mbasic.append(f"{yellowberrie} x{bbasic[0]}\n")
        if bbasic[1] > 0:
            mbasic.append(f"{blueberrie} x{bbasic[1]}\n")
        if bbasic[2] > 0:
            mbasic.append(f"{redberrie} x{bbasic[2]}\n")
        if bbasic[3] > 0:
            mbasic.append(f"{greenberrie} x{bbasic[3]}\n")
        if bbasic[4] > 0:
            mbasic.append(f"{whiteberrie} x{bbasic[4]}\n")

        embed.add_field(name="Паттерн для варки:", value=pattern, inline=False)
        embed.add_field(name="", value="──────────────────────────", inline=True)
        embed.add_field(name=f"{self.pure} Чистый чай.", value="".join(mpure) if mpure else "Нет ингредиентов", inline=False)
        embed.add_field(name=f"{self.advanced} Продвинутый чай.", value="".join(madv) if madv else "Нет ингредиентов", inline=False)
        embed.add_field(name=f"{self.basic} Базовый чай.", value="".join(mbasic) if mbasic else "Нет ингредиентов", inline=False)
        logger.info(f"{interaction.user.name} использовал калькулятор чаев.")
        await interaction.followup.send(embed=embed, ephemeral=True)


class tea_calc(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        
    @discord.Cog.listener()
    async def on_ready(self) -> None:
        logger.debug("Cog tea_calc loaded")

    @discord.slash_command()
    async def tea(self, interaction) -> None:
        await interaction.response.send_message(view=teaView(), ephemeral=True)


def setup(bot: discord.Bot) -> None:
    bot.add_cog(tea_calc(bot))