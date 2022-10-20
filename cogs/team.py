from discord import app_commands, Interaction, Object, Embed, Color, SelectOption
from discord.ui import Modal, TextInput, Select, View
from discord.ext import commands
from .database import psql

class Team(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="team", description="チームの管理")
    async def team(self, interaction: Interaction):

        conn, cur = psql.connectDB()
        data = psql.search_GuildID(conn, cur, interaction.guild_id)
        psql.closeDB(conn, cur)

        if data:
            await interaction.response.send_message(embed=Team.InfoEmbed(data), view=Team.DropdownView(), ephemeral=True)
        else:
            await interaction.response.send_modal(Team.Modal(d_team_name="", status="Regist"))
        
    class InfoEmbed(Embed):
        
        def __init__(self, data):
            super().__init__(color=Color.red(), title=f"{data[2]}")

            self.add_field(name="ID", value=f"{data[0]}", inline=False)
            self.add_field(name="登録日", value=f"{format(data[3], '%Y-%m-%d')}", inline=False)
            self.set_footer(text=f"Last Update:{format(data[4], '%Y-%m-%d')}")
    
    class Dropdown(Select):
        def __init__(self):
            
            options = [
                SelectOption(label="チーム情報の編集", emoji="📝"),
                SelectOption(label="チームの削除", emoji="⛔"),
                SelectOption(label="バグ報告・意見箱")
            ]

            super().__init__(placeholder='コマンドを選択', min_values=1, max_values=1, options=options)

        async def callback(self, interaction: Interaction):
            
            conn, cur = psql.connectDB()
            data = psql.search_GuildID(conn, cur, interaction.guild_id)
            psql.closeDB(conn, cur)

            if self.values[0] == "チーム情報の編集":

                await interaction.response.send_modal(Team.Modal(d_team_name=data[2], status="Edit"))

            elif self.values[1] == "チームの削除":

                pass

            elif self.values[2] == "バグ報告・意見箱":

                pass


    class DropdownView(View):

        def __init__(self):
            super().__init__()

            self.add_item(Team.Dropdown())

    class Modal(Modal):

        def __init__(self, d_team_name, status):

            self.status = status

            if status == "Regist":

                super().__init__(title="チーム情報登録フォーム", timeout=600)

                self.team_name = TextInput(label="チーム名(10文字以内)")

                self.add_item(self.team_name)
            
            elif status == "Edit":

                super().__init__(title="チーム情報編集フォーム", timeout=600)

                self.team_name = TextInput(label="チーム名(10文字以内)", default=f"{d_team_name}")

                self.add_item(self.team_name)
            
        async def on_submit(self, interaction: Interaction):
            
            if self.status == "Regist":

                conn, cur = psql.connectDB()
                psql.register_GuildData(conn, cur, team_name=self.team_name.value, guild_id=interaction.guild_id)
                psql.commitcloseDB(conn, cur)

                await interaction.response.send_message("登録が完了しました\n再度`/team`コマンドを使用することでチーム情報を確認できます", ephemeral=True)

            elif self.status == "Edit":

                conn, cur = psql.connectDB()
                psql.update_TeamName(conn, cur, new_team_name=self.team_name.value, guild_id=interaction.guild_id)
                psql.commitcloseDB(conn, cur)

                await interaction.response.send_message("編集が完了しました\n再度`/team`コマンドを使用することでチーム情報を確認できます", ephemeral=True)

async def setup(bot:commands.Bot):

    await bot.add_cog(Team(bot), guilds=[Object(id=965811655911022602)]) #guildsは公開時に削除