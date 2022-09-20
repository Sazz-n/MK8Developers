from discord import app_commands, Interaction, Object, Attachment
from discord.ext import commands
from .peperon import makeScoreTable

class Pepe(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="upload", description="リザルトの読み込み")
    async def upload(self, interaction: Interaction, attachment: Attachment):
        await interaction.response.defer(thinking=False, ephemeral=True)
        checkFlag, img = makeScoreTable.checkInputImgSize(attachment)
        if checkFlag:
            msg, pointListMsg, checkFlag = makeScoreTable.main(img, attachment)
            if checkFlag:
                await interaction.followup.send(f"`{pointListMsg}`\n{msg}", ephemeral=True)
        else:
            await interaction.followup.send(f"```画像から得点を読み取れませんでした```", ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Pepe(bot), guilds=[Object(id=965811655911022602)]) #guildsは公開時に削除