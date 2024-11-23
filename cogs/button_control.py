import discord
from discord.ext import commands
import cogs.main_calc as expl
import cogs.recycle as recycle
import cogs.map as map
import cogs.electr_calc as electr
import cogs.wipes as wipes
import cogs.team_broadcast as findteam
import cogs.tea_calc as tea

class btnControl(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.add_view(self.Menu(self))

    @discord.slash_command()
    @commands.has_permissions(administrator=True)
    async def menumessage(self, interaction) -> None:
        embed = discord.Embed(title="Меню", description="Хранит в себе **весь** функционал бота RustMe Helper.\nЧтобы открыть меню нажмите на кнопку ниже 🔽", color=discord.Colour.brand_red())
        try:
            await interaction.channel.send(embed=embed, view=self.Menu(self))
            await interaction.response.send_message("✅ Успешно", ephemeral=True)
        except:
            await interaction.response.send_message("❌ Недостаточно прав.", ephemeral=True)

    class Menu(discord.ui.View):
        def __init__(self, parent):
            super().__init__(timeout=None)
            self.parent = parent
    
        @discord.ui.button(label="Открыть меню", style=discord.ButtonStyle.gray, emoji="📋", custom_id="menu")
        async def browse_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(view=self.parent.PackView(self.parent), ephemeral=True)

    class PackSelect(discord.ui.Select):
        def __init__(self, parent):
            self.parent = parent
            options = [
                discord.SelectOption(label="Калькуляторы", emoji="🔢"),
                discord.SelectOption(label="Карта", emoji="🗺"),
                discord.SelectOption(label="Калькулятор чая", emoji="☕"),
                discord.SelectOption(label="Поиск команды", emoji="👥"),
                discord.SelectOption(label="Схемы электричества", emoji="⚡"),
                discord.SelectOption(label="Таблица вайпов", emoji="📃"),
                discord.SelectOption(label="Таблица переработки", emoji="♻")
            ]
            super().__init__(placeholder="Выберите функцию...", options=options, max_values=1, min_values=1)

        async def callback(self, interaction: discord.Interaction):
            match self.values[0]:
                case "Калькуляторы":
                    await expl.calc.calc(interaction)
                case "Карта":
                    await map.map.map(interaction)
                case "Калькулятор чая":
                    await tea.tea_calc.tea(interaction)
                case "Поиск команды":
                    await interaction.response.send_message(view=self.parent.TeamSelectView(self.parent), ephemeral=True)
                case "Схемы электричества":
                    await electr.electr_calc.scheme(interaction)
                case "Таблица вайпов":
                    await interaction.response.send_message(view=self.parent.WipeSelectView(self.parent), ephemeral=True)
                case "Таблица переработки":
                    await recycle.Recycle.recycle_info(interaction)

    class PackView(discord.ui.View):
        def __init__(self, parent):
            super().__init__(timeout=None)
            self.add_item(parent.PackSelect(parent))

    class TeamSelect(discord.ui.Select):
        def __init__(self, parent):
            self.parent = parent
            options = [
                discord.SelectOption(label="Клан", emoji="👥"),
                discord.SelectOption(label="Соло", emoji="👤")
            ]
            super().__init__(placeholder="Вы клан или соло игрок?...", options=options, max_values=1, min_values=1)

        async def callback(self, interaction: discord.Interaction):
            match self.values[0]:
                case "Клан":
                    await findteam.TeamBroadcast.broadcast_team_message(self.parent, interaction, type="Клан")
                case "Соло":
                    await findteam.TeamBroadcast.broadcast_team_message(self.parent, interaction, type="Соло")

    class TeamSelectView(discord.ui.View):
        def __init__(self, parent):
            super().__init__(timeout=None)
            self.add_item(parent.TeamSelect(parent))

    class WipeSelect(discord.ui.Select):
        def __init__(self, parent):
            self.parent = parent
            options = [
                discord.SelectOption(label="Глобальный"),
                discord.SelectOption(label="Следующий")
            ]
            super().__init__(placeholder="Выберите тип вайпа...", options=options, max_values=1, min_values=1)

        async def callback(self, interaction: discord.Interaction):
            match self.values[0]:
                case "Глобальный":
                    await interaction.response.send_message(view=self.parent.WipeDaySelectView(parent=self.parent, type="Глобальный"))
                case "Следующий":
                    await interaction.response.send_message(view=self.parent.WipeDaySelectView(parent=self.parent, type="Следующий"))

    class WipeSelectView(discord.ui.View):
        def __init__(self, parent):
            super().__init__(timeout=None)
            self.add_item(parent.WipeSelect(parent))
            
    class WipeDaySelect(discord.ui.Select):
        def __init__(self, parent, type):
            self.parent = parent
            self.type = type
            options = [
                discord.SelectOption(label="Пятница"),
                discord.SelectOption(label="Понедельник")
            ]
            super().__init__(placeholder="Выберите день вайпа...", options=options, max_values=1, min_values=1)

        async def callback(self, interaction: discord.Interaction):
            match self.values[0]:
                case "Глобальный":
                    await wipes.Wipes.wipe(interaction, type=self.type, day="Понедельник")
                case "Следующий":
                    await wipes.Wipes.wipe(interaction, type=self.type, day="Понедельник")

    class WipeDaySelectView(discord.ui.View):
        def __init__(self, parent, type):
            super().__init__(timeout=None)
            self.add_item(parent.WipeSelect(type=type))

def setup(bot: discord.Bot) -> None:
    bot.add_cog(btnControl(bot))
