from discord import app_commands, Interaction, Object, SelectOption
from discord.ui import View, Select
from discord.ext import commands
from .database import psql

class Mogi(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="mogi", description="模擬戦メニュー")
    async def mogi(self, interaction: Interaction):
        data = psql.search_GuildID(interaction.guild_id)
        if data == None:
            await interaction.response.send_message("チーム登録が行われていません\n`/team`コマンドでチーム登録を行ってください", ephemeral=True)
        else:
            await interaction.response.send_message(view=Mogi.DropdownView(), ephemeral=True)
            pass

    class DropdownView(View):
        def __init__(self):
            super().__init__()
            self.add_item(Mogi.Dropdown())

    class Dropdown(Select):
        def __init__(self):
            options = [
                SelectOption(label="カジュアルマッチ", emoji="👥", description="対戦相手を募集もしくは選択して模擬戦を行います"),
                SelectOption(label="6v6ランクマッチ", emoji="⚔️", description="coming soon..."),
            ]
            super().__init__(placeholder='マッチを選択', min_values=1, max_values=1, options=options)

        async def callback(self, interaction: Interaction):
            if self.values[0] == "ランダムマッチ":
                await interaction.response.send_message("coming soon...", ephemeral=True)
            elif self.values[0] == "6v6ランクマッチ":
                await interaction.response.send_message("coming soon...", ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Mogi(bot), guilds=[Object(id=965811655911022602)]) #guildsは公開時に削除