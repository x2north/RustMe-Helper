import discord
from discord.ext import commands
import sqlite3
import logging
import time
import datetime

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


allowed_users = [692387119892529255, 987654321098765432]
cooldown_time = 180 * 60
choises = ["Клан", "Соло"]

conn = sqlite3.connect('guild_channels.db')
c = conn.cursor()

class SoloModal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.add_item(discord.ui.InputText(label="Ваш ник", placeholder="Игровой никнейм."))
        self.add_item(discord.ui.InputText(label="Ваш донат", placeholder="На аккаунте с выше указаным ником."))
        self.add_item(discord.ui.InputText(label="Ваше описание", placeholder="Расскажите о себе.", style=discord.InputTextStyle.long, max_length=1024, min_length=128))
        self.add_item(discord.ui.InputText(label="Поиск", placeholder="Критерии для поиска.",  style=discord.InputTextStyle.long, max_length=1024, min_length=128))


    async def callback(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Поиск тиммейта(ов)", color=discord.Colour.dark_blue(), timestamp=datetime.datetime.now())
            embed.add_field(name="Никнейм", value=f"```{self.children[0].value}```", inline=False)
            embed.add_field(name="Донат", value=f"```{self.children[1].value}```", inline=False)
            embed.add_field(name="Описание", value=f"```{self.children[2].value}```", inline=False)
            embed.add_field(name="Критерии", value=f"```{self.children[3].value}```", inline=False)
            embed.description = f"Нашли тимейта который вам подходит? Напишите в лс ***{interaction.user.name}***!"
            embed.set_image(url="https://cdn.discordapp.com/attachments/864505449487663124/927213303132983316/222.png?ex=66f818ae&is=66f6c72e&hm=8f2409b56589bcdf0382bcd1a2c6c2cd1d23cd3f35ae076678f4d3432fefaeab&")
        except Exception as e:
            logger.error(f"Ошибка при создании ембеда BTV {e}")
            
            
            
        await broadcast_to_all_guilds(interaction, "team_channel", embed, "embed", self.bot)
        update_last_broadcast_time(interaction.user.id)
        


class ClanModal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.add_item(discord.ui.InputText(label="Описание", placeholder="Расскажите о вашем клане.", style=discord.InputTextStyle.long, max_length=1024, min_length=128))
        self.add_item(discord.ui.InputText(label="Поиск", placeholder="Критерии для поиска игроков.",  style=discord.InputTextStyle.long, max_length=1024, min_length=128))
        self.add_item(discord.ui.InputText(label="Название вашего клана", placeholder="Укажите как называется ваш клан"))


    async def callback(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Поиск игроков в клан", color=discord.Colour.dark_red(), timestamp=datetime.datetime.now())
            embed.add_field(name="Описание", value=f"```{self.children[0].value}```", inline=False)
            embed.add_field(name="Критерии", value=f"```{self.children[1].value}```", inline=False)
            embed.set_image(url="https://cdn.discordapp.com/attachments/864505449487663124/927213303132983316/222.png?ex=66f818ae&is=66f6c72e&hm=8f2409b56589bcdf0382bcd1a2c6c2cd1d23cd3f35ae076678f4d3432fefaeab&")
            embed.add_field(name="Название клана", value=f"```{self.children[2].value}```", inline=False)
            embed.description = f"Подходите по критериям? Напишите в лс ***{interaction.user.name}***!"
        except Exception as e:
            logger.error(f"Ошибка при создании ембеда BTV {e}")
            
            
            
        await broadcast_to_all_guilds(interaction, "team_channel", embed, "embed", self.bot)
        update_last_broadcast_time(interaction.user.id)
        
        
        
        

c.execute('''CREATE TABLE IF NOT EXISTS channels (
                guild_id INTEGER PRIMARY KEY,
                team_channel INTEGER,
                news_channel INTEGER
            )''')


c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY
            )''')


c.execute('''CREATE TABLE IF NOT EXISTS team_broadcast_cooldowns (
                user_id INTEGER PRIMARY KEY,
                last_used REAL
            )''')

conn.commit()

def set_channel_in_db(guild_id, channel_type, channel_id):
    c.execute(f"SELECT * FROM channels WHERE guild_id = ?", (guild_id,))
    result = c.fetchone()
    
    if result:
        c.execute(f"UPDATE channels SET {channel_type} = ? WHERE guild_id = ?", (channel_id, guild_id))
    else:
        if channel_type == "team_channel":
            c.execute("INSERT INTO channels (guild_id, team_channel) VALUES (?, ?)", (guild_id, channel_id))
        elif channel_type == "news_channel":
            c.execute("INSERT INTO channels (guild_id, news_channel) VALUES (?, ?)", (guild_id, channel_id))
    
    conn.commit()

def get_all_channels_from_db(channel_type):
    c.execute(f"SELECT guild_id, {channel_type} FROM channels WHERE {channel_type} IS NOT NULL")
    return c.fetchall()

def delete_channel_from_db(guild_id, channel_type):
    c.execute(f"UPDATE channels SET {channel_type} = NULL WHERE guild_id = ?", (guild_id,))
    conn.commit()

def is_user_banned(user_id):
    c.execute("SELECT * FROM banned_users WHERE user_id = ?", (user_id,))
    return c.fetchone() is not None

def get_last_broadcast_time(user_id):
    c.execute("SELECT last_used FROM team_broadcast_cooldowns WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    return None

def update_last_broadcast_time(user_id):
    current_time = time.time()
    c.execute("INSERT OR REPLACE INTO team_broadcast_cooldowns (user_id, last_used) VALUES (?, ?)", (user_id, current_time))
    conn.commit()

async def broadcast_to_all_guilds(interaction, channel_type, message, message_type, bot):
    channels = get_all_channels_from_db(channel_type)
    success_count = 0
    error_count = 0

    for guild_id, channel_id in channels:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                if message_type == "embed":
                    await channel.send(embed=message)
                else:
                    await channel.send(message)
                success_count += 1
            except Exception as e:
                error_count += 1
                await interaction.response.send_message(f"Ошибка при отправке сообщения в канал {channel_id}: {str(e)}", ephemeral=True)
        else:
            error_count += 1
            try:
                logger.error(f"Канал {channel_id} в гильдии {guild_id} не найден. Удаление...")
                delete_channel_from_db(guild_id, channel_type)
                logger.debug("Канал удален!")
            except Exception as e:
                logger.error(f"Не удалось удалить канал из базы данных: {e}")

    await interaction.response.send_message(f"Сообщение было доставлено в {success_count} канал(ов). \nНе доставлено: {error_count}.", ephemeral=True)
    logger.info(f"{interaction.user.name} использовал систему рассылки.")

    

class TeamBroadcast(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        
    

    
    @discord.slash_command(name='set_team_channel', description="Установить канал рассылки новостей бота RustMe Helper.")
    @commands.has_permissions(administrator=True)
    async def set_team_channel(self, interaction, channel: discord.TextChannel):
        try:
            guild_id = interaction.guild.id
            set_channel_in_db(guild_id, "team_channel", channel.id)
            await interaction.response.send_message(f"Командный канал {channel.mention} был установлен для рассылки!", ephemeral=True)
            logger.debug(f"Канал {channel.id} добавлен под тегом TEAM для сервера {guild_id}.")
        except Exception as e:
            logger.critical(f"Команда setteamchannel вызвала ошибку: {e}")

    @discord.slash_command(name='set_news_channel', description="Установить канал рассылки анкет поиска игроков.")
    @commands.has_permissions(administrator=True)
    async def set_news_channel(self, interaction, channel: discord.TextChannel):
        try:
            guild_id = interaction.guild.id
            set_channel_in_db(guild_id, "news_channel", channel.id)
            await interaction.response.send_message(f"Новостной канал {channel.mention} был установлен для рассылки!", ephemeral=True)
            logger.debug(f"Канал {channel.id} добавлен под тегом NEWS для сервера {guild_id}.")
        except Exception as e:
            logger.critical(f"Команда setnewschannel вызвала ошибку: {e}")

    @discord.slash_command(name='find_team', description="Отправляет сообщение о поиске игроков на сервера! Кулдаун: 180 минут")
    @commands.has_permissions(administrator=True)
    async def broadcast_team_message(self, interaction, type: discord.Option(str, "Укажите являетесь ли вы кланом или соло игроком.", choices=['Клан', 'Соло'])): # type: ignore
        user_id = interaction.user.id


        if is_user_banned(user_id):
            await interaction.response.send_message("Вы находитесь в бане и не можете отправлять сообщения через команду.", ephemeral=True)
            return

        last_used_time = get_last_broadcast_time(user_id)
        current_time = time.time()

        if last_used_time and (current_time - last_used_time) < cooldown_time:
            remaining_time = int((cooldown_time - (current_time - last_used_time)) / 60)
            await interaction.response.send_message(f"Команда была использована недавно. Попробуйте снова через {remaining_time} минут.", ephemeral=True)
        else:
            if type == "Клан":
                modal = ClanModal(bot=self.bot, title="Поиск игроков в клан")
            elif type == "Соло":
                modal = SoloModal(bot=self.bot, title="Поиск тиммейта")
            await interaction.response.send_modal(modal)

    @discord.slash_command(name='news')
    @commands.has_permissions(administrator=True)
    async def broadcast_news_message(self, interaction, *, message):
        user_id = interaction.user.id

        if user_id not in allowed_users:
            await interaction.response.send_message("У вас нет прав для использования этой команды.", ephemeral=True)
            return

        await broadcast_to_all_guilds(interaction, "news_channel", message, "normal", self.bot)

    @discord.slash_command(name='suspend')
    async def ban_user(self, interaction, user_id):
        if interaction.user.id in allowed_users:
            c.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            await interaction.response.send_message(f"Пользователь с ID {user_id} был добавлен в чс.", ephemeral=True)
            logger.debug(f"Пользователь {user_id} забанен для рассылок.")
        else:
            await interaction.response.send_message("❌ Вы не можете сделать это.", ephemeral=True)

    @discord.slash_command(name='unsuspend')
    async def unban_user(self, interaction, user_id):
        if interaction.user.id in allowed_users:
            c.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
            conn.commit()
            await interaction.response.send_message(f"Пользователь с ID {user_id} был удалён из чс.", ephemeral=True)
            logger.debug(f"Пользователь {user_id} разбанен для рассылок.")
        else:
            await interaction.response.send_message("❌ Вы не можете сделать это.", ephemeral=True)

    @discord.Cog.listener()
    async def on_command_error(message: discord.Message) -> None:
        logger.error(f'From team message {message}')

def setup(bot: discord.Bot) -> None:
    bot.add_cog(TeamBroadcast(bot))

