import json
from datetime import datetime
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

def get_next_event(event_type="next", day_of_week=None):
    with open('configs/wipes.json', 'r', encoding='utf-8') as file:
        events = json.load(file)

    today = datetime.today()

    if event_type == "Глобальный":
        future_events = [event for event in events if event["name"] == "ГЛОБАЛЬНЫЙ ВАЙП" and datetime.strptime(event["date"], "%Y-%m-%d") > today]
    else:
        future_events = [event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") > today]

    if day_of_week:
        future_events = [event for event in future_events if datetime.strptime(event['date'], "%Y-%m-%d").strftime("%A").lower() == day_of_week.lower()]

    future_events.sort(key=lambda event: datetime.strptime(event["date"], "%Y-%m-%d"))

    if future_events:
        return future_events[0]
    return None
    

class Wipes(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.slash_command()
    async def wipe(self, interaction, 
                   type: discord.Option(str, "Выберите тип вайпа для поиска.", choices=['Глобальный', 'Следующий'], name="тип"),
                   day: discord.Option(str, "Укажите день недели (например: пятница, понедельник)", name="день", choices=['Пятница', 'Понедельник'])) -> None: # type: ignore
        match day:
            case 'Пятница':
                day = 'Friday'
            case 'Понедельник':
                day = 'Monday'
        
        
        nearest_event = get_next_event(type, day)
        if nearest_event:
            event_date = datetime.strptime(nearest_event['date'], "%Y-%m-%d")
            day_of_week = event_date.strftime("%A")

            embed = discord.Embed(description=f"Следующий {nearest_event['name']} пройдет **{nearest_event['date']}** (**{day_of_week}**)", color=discord.Colour.green())
            if nearest_event['blueprints'] is False:
                embed.description += "\nИзучения **не сохраняются**"
            else:
                embed.description += "\nИзучения **сохраняются**"
        else:
            embed = discord.Embed(description="Не найдено вайпов для указанного дня недели.", color=discord.Colour.red())
            logger.error(f"Не найдено вайпов для {day}! Обновите таблицу configs/wipes.json")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user.name} использовал график вайпов с типом {type} на {day}.")

def setup(bot: discord.Bot) -> None:
    bot.add_cog(Wipes(bot))
