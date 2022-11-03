from discord import app_commands, Interaction, Object, Embed, Color, SelectOption
from discord.ui import Modal, TextInput, Select, View
from discord.ext import commands
from .database import psql

class Team(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="team", description="チームの管理")
    async def team(self, interaction: Interaction):
        data = psql.search_GuildID(interaction.guild_id)
        if data == None:
            await interaction.response.send_modal(Team.InfoModal(pre_team_name="", status="Regist"))
        else:
            await interaction.response.send_message(embed=Team.InfoEmbed(data), view=Team.DropdownView(), ephemeral=True)
        
    class InfoEmbed(Embed):
        def __init__(self, data: dict):
            super().__init__(color=Color.red(), title=f"{data['team_name']}")
            self.add_field(name="ID", value=f"{data['id']}", inline=False)
            self.add_field(name="登録日", value=f"{format(data['timestamp'], '%Y-%m-%d')}", inline=False)
            self.set_footer(text=f"最終更新日 : {format(data['last_update'], '%Y-%m-%d')}")
    
    class DropdownView(View):
        def __init__(self):
            super().__init__()
            self.add_item(Team.Dropdown())

    class Dropdown(Select):
        def __init__(self):
            options = [
                SelectOption(label="戦績の登録", emoji="📝"),
                SelectOption(label="チーム情報の編集", emoji="🔧"),
            ]
            super().__init__(placeholder='コマンドを選択', min_values=1, max_values=1, options=options)

        async def callback(self, interaction: Interaction):
            data = psql.search_GuildID(interaction.guild_id)
            if self.values[0] == "チーム情報の編集":
                await interaction.response.send_modal(Team.InfoModal(status="Edit", pre_team_name=data['team_name']))
            elif self.values[0] == "戦績の登録":
                await interaction.response.send_modal(Team.RecordModal(status="Record"))

    class InfoModal(Modal):
        def __init__(self, status, pre_team_name):
            self.status = status
            if status == "Regist":
                super().__init__(title="チーム情報登録フォーム", timeout=600)
                self.team_name = TextInput(label="チーム名(10文字以内)", required=True)
                self.add_item(self.team_name)
            elif status == "Edit":
                super().__init__(title="チーム情報編集フォーム", timeout=600)
                self.team_name = TextInput(label="チーム名(10文字以内)", required=True, default=f"{pre_team_name}")
                self.add_item(self.team_name)
            
        async def on_submit(self, interaction: Interaction):
            if self.status == "Regist":
                psql.register_GuildData(team_name=self.team_name.value, guild_id=interaction.guild_id)
                await interaction.response.send_message("登録が完了しました\n再度`/team`コマンドを使用することでチーム情報を確認できます", ephemeral=True)
            elif self.status == "Edit":
                psql.update_TeamName(new_team_name=self.team_name.value, guild_id=interaction.guild_id)
                await interaction.response.send_message("編集が完了しました\n再度`/team`コマンドを使用することでチーム情報を確認できます", ephemeral=True)

    class RecordModal(Modal):
        def __init__(self, status):
            self.status = status
            if status == "Record":
                super().__init__(title="戦績登録フォーム", timeout=600)
                self.enemy_name = TextInput(label="敵チーム名(10文字以内)", required=True, max_length=10)
                self.team_score = TextInput(label="自チームの点数", required=True)
                self.enemy_score = TextInput(label="敵チームの点数", required=True)
                for item in [self.enemy_name, self.team_score, self.enemy_score]:
                    self.add_item(item)

        async def on_submit(self, interaction: Interaction):
            if self.status == "Record":
                data = psql.search_GuildID(interaction.guild_id)
                team_name = data['team_name']
                psql.register_WarData(team_name=team_name, team_score=self.team_score.value, enemy_name=self.enemy_name.value, enemy_score=self.enemy_score.value)
                await interaction.response.send_message("戦績が登録されました", ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Team(bot), guilds=[Object(id=965811655911022602)]) #guildsは公開時に削除