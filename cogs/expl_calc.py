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

class MyView(discord.ui.View):
    @discord.ui.select(
        min_values=1,
        max_values=4,
        options=[
            discord.SelectOption(label="Взрывчатка C4", emoji="<:timed_explosive_charge:1276146408130609227>", value="0"),
            discord.SelectOption(label="Боевая ракета", emoji="<:rocket:1276146383870759005>", value="1"),
            discord.SelectOption(label="Разрывные патроны", emoji="<:explosive_rifle_bullet:1276146359011119166>", value="2"),
            discord.SelectOption(label="Связка бобовых гранат", emoji="<:satchel:1276146328610668594>", value="3")
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        modal = MyModal(select, title="Калькулятор взрывчатки")
        await interaction.response.send_modal(modal=modal)
        
class MyModal(discord.ui.Modal):
    EXPLOSIVES_DATA = {
        "0": {"label": "Взрывчатка C4", "sulfur": 2000, "coal": 3000, "gp": 1000, "tech": 2},
        "1": {"label": "Боевая ракета", "sulfur": 1400, "coal": 1950, "gp": 650, "pipes": 2},
        "2": {"label": "Разрывные патроны", "sulfur": 50, "coal": 50, "gp": 10, "metal": 10},
        "3": {"label": "Связка бобовых гранат", "sulfur": 480, "coal": 720, "gp": 240, "ropes": 1, "bags": 1}
    }

    def __init__(self, select, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.select = select

        for i in self.select.values:
            self.add_item(discord.ui.InputText(
                label=self.EXPLOSIVES_DATA[i]["label"],
                placeholder="Введите кол-во (число, ex.: 4)"
            ))
                    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        total = {
            "sulfur": 0, "coal": 0, "pipes": 0, "tech": 0,
            "metal": 0, "ropes": 0, "bags": 0, "gp": 0
        }

        for i in self.children:
            try:
                count = int(i.value)
            except ValueError:
                await interaction.followup.send("Укажите число.", ephemeral=True)
                return
            
            for key, value in self.EXPLOSIVES_DATA.items():
                if i.label == value["label"]:
                    for resource, amount in value.items():
                        if resource != "label":
                            total[resource] += amount * count

        message = []
        resource_emojis = {
            "sulfur": "<:sulfur:1276146456436408401>",
            "coal": "<:coal:1276146478368166032>",
            "pipes": "<:metal_pipe:1276146526913298543>",
            "tech": "<:tech_trash:1276146556881342548>",
            "metal": "<:metal_fragments:1276146430137864212>",
            "ropes": "<:rope:1276146583406247979>",
            "bags": "<:small_stash:1276146610820354048>",
            "gp": "<:gunpowder:1280434085604626535>"
        }

        for resource, value in total.items():
            if value > 0:
                message.append(f"{resource_emojis[resource]} x{value}")

        embed = discord.Embed(
            title="Результат", 
            description="\n".join(message) + f"\n\n Сводка:\n Скрафтите {total['gp']} {resource_emojis['gp']}",
            color=discord.Colour.gold()
        )
        embed.set_footer(text="Спасибо, что используете RustMe Helper!")    
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user.name} использовал калькулятор взрывчатки.")

class expl_calc(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

def setup(bot: discord.Bot) -> None:
    bot.add_cog(expl_calc(bot))
