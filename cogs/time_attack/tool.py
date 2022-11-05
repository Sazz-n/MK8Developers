import math
import warnings
import statistics
import discord

def time_str_arrange(time_str):
    if type(time_str) is float:
        time_str = time_float_to_str(time_str)
    if type(time_str) is int:
        time_str = str(time_str)
    time_str_arranged = time_str[:1] + ":" + time_str[1:3] + "." + time_str[3:]
    return time_str_arranged

  
# 秒数型のタイムをstr型にする。
def time_float_to_str(time_float):
    time_float_min = str(round(time_float//60))
  
    #整数部分と少数部分を取得
    time_float_sec_t = math.modf(round(time_float - float(time_float_min)*60, 3))

    time_ml = str(round(time_float_sec_t[0], 3))[2:]
    time_sec = str(int(time_float_sec_t[1]))

    time_sec_addzero = time_sec.rjust(2, "0")
    time_ml_addzero = time_ml.ljust(3, "0")

  #155678の形式
    time_str = time_float_min + time_sec_addzero + time_ml_addzero

    return time_str

  
# 123456の形式を秒数(float)形式にする
def time_str_to_float(time_str):
    if type(time_str) is int:
        time_str = str(time_str)
      
    if len(time_str) == 6:
        time_min_str = time_str[:1]
        time_sec_str = time_str[1:3]
        time_ml_str = time_str[3:]

        time_min = int(time_min_str)
        time_sec = int(time_sec_str)
        time_ml = int(time_ml_str)

        time_float = round(time_min*60 + time_sec + time_ml/1000, 3)
    
        return time_float

    else:
        warnings.warn("Tool.time_str_to_float関数の因数が6桁のタイムではありません。")
        return None

      
# ユーザーのタイムとベースのタイムから秒差、落ち、○落ちに対応したDiscordのスタンプを取得する。
def get_diff_fall_circle(user_time, base_time):
    diff = get_diff(user_time, base_time)
    fall = get_fall(diff)
    circle = get_circle(fall)
    return diff, fall, circle


# diffから○落ちを計算する
def get_fall(diff):
    fall = math.ceil(diff)
    return fall

  
# ○落ちから色のついた円のスタンプを取得する
def get_circle(diff):
    fall = math.ceil(diff)
    circle = ':red_circle:'
    if fall == 1:
        circle = ':red_circle:'
    if fall == 2:
        circle = ':yellow_circle:'
    if fall == 3:
        circle = ':green_circle:'
    if fall > 3 and fall <= 5:
        circle = ':blue_circle:'
    if fall > 5:
        circle = ':white_circle:'
    return circle


# user_timeとbase_timeから差を計算する
# base_time ...... WR
def get_diff(user_time, base_time):
    if type(user_time) is str:
        user_time = time_str_to_float(user_time)
    if type(base_time) is str:
        base_time = time_str_to_float(base_time)

    diff = round(user_time - base_time, 3)
    return diff


def update_user_course_time(row:int, record:str, course_index:int, worksheet:object):
    worksheet.update_cell(row, course_index+3, record)

def id_split(user_id):
    if type(user_id) is int:
        user_id = str(user_id)
          
    id_split = [user_id[:9], user_id[9:]]

        #0から始まる場合、最初に"a"を足す
    if id_split[1].startswith("0"):
        id_split[1] = "a" + id_split[1]

    user_id_1 = id_split[0]
    user_id_2 = id_split[1]

    return user_id_1, user_id_2

def get_user_longuage(user_row:int, record_wks_data: list):
    cell_str = record_wks_data[user_row-1][100]
    user_language = "jpn"
    if cell_str == "" or cell_str == "c_jpn":
        user_language = "jpn"
    elif cell_str == "c_eng":
        user_language = "eng"
    return user_language
    
  
# -> #0xのついたintかstr型の6桁の数字
def get_color(number_with_0x):
    if type(number_with_0x) is int:
        number_with_0x = hex(number_with_0x)
    if len(number_with_0x) < 8:
        while len(number_with_0x) < 8:
            number_with_0x = number_with_0x[:2] + "0" + number_with_0x[2:]
    R = int(number_with_0x[2:4], 16)
    G = int(number_with_0x[4:6], 16)
    B = int(number_with_0x[6:8], 16)
    try:
        color = discord.Colour.from_rgb(R, G, B)
        return color
    except:
        return None
    



class LoungeRank:
    def __init__(self, rank_name: str =None, mmr: int =None):
        if rank_name != None:
            if rank_name.startswith("i") or rank_name.startswith("I"):
                rank = "Iron"
                min_mmr = 0
                max_mmr = 2000
                color = 0x817876
                nita_row = 8
                ta_row = 13
            elif rank_name.startswith("b") or rank_name.startswith("B"):
                rank = "Bronze"
                min_mmr = 2000
                max_mmr = 4000
                color = 0xb45f06
                nita_row = 9
                ta_row = 14
            elif rank_name.startswith("s") or rank_name.startswith("S") and not rank_name.startswith("sa") and not rank_name.startswith("Sa"):
                rank = "Silver"
                min_mmr = 4000
                max_mmr = 6000
                color = 0xcccccc
                nita_row = 10
                ta_row = 15
            elif rank_name.startswith("g") or rank_name.startswith("G"):
                rank = "Gold"
                min_mmr = 6000
                max_mmr = 8000
                color = 0xf1c232
                nita_row = 11
                ta_row = 16
            elif rank_name.startswith("p") or rank_name.startswith("P"):
                rank = "Platinum"
                min_mmr = 8000
                max_mmr = 10000
                color = 0x3fabb8
                nita_row = 12
                ta_row = 17
            else:
                rank = None
                min_mmr = None
                max_mmr = None
                rank_div = None
                color = None
                nita_row = None
                ta_row = None
            if rank != None:
                if rank_name.endswith("1"):
                    rank_div = 1
                    max_mmr -= 1000
                elif rank_name.endswith("2"):
                    rank_div = 2
                    min_mmr += 1000
                else:
                    rank_div = ""

            self.rank = rank
            if rank != None:
                self.rank_name = rank + str(rank_div)
            else:
                self.rank_name = None
            self.rank_div = rank_div
            self.min_mmr = min_mmr
            self.max_mmr = max_mmr
            self.color = color
            self.ta_row = ta_row
            self.nita_row = nita_row
      
        elif mmr != None:
            if 0 <= mmr and mmr < 1000:
                rank = "Iron"
                min_mmr = 0
                max_mmr = 1000
                rank_div = 1
                color = 0x817876
                nita_row = 8
                ta_row = 13
            elif 1000 <= mmr and mmr < 2000:
                rank = "Iron"
                min_mmr = 1000
                max_mmr = 2000
                rank_div = 2
                color = 0x817876
                nita_row = 8
                ta_row = 13
            elif 2000 <= mmr and mmr < 3000:
                rank = "Bronze"
                min_mmr = 2000
                max_mmr = 3000
                rank_div = 1
                color = 0xb45f06
                nita_row = 9
                ta_row = 14
            elif 3000 <= mmr and mmr < 4000:
                rank = "Bronze"
                min_mmr = 3000
                max_mmr = 4000
                rank_div = 2
                color = 0xb45f06
                nita_row = 9
                ta_row = 14
            elif 4000 <= mmr and mmr < 5000:
                rank = "Silver"
                min_mmr = 4000
                max_mmr = 5000
                rank_div = 1
                color = 0xcccccc
                nita_row = 10
                ta_row = 15
            elif 5000 <= mmr and mmr < 6000:
                rank = "Silver"
                min_mmr = 5000
                max_mmr = 6000
                rank_div = 2
                color = 0xcccccc
                nita_row = 10
                ta_row = 15
            elif 6000 <= mmr and mmr < 7000:
                rank = "Gold"
                min_mmr = 6000
                max_mmr = 7000
                rank_div = 1
                color = 0xf1c232
                nita_row = 11
                ta_row = 16
            elif 7000 <= mmr and mmr < 8000:
                rank = "Gold"
                min_mmr = 7000
                max_mmr = 8000
                rank_div = 2
                color = 0xf1c232
                nita_row = 11
                ta_row = 16
            elif 8000 <= mmr and mmr < 9000:
                rank = "Platinum"
                min_mmr = 8000
                max_mmr = 9000
                rank_div = 1
                color = 0x3fabb8
                nita_row = 12
                ta_row = 17
            elif 9000 <= mmr and mmr < 10000:
                rank = "Platinum"
                min_mmr = 9000
                max_mmr = 10000
                rank_div = 2
                color = 0x3fabb8
                nita_row = 12
                ta_row = 17
            else:
                rank = None
                min_mmr = None
                max_mmr = None
                rank_div = None
                color = 0x286CD3
                row = None

            self.rank = rank
            self.rank_name = rank + str(rank_div)
            self.rank_div = rank_div
            self.min_mmr = min_mmr
            self.max_mmr = max_mmr
            self.color = color

        else:
            self.rank = None
            self.rank_name = None
            self.rank_div = None
            self.min_mmr = None
            self.max_mmr = None
            self.color = None
          
    def get_row_and_mmr_dict(self, record_wks_data: list):
        row_and_mmr_dict = {}
        for index, user_data_l in enumerate(record_wks_data):
            user_mmr = user_data_l[99].replace("c_", "")
            if user_mmr != "" and user_mmr != "none":
                user_mmr = int(user_mmr)
                if self.min_mmr <= user_mmr and self.max_mmr > user_mmr:
                    row = index + 1
                    row_and_mmr_dict[row] = user_mmr
        return row_and_mmr_dict

    def get_course_avarage_time_and_average_mmr(self, course_index: int, record_wks_data: list):
        row_and_mmr_dict = self.get_row_and_mmr_dict(record_wks_data=record_wks_data)
        if len(row_and_mmr_dict) != 0:
            row_l = list(row_and_mmr_dict.keys())
            course_time_l = []
            mmr_l = []
            for row in row_l:
                user_data_l = record_wks_data[row-1]
                course_time = user_data_l[course_index+2]
                if course_time != "":
                    course_time_l.append(course_time)
                    mmr_l.append(row_and_mmr_dict[row])
            if len(course_time_l) != 0:
                  
                course_time_float_l = [time_str_to_float(i) for i in course_time_l]
                course_average_time_float = statistics.mean(course_time_float_l)
                course_average_time_str = time_float_to_str(course_average_time_float)
                average_mmr = round(statistics.mean(mmr_l), 1)
                data_n = len(course_time_l)
                return course_average_time_str, average_mmr, data_n
            else:
                return None
        else:
            return None


