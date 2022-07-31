import discord
from discord import app_commands, Embed, Interaction, Object, Color
from discord.app_commands import Choice
from discord.ext import commands
from typing import Optional

color_dic = {
    "red":Color.red(), 
    "blue":Color.blue(), 
    "green":Color.green(), 
    "orange":Color.orange(),
    "purple":Color.purple()
    }

class Basic(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="embed", description="embed(埋め込みテキスト)の作成")
    @app_commands.describe(title="タイトル", description="内容", color="色", author="作者")
    @app_commands.choices(color=[Choice(name=str(i), value=i) for i in color_dic])
    async def makeembed(self, interaction: Interaction, title: str, description: str, color: str = None, author: Optional[discord.Member] = None):
        embed = Embed()
        embed.title = title
        embed.description = description
        if author == None:
            pass
        else:
            embed.set_author(name=author, icon_url=author.display_avatar.url)
        if color == None:
            embed.color = Color.random()
        else:
            embed.color = color_dic[color]
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="ヘルプの表示")
    async def help(self, interaction:Interaction):
        embed = Embed(title="ヘルプ")
        embed.add_field(
            name="制作者",
            value="""
            [fuyuneko](https://twitter.com/wintercatmk8dx)
            [non](https://twitter.com/enoooooooon)
            [sheat](https://twitter.com/sheat_MK)
            [ペペロン](https://twitter.com/PePeroooN27)
            [まいはに～](https://twitter.com/My_hani_)
            """,
            inline=False
            )
        embed.add_field(
            name="GitHub",
            value="[MK8Developers - GitHub](https://github.com/maiha-mk/MK8Developers)",
            inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Basic(bot), guilds=[Object(id=965811655911022602)]) #guildsは公開時に削除