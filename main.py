import discord
from discord.ext import commands

import config

intents = discord.Intents.default()

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, application_id=997868018828845056)
        self.initial_extensions = ["cogs.basic"]
        
    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        await bot.tree.sync(guild=discord.Object(id=965811655911022602)) #guildは公開時に削除
        
bot = Bot()
bot.run(config.TOKEN)