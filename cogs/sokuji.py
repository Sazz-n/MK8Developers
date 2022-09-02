from discord import app_commands, Interaction, Object, Embed, Color, ButtonStyle
from discord.ui import Button, View, Modal, TextInput
from discord.ext import commands

class Sokuji(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.sokujidata = {}
    def place_import(text: str, result: list):
        while text:
            if text.startswith("10"):
                result.append(10)
                text = text[2:]
            elif text.startswith("110"):
                result.extend([1.10])
                text = text[3:]
            elif text.startswith("1112"):
                result.extend([11,12])
                text = text[4:]
            elif text.startswith("111"):
                result.extend([1,11])
                text = text[3:]
            elif text.startswith("112"):
                result.extend([1,12])
                text = text[3:]
            elif text.startswith("11"):
                result.append(11)
                text = text[2:]
            elif text.startswith("12"):
                if 1 in result or 2 in result:
                    result.append(12)
                    text = text[2:]
                else:
                    result.extend([1,2])
                    text = text[2:]
            elif text:
                result.append(int(text[0]))
                text = text[1:]
        if len(result) == 1:
            result.extend([8,9,10,11,12])
        elif len(result) == 2:
            result.extend([9,10,11,12])
        elif len(result) == 3:
            result.extend([10,11,12])
        elif len(result) == 4:
            result.extend([11,12])
        elif len(result) == 5:
            result.extend([12])
        result.sort()

    class SokujiEmbed(Embed):
        def __init__(self, sokujidata, interaction: Interaction):
            super().__init__(color=Color.default(), title="即時集計")
            guild_sokuji = sokujidata[interaction.guild_id]
            team_score_sum = 0
            enemy_score_sum = 0
            try:
                if guild_sokuji["race1"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race1'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="1", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race2"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race2'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="2", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race3"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race3'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="3", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race4"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race4'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="4", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race5"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race5'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="5", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race6"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race6'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="6", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race7"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race7'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="7", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race8"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race8'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="8", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race9"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race9'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="9", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race10"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race10'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="10", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race11"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race11'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="11", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
                if guild_sokuji["race12"]:
                    team_score, enemy_score, text, diff = self.calc_score(guild_sokuji['race12'])
                    team_score_sum += team_score
                    enemy_score_sum += enemy_score
                    self.add_field(name="12", value=f"`{team_score} : {enemy_score}({diff})| {text}`", inline=False)
            except KeyError:
                pass
            diff_sum = team_score_sum - enemy_score_sum
            if diff_sum > 0:
                diff_sum = "+" + str(diff_sum)
            self.insert_field_at(index=0, name=f"vs. {guild_sokuji['enemy']}", value=f"`{team_score_sum} : {enemy_score_sum}({diff_sum})| @{guild_sokuji['races_left']}`", inline=False)
        def calc_score(self, place:list()):
            score_table = [15,12,10,9,8,7,6,5,4,3,2,1]
            team_score = 0
            for i in place:
                team_score += score_table[i-1]
            enemy_score = 82 - team_score
            text = ''.join([str(i) + ' ' for i in place])
            text = text[:-1]
            diff = team_score - enemy_score
            if diff > 0:
                diff = "+" + str(diff)
            return team_score, enemy_score, text, diff

    @app_commands.command(name="sokuji", description="即時の開始")
    async def sokuji(self, interaction: Interaction, enemy: str):
        self.sokujidata[interaction.guild_id] = {}
        self.sokujidata[interaction.guild_id]["races_left"] = 12
        self.sokujidata[interaction.guild_id]["enemy"] = enemy
        self.sokujidata[interaction.guild_id]["original_interaction"] = interaction
        embed = Sokuji.SokujiEmbed(sokujidata=self.sokujidata, interaction=interaction)
        await interaction.response.send_message(embed=embed, view=Sokuji.View(bot=self.bot, sokujidata=self.sokujidata))

    class View(View):
        def __init__(self, bot, sokujidata):
            super().__init__(timeout=None)
            self.add_item(Sokuji.InputButton(bot=bot, sokujidata=sokujidata))
            self.add_item(Sokuji.EditButton(bot=bot, sokujidata=sokujidata))
    
    class InputButton(Button):
        def __init__(self, bot, sokujidata):
            super().__init__(label="順位入力", style=ButtonStyle.red)
            self.bot = bot
            self.sokujidata = sokujidata
        async def callback(self, interaction: Interaction):
            await interaction.response.send_modal(Sokuji.InputModal(bot=self.bot, sokujidata=self.sokujidata))
    
    class EditButton(Button):
        def __init__(self, bot, sokujidata):
            super().__init__(label="修正", style=ButtonStyle.blurple)
            self.bot = bot
            self.sokujidata = sokujidata
        async def callback(self, interaction: Interaction):
            await interaction.response.send_modal(Sokuji.EditModal(bot=self.bot, sokujidata=self.sokujidata))        

    class InputModal(Modal, title="入力"):
        def __init__(self, bot:commands.Bot, sokujidata):
            super().__init__(timeout=None)
            self.bot = bot
            self.sokujidata = sokujidata
            self.place_list = []
        place = TextInput(label="順位", placeholder="例) 123101112", required=True)
        async def on_submit(self, interaction: Interaction):
            Sokuji.place_import(text=self.place.value, result=self.place_list)
            if len(self.place_list) != len(set(self.place_list)):
                await interaction.response.send_message(f"`入力値が正しくありません`:`{self.place.value}`", ephemeral=True)
                return 
            guild_sokujidata = self.sokujidata[interaction.guild_id]
            if int(guild_sokujidata["races_left"]) > 0:
                guild_sokujidata[f"race{13 - guild_sokujidata['races_left']}"] = self.place_list
                guild_sokujidata["races_left"] -= 1
            if int(guild_sokujidata["races_left"]) == 0:
                await guild_sokujidata["original_interaction"].delete_original_response()
                await interaction.response.send_message(embed=Sokuji.SokujiEmbed(sokujidata=self.sokujidata, interaction=interaction))
                return
            embed = Sokuji.SokujiEmbed(sokujidata=self.sokujidata, interaction=interaction)
            await guild_sokujidata["original_interaction"].delete_original_response()
            await interaction.response.send_message(embed=embed, view=Sokuji.View(bot=self.bot, sokujidata=self.sokujidata))
            guild_sokujidata["original_interaction"] = interaction
    
    class EditModal(Modal, title="修正"):
        def __init__(self, bot: commands.Bot, sokujidata):
            super().__init__(timeout=None)
            self.bot = bot
            self.sokujidata = sokujidata
            self.place_list = []
        race_no = TextInput(label="Nレース目", required=True, max_length=2)
        place = TextInput(label="順位", placeholder="例) 123101112", required=True)
        async def on_submit(self, interaction: Interaction):
            guild_sokujidata = self.sokujidata[interaction.guild_id]
            try:
                if guild_sokujidata[f"race{self.race_no}"]:
                    Sokuji.place_import(text=self.place.value, result=self.place_list)
                    guild_sokujidata[f"race{self.race_no}"] = self.place_list
            except KeyError:
                await interaction.response.send_message(f"`入力値が正しくありません`:`{self.race_no.value}`", ephemeral=True)
                return
            if len(self.place_list) != len(set(self.place_list)):
                await interaction.response.send_message(f"`入力値が正しくありません`:`{self.place.value}`", ephemeral=True)
                return 
            embed = Sokuji.SokujiEmbed(sokujidata=self.sokujidata, interaction=interaction)
            await guild_sokujidata["original_interaction"].delete_original_response()
            await interaction.response.send_message(embed=embed, view=Sokuji.View(bot=self.bot, sokujidata=self.sokujidata))
            guild_sokujidata["original_interaction"] = interaction

async def setup(bot:commands.Bot):
    await bot.add_cog(Sokuji(bot), guilds=[Object(id=904976766316187678)]) #guildsは公開時に削除