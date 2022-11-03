# discordモジュール
import discord
from discord.ext import commands

# configファイル
import config

# インテントの設定
intents = discord.Intents.default()

# Botクラスの定義
class Bot(commands.Bot):

    # コマンドプレフィックス・インテント・アプリケーションIDの設定
    # 読み込むCogの定義
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, application_id=config.application_id)
        self.initial_extensions = ["cogs.pepe", "cogs.team"]
        
    # Cogの読み込み
    # アプリケーションコマンドの同期
    async def setup_hook(self):
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        await bot.tree.sync(guild=discord.Object(id=965811655911022602)) #guild=...は公開時に削除
        
# botインスタンスの生成
bot = Bot()

# botの起動
bot.run(config.TOKEN)