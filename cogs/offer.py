import discord
from discord.ext import commands
import asyncio
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


class Confrim(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=None)
                
                self.bot = bot
                
            @discord.ui.button(label="Прочитайте сообщение...", style=discord.ButtonStyle.primary, custom_id="confirm", disabled=True)
            async def browse_callback(self, button, interaction):
                modal = MyModal(self.bot, title="Подача РП")
                await interaction.response.send_modal(modal)
                

class MyModal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.add_item(discord.ui.InputText(label="Название РП", placeholder="Без & и других символов!"))
        self.add_item(discord.ui.InputText(label="Описание РП", placeholder="Описаниe",style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Превью", placeholder="Ссылка на imgur.com"))
        self.add_item(discord.ui.InputText(label="Ресурс-пак", placeholder="Ссылка на drive.google.com"))
        self.add_item(discord.ui.InputText(label="Тип РП", placeholder="Классика | DLC | Moded | Обновление"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(title=f"{interaction.user.name} подал рп на рассмотрение.")
        embed.add_field(name="Название", value=f"{self.children[0].value}", inline=False)
        embed.add_field(name="Описание", value=f"{self.children[1].value}", inline=False)
        embed.add_field(name="Превью", value=f"{self.children[2].value}", inline=False)
        embed.add_field(name="Ресурс-пак", value=f"{self.children[3].value}", inline=False)
        embed.add_field(name="Тип РП", value=f"{self.children[4].value}", inline=False)
        try:
            guild = await self.bot.fetch_guild("1275727514093752404")
            channel = await guild.fetch_channel("1275829889458503730")
            await channel.send("@everyone", embed=embed)
            await interaction.followup.send("✅ Вы успешно подали рп на рассмотрение, ожидайте ответа.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"🛑 Произошла ошибка, повторите позже. Ошибка: {e}", ephemeral=True)
            
                   
class offer(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.add_view(Confrim(self.bot))
        logger.debug("Cog offer loaded")


    @discord.slash_command(description="Предложите ваш рп для добавления в библиотеку RMHelper.")
    async def offer(self, interaction) -> None:
        view = Confrim(self.bot)
        embed = discord.Embed(title="Сводка", description="Перед подачей ресурс пака(рп) обязательно ознакомтесь:\n\nРп должен соответствовать правилам указаных на сервере Rust, ознакомится [Здесь](https://discord.com/channels/456404359471955990/1201193454345142423)\n\nРесурс пак не должен быть запакован в виде папки(когда нужна разархивация), пожалуйста предоставьте ссылку на архив сразу с ресурс паком.\n\nРп обязан иметь превью(на любом хостинге фотографий)", color=discord.Colour.brand_red())
        embed.set_footer(text="Кнопка будет доступна через 25 секунд!")
        message = await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        await asyncio.sleep(25)
        
        for child in view.children:
            if isinstance(child, discord.ui.Button) and child.custom_id == "confirm":
                child.disabled = False
                child.label = "Продолжить"
        embed.set_footer(text="Кнопка доступна!")

        await message.edit(embed=embed,view=view)
        
        
        

def setup(bot: discord.Bot) -> None:
    bot.add_cog(offer(bot))
