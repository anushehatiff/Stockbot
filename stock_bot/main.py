import discord
from discord.ext import commands
import responses

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")
    await bot.add_cog(responses.Replies(bot))


bot.run("MTEwMjQ1MjY0NzIxNjI5MTk0Mg.GlFyo3.asSM9gSOO0wpgwD3leSrCvCJt-mYh2wg72LHRU")