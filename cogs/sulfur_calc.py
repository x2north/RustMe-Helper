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
        max_values=1,
        placeholder="Выберите ресурс...",
        options=[
            discord.SelectOption(label="Порох", emoji="<:gunpowder:1280434085604626535>", value="0"),
            discord.SelectOption(label="Сера", emoji="<:sulfur:1276146456436408401>", value="1")
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        modal = MyModal(select, title="Калькулятор остатка")
        await interaction.response.send_modal(modal=modal)

class MyModal(discord.ui.Modal):
    def __init__(self, select, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.select = select

        for i in self.select.values:
            match i:
                case "0":
                    self.add_item(discord.ui.InputText(label="Порох", placeholder="Введите кол-во (число, ex.: 10000)"))
                case "1":
                    self.add_item(discord.ui.InputText(label="Сера", placeholder="Введите кол-во (число, ex.: 15000)"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        resources = {
            'rocket': {
                'gp': 650,
                'sulfur': 100,
                'coal': 1950,
                'pipes': 2
            },
            'c4': {
                'gp': 1000,
                'sulfur': 200,
                'coal': 3000,
                'tech': 2
            },
            'exp': {
                'gp': 10,
                'sulfur': 5,
                'coal': 50,
                'metal': 10
            },
            'satchel': {
                'gp': 240,
                'sulfur': 0,
                'coal': 720,
                'bags': 1,
                'ropes': 1
            }
        }

        try:
            value = int(self.children[0].value)
        except ValueError:
            await interaction.followup.send("Укажите число.", ephemeral=True)
            return

        if self.children[0].label == 'Порох':
            rockets = value // resources['rocket']['gp']
            rockets_left = value % resources['rocket']['gp']

            c4 = value // resources['c4']['gp']
            c4_left = value % resources['c4']['gp']

            exp = value // resources['exp']['gp']
            exp_left = value % resources['exp']['gp']

            satchel = value // resources['satchel']['gp']
            satchel_left = value % resources['satchel']['gp']

            embed = discord.Embed(title="Результат", description=f"Из {value} пороха вы можете скрафтить:", color=discord.Colour.brand_green())
            embed.add_field(name=f"<:timed_explosive_charge:1276146408130609227> x{c4}", value=f"Вам понадобится:\n<:sulfur:1276146456436408401> x{resources['c4']['sulfur'] * c4} \n<:tech_trash:1276146556881342548> x{resources['c4']['tech'] * c4}\n Остаток: \n{c4_left} <:gunpowder:1280434085604626535> \n ----------------------------", inline=False)
            embed.add_field(name=f"<:rocket:1276146383870759005> x{rockets}", value=f"Вам понадобится:\n<:sulfur:1276146456436408401> x{resources['rocket']['sulfur'] * rockets}\n<:metal_pipe:1276146526913298543> x{resources['rocket']['pipes'] * rockets}\n Остаток: \n{rockets_left} <:gunpowder:1280434085604626535> \n ----------------------------", inline=False)
            embed.add_field(name=f"<:explosive_rifle_bullet:1276146359011119166> x{exp}", value=f"Вам понадобится:\n<:sulfur:1276146456436408401> x{resources['exp']['sulfur'] * exp}\n<:metal_fragments:1276146430137864212> x{resources['exp']['metal'] * exp}\n Остаток: \n{exp_left} <:gunpowder:1280434085604626535> \n ----------------------------", inline=False)
            embed.add_field(name=f"<:satchel:1276146328610668594> x{satchel}", value=f"Вам понадобится:\n<:small_stash:1276146610820354048> x{resources['satchel']['bags'] * satchel} \n<:rope:1276146583406247979> x{resources['satchel']['ropes'] * satchel}\n Остаток: \n{satchel_left} <:gunpowder:1280434085604626535> \n ----------------------------", inline=False)
            embed.set_footer(text="Спасибо что используете RustMe Helper!")
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user.name} использовал калькулятор перекрафта пороха.")

        elif self.children[0].label == 'Сера':
            rockets = value // resources['rocket']['sulfur']
            rockets_left = value % resources['rocket']['sulfur']

            c4 = value // resources['c4']['sulfur']
            c4_left = value % resources['c4']['sulfur']

            exp = value // resources['exp']['sulfur']
            exp_left = value % resources['exp']['sulfur']

            embed = discord.Embed(title="Результат", description=f"Из {value} серы вы можете скрафтить:", color=discord.Colour.brand_green())
            embed.add_field(name=f"<:timed_explosive_charge:1276146408130609227> x{c4}", value=f"Вам понадобится:\n<:coal:1276146478368166032> x{resources['c4']['coal'] * c4} \n<:tech_trash:1276146556881342548> x{resources['c4']['tech'] * c4}\n Остаток: \n{c4_left} <:sulfur:1276146456436408401> \n ----------------------------", inline=False)
            embed.add_field(name=f"<:rocket:1276146383870759005> x{rockets}", value=f"Вам понадобится:\n<:coal:1276146478368166032> x{resources['rocket']['coal'] * rockets}\n<:metal_pipe:1276146526913298543> x{resources['rocket']['pipes'] * rockets}\n Остаток: \n{rockets_left} <:sulfur:1276146456436408401> \n ----------------------------", inline=False)
            embed.add_field(name=f"<:explosive_rifle_bullet:1276146359011119166> x{exp}", value=f"Вам понадобится:\n<:coal:1276146478368166032> x{resources['exp']['coal'] * exp}\n<:metal_fragments:1276146430137864212> x{resources['exp']['metal'] * exp}\n Остаток: \n{exp_left} <:sulfur:1276146456436408401> \n ----------------------------", inline=False)
            embed.set_footer(text="Спасибо что используете RustMe Helper!")
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user.name} использовал калькулятор перекрафта серы.")




class sulfur_calc(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot


def setup(bot: discord.Bot) -> None:
    bot.add_cog(sulfur_calc(bot))
