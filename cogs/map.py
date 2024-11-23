import json
from discord import Intents, SelectOption, Interaction, Embed
from discord.ext import commands
from discord.ui import View, Select
import discord
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

def load_data():
    with open('configs/map.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def extract_options(json_data):
    options = []
    for key, value in json_data.items():
        if key == "mainmap":
            continue
        if isinstance(value, dict):
            options.append(SelectOption(label=key, value=key))
        else:
            options.append(SelectOption(label=key, value=key))
    return options

bot = discord.Bot()



class map(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        
    @discord.Cog.listener()
    async def on_ready(self) -> None:
        logger.debug("Cog map loaded")


    @discord.slash_command(description="Покажет карту RustMe со всеми локациями и лутом.")
    async def map(self, interaction):
        data = load_data()
        embed = discord.Embed(title="Карта RustMe")
        embed.set_image(url=data['RT']['mainmap'])
        embed.set_footer(text='Copyright RustMe Helper')
        class MainSelectMenuView(View):
            def __init__(self):
                super().__init__()

                data = load_data()
                options = extract_options(data['RT'])
                self.select = Select(
                    placeholder="Выберите локацию...",
                    options=options,
                    custom_id="main_select_menu"
                )
                self.select.callback = self.main_select_callback
                self.add_item(self.select)

            async def main_select_callback(self, interaction: Interaction):
                data = load_data()
                selected_option = interaction.data['values'][0]
                selected_data = data['RT'][selected_option]


                if isinstance(selected_data, dict):
                    embed = Embed(title=f"{selected_option}")
                    embed.set_image(url=selected_data['map'])
                    embed.set_footer(text="Copyright RustMe Helper")
                    nested_view = NestedSelectMenuView(selected_data, embed)
                    await interaction.response.send_message(view=nested_view, embed=embed, ephemeral=True)

                else:
                    embed = Embed(title=f"{selected_option}")
                    embed.set_image(url=selected_data)
                    embed.set_footer(text="Copyright RustMe Helper")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
                logger.info(f"{interaction.user.name} использовал карту")

        class NestedSelectMenuView(View):
            def __init__(self, nested_data, parent_embed):
                super().__init__()

                data = load_data()
                self.nested_data = nested_data
                self.parent_embed = parent_embed
                self.map_text = nested_data.get("map", "")
                
                options = [SelectOption(label=k, value=k) 
                        for k, v in nested_data.items() if k != "map"]

                self.select = Select(
                    placeholder="Выберите локацию...",
                    options=options,
                    custom_id="nested_select_menu"
                )
                self.select.callback = self.nested_select_callback
                self.add_item(self.select)

            async def nested_select_callback(self, interaction: Interaction):
                data = load_data()
                selected_option = interaction.data['values'][0]
                selected_data = self.nested_data[selected_option]

                if isinstance(selected_data, str) and selected_data.startswith("http"):
                    self.parent_embed.set_image(url=selected_data)
                    await interaction.response.send_message(embed=self.parent_embed, ephemeral=True)
                else:
                    self.parent_embed.description = f"{selected_option}: {selected_data}"
                    await interaction.response.send_message(embed=self.parent_embed, ephemeral=True)

        await interaction.response.send_message(embed=embed, view=MainSelectMenuView(), ephemeral=True)

def setup(bot: discord.Bot) -> None:
    bot.add_cog(map(bot))