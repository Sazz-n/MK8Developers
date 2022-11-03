import psycopg2
from psycopg2.extras import DictCursor
import datetime
import config

dt_jst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
now = str(format(dt_jst,'%Y-%m-%d %H:%M:%S'))

def connectDB(): # DBへの接続

    conn = psycopg2.connect(config.psql)
    cur = conn.cursor(cursor_factory=DictCursor)

    return conn, cur

def closeDB(conn, cur): # DBから切断

    cur.close()
    conn.close()

def commitcloseDB(conn, cur): # コミットして切断

    cur.close()
    conn.commit()
    conn.close()

# ------------------------------ teamdataテーブル ------------------------------
# id(int), guild_id(int), team_name(char(10)), timestamp(ts), last_update(ts) 

def search_GuildID(guild_id):

    conn, cur = connectDB()

    cur.execute(f"SELECT * FROM teamdata WHERE guild_id = '{str(guild_id)}'")
    data = cur.fetchone()

    closeDB(conn, cur)

    if data == None:
        return None
    else:
        return dict(data)

def register_GuildData(team_name, guild_id):

    conn, cur = connectDB()

    cur.execute("SELECT MAX(id) FROM teamdata")
    row = cur.fetchone()[0] + 1
    cur.execute(f"INSERT INTO teamdata (id, guild_id, team_name, timestamp, last_update) VALUES ('{row}', '{guild_id}', '{team_name}', '{now}', '{now}')")

    commitcloseDB(conn, cur)

def update_TeamName(new_team_name, guild_id):

    conn, cur = connectDB()

    cur.execute(f"UPDATE teamdata SET team_name = '{new_team_name}', last_update = '{now}' WHERE guild_id = '{guild_id}'")

    commitcloseDB(conn, cur)

# ------------------------------ wardataテーブル ------------------------------
# id(int), team_name(char(10)), team_score(int), enemy_score(int), enemy_name(char(10)), timestamp(ts)

def register_WarData(team_name, team_score, enemy_score, enemy_name):

    conn, cur = connectDB()

    cur.execute("SELECT MAX(id) FROM wardata")
    row = cur.fetchone()[0] + 1
    cur.execute(f"INSERT INTO wardata (id, team_name, team_score, enemy_score, enemy_name, timestamp) VALUES ('{row}', '{team_name}', '{team_score}', '{enemy_score}', '{enemy_name}', '{now}')")

    commitcloseDB(conn, cur)

# ------------------------------ userdataテーブル ------------------------------
# def search_UserID(conn, cur, user_id):

#     cur.execute(f"SELECT * FROM userdata WHERE user_id = '{str(user_id)}'")
#     data = cur.fetchone()

#     return data

# def register_UserData(conn, cur, user_name, user_id):

#     cur.execute("SELECT MAX(id) FROM userdata")
#     row = cur.fetchone()[0] + 1
#     cur.execute(f"INSERT INTO userdata VALUES ('{row}', '{user_id}', '{user_name}', '{now}')")