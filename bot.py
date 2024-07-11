import discord
from discord.ext import commands
import os
import logging

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix = '!', intents=intents, help_command=commands.DefaultHelpCommand(no_category='Commands'))

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Use !help for a full list of the avaliable commands.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permission to use this command.")
    else:
        await ctx.send("An error occurred while processing the command.")
        logging.error(f'Error in command {ctx.command}: {error}')


#Loading all the cogs from the cogs directory
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename !='__init__.py':
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run("YOUR_BOT_TOKEN")