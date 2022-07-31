from discord import app_commands, Embed, Interaction, Object
from discord.ext import commands

class Basic(commands.Cog):
    
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