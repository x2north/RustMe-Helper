import discord
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

emojis = {
    "c4": "<:timed_explosive_charge:1276146408130609227>",
    "rocket": "<:rocket:1276146383870759005>",
    "exp": "<:explosive_rifle_bullet:1276146359011119166>",
    "satchel": "<:satchel:1276146328610668594>",
    "woodenw":"<:wooden_wall:1286056196524216542>",
    "stonew":"<:stone_wall:1286056051745095762>",
    "metalw":"<:metal_wall:1286056175946960958>",
    "hqmw":"<:HQM_wall:1286056073630847167>",
    "hqmd":"<:double_hqm_door:1286056093050605644>",
    "metald":"<:double_metal_door:1286056111102885919>",
    "woodend":"<:double_wooden_door:1286056133135433799>",
    "garaged":"<:garage_door:1286056154207879258>"
}

raid_data = {
    "Железная дверь": {"emoji": emojis["metald"], "c4": 1, "rockets": 2, "exp": 63, "satchels": 4, "minimal": [0, 1, 9]},
    "Гаражная дверь": {"emoji": emojis["garaged"], "c4": 2, "rockets": 3, "exp": 150, "satchels": 10, "minimal": [1, 0, 41]},
    "МВК дверь": {"emoji": emojis["hqmd"], "c4": 3, "rockets": 5, "exp": 250, "satchels": 17, "minimal": [2, 0, 30]},
    "Деревянная дверь": {"emoji": emojis["woodend"], "c4": 1, "rockets": 1, "exp": 19, "satchels": 2, "minimal": [0, 0, 19]},
    "Каменная стена": {"emoji": emojis["stonew"], "c4": 2, "rockets": 4, "exp": 185, "satchels": 10, "minimal": [2, 0, 0]},
    "Железная стена": {"emoji": emojis["metalw"], "c4": 4, "rockets": 8, "exp": 400, "satchels": 23, "minimal": [3, 1, 15]},
    "МВК стена": {"emoji": emojis["hqmw"], "c4": 8, "rockets": 15, "exp": 799, "satchels": 46, "minimal": [7, 0, 31]},
    "Деревянная стена": {"emoji": emojis["woodenw"], "c4": 1, "rockets": 2, "exp": 49, "satchels": 3, "minimal": [0, 0, 49]}
}

class MyView(discord.ui.View):
    @discord.ui.select(
        min_values=1,
        max_values=5,
        options=[discord.SelectOption(label=name, emoji=data["emoji"], value=name) for name, data in raid_data.items()]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        modal = MyModal(select, title="Калькулятор рейда")
        await interaction.response.send_modal(modal=modal)

class MyModal(discord.ui.Modal):
    def __init__(self, select, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.select = select

        for label in self.select.values:
            self.add_item(discord.ui.InputText(label=label, placeholder="Введите кол-во (число, ex.: 4)"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        total = {"rockets": 0, "c4": 0, "exp": 0, "satchels": 0}
        minimal = [0, 0, 0]

        for input_field in self.children:
            try:
                count = int(input_field.value)
            except ValueError:
                await interaction.followup.send("Укажите число.", ephemeral=True)
                return

            data = raid_data.get(input_field.label)
            if data:
                total["rockets"] += data["rockets"] * count
                total["c4"] += data["c4"] * count
                total["exp"] += data["exp"] * count
                total["satchels"] += data["satchels"] * count

                minimal = [min_val + data["minimal"][i] * count for i, min_val in enumerate(minimal)]

        optimal_str = []
        if minimal[0]:
            optimal_str.append(f"x{minimal[0]} {emojis['c4']}")
        if minimal[1]:
            optimal_str.append(f"x{minimal[1]} {emojis['rocket']} ")
        if minimal[2]:
            optimal_str.append(f"x{minimal[2]} {emojis['exp']} ")

        embed = discord.Embed(title="Результат", color=discord.Colour.gold())
        if optimal_str:
            embed.add_field(name="👍 Оптимально:", value="\n".join(optimal_str), inline=False)
            embed.add_field(name="", value="-------------", inline=False)
        embed.add_field(name=f"{emojis['c4']} Взрывчатка C4", value=f"x{total["c4"]}", inline=False)
        embed.add_field(name=f"{emojis['rocket']} Боевая ракета", value=f"x{total["rockets"]}", inline=False)
        embed.add_field(name=f"{emojis['exp']} Разрывной патрон", value=f"x{total["exp"]}", inline=False)
        embed.add_field(name=f"{emojis['satchel']} Связка бобовых гранат", value=f"x{total["satchels"]}", inline=False)
        logger.info(f"{interaction.user.name} использовал калькулятор рейда.")

        await interaction.followup.send(embed=embed, ephemeral=True)


class raid_calc(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

        
        
def setup(bot: discord.Bot) -> None:
    bot.add_cog(raid_calc(bot))




