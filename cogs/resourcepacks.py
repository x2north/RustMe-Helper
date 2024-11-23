import discord
from discord.ext import commands
import json
import config_manif as cfg
import discord.ext.commands.errors

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

def load_rp():
    with open("configs/resourcepacks.json", "r", encoding='utf-8') as file:
        data = json.load(file)
        return data
    
def category_color(category: str):
    match category:
        case "Классика":
            return discord.Colour.og_blurple()
        case "DLC":
            return discord.Colour.brand_red()
        case "Модифицированный":
            return discord.Colour.dark_blue()

class CategorySelect(discord.ui.Select):
    def __init__(self):
        data = load_rp()
        options = [
            discord.SelectOption(label=category, emoji="<:folder:1275747167428149298>") for category in data["resourcepacks"].keys()
        ]
        super().__init__(placeholder="Выберите категорию...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        selected_category = self.values[0]
        await interaction.followup.send(
            content=f"Вы выбрали категорию: {selected_category}",
            view=PackSelectView(selected_category), 
            ephemeral=True
            
        )
        
        
        
class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Помощь с установкой DLC", emoji="❔", value="dlc"),
            discord.SelectOption(label="Хотите добавить свой РП", emoji="❔", value="addyour"),
            discord.SelectOption(label="Пользовательское соглашение", emoji="📝", value="rules")
        ]
        super().__init__(placeholder="Выберите категорию...", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_category = self.values[0]
        match selected_category:
            case "dlc":
                embed = discord.Embed(title="Мануал по установке DLC", color=discord.Colour.green())
                embed.add_field(name="Что такое DLC?", value="Давайте представим. Есть **DLC под номером 1**, которое заменяет цвет кабана на красный, а также есть **2-е DLC** который заменяет цвет кабана на синий и добавляет на штурмовую винтовку скин.", inline=False)
                embed.add_field(name="Как установить?", value="# **Основной принцип работы** Давайте представим. Есть **DLC под номером 1**, которое заменяет цвет кабана на красный, а также есть __2-е DLC__ который заменяет цвет кабана на синий и добавляет на штурмовую винтовку скин У нас есть *основной RP*, допустим возьмём оригинальный ресурс пак RustMe. Основным RP может быть и наш ресурс пак или другого пользователя. Основной RP мы *обязательно* ставим в самый низ. Ставим наверх основного RP __2-е DLC__. В игре меняется не весь ресурс пак, а только то, что имеется во __2-м DLC__, а это как мы помним синий кабан и скин на штурмовую винтовку. Теперь ставим выше  __2-о DLC__ **1-е DLC** и в игре меняется только кабан, теперь он красный, но скин на винтовку остаётся. Теперь если мы поднимем __2-е DLC__ так чтобы **1-е DLC** было снизу, то красного кабана уже не будет, теперь в игре только синий кабан с скином на винтовку. `DLC меняет объекты во всех ресурс паках снизу то, что в него добавлено", inline=False)
                embed.add_field(name="Пример установки", value="LumberJack Pack - *DLC*\nRP CLASS565 4.1 - *Основной RP*")
                embed.set_footer(text="Автор мануала: CLASS565 | https://discord.gg/rRBgS9hzQe")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1043851361432903742/1050155090742353940/image.png?ex=66c6fe64&is=66c5ace4&hm=5ce5f47e841ea3d15724070b5f86b09eb2c7a62f78fdc4ed01e2a4ee404a6846&")     
            case "addyour":
                embed = discord.Embed(title="Партнерская программа", color=discord.Colour.purple())
                embed.description = "Вы разработчик РП и хотите добавить его в бота?\n Используйте команду `/offer` и ожидайте ответа."
            case "rules":
                embed = discord.Embed(title="Правила использования", color=discord.Colour.red())
                embed.add_field(name="Политика", value="Все ресурс паки должны соблюдать правила серверов [RustMe](https://rustme.net/), любая попытка их нарушить приведет к удалению РП и его блокировке.\n\n Мы не несем ответственность в случае игровой блокировки при попытке изменения РП. \n\n Если РП с обновлением правил перестает соблюдать их, создатель обязан сообщить администраторам ([Magasty](https://discordapp.com/users/692387119892529255) | [Iwoje](https://discordapp.com/users/962274709368623116))\n\n RustMe Helper не является официальным продуктом RustMe, не утвержден RustMe.", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)
                

class PackSelect(discord.ui.Select):
    def __init__(self, category):
        data = load_rp()
        self.category = category
        packs = data["resourcepacks"][category]
        
        options = []
        for pack_key, pack_data in packs.items():
            emoji = "<:partner:1281008270617870442>" if pack_data.get('partner', False) else "<:download:1281008276196294699>"
            options.append(discord.SelectOption(label=pack_key, emoji=emoji))
        
        super().__init__(placeholder="Выберите ресурс-пак...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        data = load_rp()
        selected_pack = self.values[0]
        pack_data = data["resourcepacks"][self.category][selected_pack]
        if pack_data['version'] == f"{cfg.client_version()}":
            embed = discord.Embed(title=f"{selected_pack}", color=category_color(self.category))
        else:
            embed = discord.Embed(title=f"{selected_pack} <:warning:1275746946446921728> Устарел", color=category_color(self.category))
        embed.description = pack_data['description']
        embed.add_field(name="Author", value=f"```{pack_data['author']}```", inline=False)
        if pack_data['last_update'] != "Никогда":
            embed.add_field(name="Last update", value=f"```{pack_data['last_update']} ```", inline=True)
        else:
            pass
        if pack_data['image_link'] != None:
            embed.set_image(url=pack_data['image_link'])
        else:
            pass
        embed.add_field(name="Установка", value=f"[[Скачать]]({pack_data['link']})", inline=True)
        embed.add_field(name="Тип установки", value=f"```{pack_data['install']}```", inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

class CategorySelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CategorySelect())

class PackSelectView(discord.ui.View):
    def __init__(self, category):
        super().__init__()
        self.add_item(PackSelect(category))
        
class HelpSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpSelect())

class BrowseRP(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                
            @discord.ui.button(label="Поиск", style=discord.ButtonStyle.gray, emoji="🔍", custom_id="browserp")
            async def browse_callback(self, button, interaction):
                await interaction.response.defer(ephemeral=True)
                await interaction.followup.send(view=CategorySelectView(), ephemeral=True)
            
            @discord.ui.button(label="Помощь", style=discord.ButtonStyle.grey, emoji="❔", custom_id="helprp")
            async def help_callback(self, button, interaction):
                await interaction.response.defer(ephemeral=True)
                await interaction.followup.send(view=HelpSelectView(), ephemeral=True)

        
        
        
        
        
################################################################################################################





class RP(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.add_view(BrowseRP())
        logger.debug("Cog resourcepacks loaded")

    @discord.slash_command(description="Начать поиск ресурс-паков")
    async def browse(self, interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(view=CategorySelectView(), ephemeral=True)
        
        
    @discord.slash_command(description="Отправляет статичное сообщение (Только для администрации.)")
    @discord.guild_only()
    @commands.has_permissions(administrator=True)
    async def browsemessage(self, interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            embed = discord.Embed(title="Поиск рп", description="RustMe Helper - библиотека ресурс-паков для серверов RustMe.\nЧтобы начать поиск нажмите на кнопку ниже 🔽", color=discord.Colour.red())
            channel = interaction.channel
            await channel.send(embed=embed, view=BrowseRP())
            await interaction.followup.send("✅ Успешно", ephemeral=True)
        except discord.ext.commands.errors.MissingPermissions as e:
            await interaction.followup.send("❌ У Бота недостаточно прав.", ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.followup.send("❌ У Бота Недостаточно прав.", ephemeral=True)
        
def setup(bot: discord.Bot) -> None:
    bot.add_cog(RP(bot))