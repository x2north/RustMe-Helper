import discord
import config_manif as cfg
import os
import json
from discord.ext import commands
import discord.ext as ext
import discord.activity
import discord.ext.tasks

bot = discord.Bot()


for filename in os.listdir('cogs'):
    if filename.endswith('.py') and not filename.startswith('__'):
        bot.load_extension(f'cogs.{filename[:-3]}')        
        
        
def reload_all_extensions(bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            try:
                if extension in bot.extensions:
                    bot.reload_extension(extension)
                    print(f"Reloaded extension: {extension}")
                else:
                    bot.load_extension(extension)
                    print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to reload extension {extension}: {e}")

@ext.tasks.loop(seconds=30)
async def check_reload_trigger():
    try:
        with open("reload_trigger.json", "r") as file:
            data = json.load(file)

        if data.get("reload_cogs", False):
            reload_all_extensions(bot)
            print("All extensions reloaded from JSON trigger.")

            data["reload_cogs"] = False
            with open("reload_trigger.json", "w") as file:
                json.dump(data, file, indent=4)

    except FileNotFoundError:
        print("JSON file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
    except Exception as e:
        print(f"Unexpected error: {e}")

@ext.tasks.loop(seconds=15)
async def presence_change():
    global counter
    if not hasattr(presence_change, "counter"):
        presence_change.counter = True
    
    activity1 = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{len(bot.guilds)} серверов"
    )
    activity2 = discord.Activity(
        type=discord.ActivityType.listening,
        name="/help"
    )
    
    if presence_change.counter:
        await bot.change_presence(activity=activity1)
    else:
        await bot.change_presence(activity=activity2)
    
    presence_change.counter = not presence_change.counter
    


@bot.event
async def on_ready():
    presence_change.start()
    check_reload_trigger.start()

bot.run(f"{cfg.client_token()}")
