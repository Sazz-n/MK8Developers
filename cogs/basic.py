import discord
from discord import app_commands, Embed, Interaction, Object, Color, TextStyle
from discord.ui import Modal, TextInput
from discord.app_commands import Choice
from discord.ext import commands
from typing import Optional
import re

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

    @app_commands.command(name="poll", description="投票の作成")
    async def poll(self, interaction: Interaction):

        await interaction.response.send_modal(Basic.PollModal(bot=self.bot))

    class PollModal(Modal):

        def __init__(self, bot:commands.Bot):
            self.bot = bot
            super().__init__(timeout=None, title="投票の作成")

        daimei = TextInput(label="題名")
        choices = TextInput(label="選択肢 1つにつき1行(最大10個)", style=TextStyle.paragraph)

        async def on_submit(self, interaction: Interaction):

            choice_li = re.split('\n', self.choices.value)

            if len(choice_li) < 11:

                await interaction.response.send_message(embed=Basic.PollEmbed(title=self.daimei.value, choice=choice_li), ephemeral=True)

                msg = await interaction.original_response()
                emoji = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

                for i in choice_li:
                    await msg.add_reaction(emoji[choice_li.index(i)])

            else:

                await interaction.response.send_message("選択肢は10個以内にしてください", ephemeral=True)

    class PollEmbed(Embed):

        def __init__(self, title, choice: list):

            emoji = [":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]
            description = ""

            for i in choice:
                description += f"{emoji[choice.index(i)]} {i}\n"

            super().__init__(color=Color.green(), title=title, description=description)

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