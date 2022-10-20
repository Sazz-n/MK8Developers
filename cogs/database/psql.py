import psycopg2
import datetime
import config

dt_jst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
now = str(format(dt_jst,'%Y-%m-%d %H:%M:%S'))

def connectDB(): # DBへの接続

    conn = psycopg2.connect(config.psql)
    cur = conn.cursor()

    return conn, cur

def closeDB(conn, cur): # DBから切断

    cur.close()
    conn.close()

def commitcloseDB(conn, cur): # コミットして切断

    cur.close()
    conn.commit()
    conn.close()

# ------------------------------ userdataテーブル ------------------------------
def search_UserID(conn, cur, user_id):

    cur.execute(f"SELECT * FROM userdata WHERE user_id = '{str(user_id)}'")
    data = cur.fetchone()

    return data

def register_UserData(conn, cur, user_name, user_id):

    cur.execute("SELECT MAX(id) FROM userdata")
    row = cur.fetchone()[0] + 1
    cur.execute(f"INSERT INTO userdata VALUES ('{row}', '{user_id}', '{user_name}', '{now}')")

# ------------------------------ teamdataテーブル ------------------------------
def search_GuildID(conn, cur, guild_id):

    cur.execute(f"SELECT * FROM teamdata WHERE guild_id = '{str(guild_id)}'")
    data = cur.fetchone()

    return data

def register_GuildData(conn, cur, team_name, guild_id):

    cur.execute("SELECT MAX(id) FROM teamdata")
    row = cur.fetchone()[0] + 1
    cur.execute(f"INSERT INTO teamdata VALUES ('{row}', '{guild_id}', '{team_name}', '{now}', '{now}')")

def update_TeamName(conn, cur, new_team_name, guild_id):

    cur.execute(f"UPDATE teamdata SET team_name = '{new_team_name}', last_update = '{now}' WHERE guild_id = '{guild_id}'")

# ------------------------------ wardataテーブル ------------------------------     
def register_WarData(conn, cur, team_name, team_score, enemy_score, enemy_name):

    cur.execute("SELECT MAX(id) FROM wardata")
    row = cur.fetchone()[0] + 1
    cur.execute(f"INSERT INTO wardata VALUES ('{row}', '{team_name}', '{team_score}', '{enemy_score}', '{enemy_name}', '{now}')")

    