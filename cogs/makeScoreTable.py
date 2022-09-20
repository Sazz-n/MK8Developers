import cv2
import requests

pointImageSize_type1 = [23,30]
pointImage_left_type1 = [518,542,566]
pointImage_top_type1 = [135,177,219,261,303,345,387,429,471,514,555,597]
numberCheckPoint_type1 = [[10,3],[3,9],[17,9],[10,15],[3,21],[17,21],[10,27],[9,9],[9,21]]

pointImageSize_type2 = [17,22]
pointImage_left_type2 = [1166,1184,1201]
pointImage_top_type2 = [67,118,170,223,275,326,378,431,483,534,586,639]
numberCheckPoint_type2 = [[8,2],[2,6],[13,6],[8,11],[2,16],[13,16],[8,20],[8,6],[8,16]]

numberIdentity = [ [1,1,1,0,1,1,1,0,0],
                   [0.5,0,0,0.5,0,0,0.5,1,1],
                   [1,0,1,1,1,0,1,0,0],
                   [1,0,1,1,0,1,1,0,0],
                   [0,1,1,1,0,1,0,0,0],
                   [1,1,0,1,0,1,1,0,0],
                   [1,1,0,1,1,1,1,0,0],
                   [1,0,1,0,0,1,0,0,0],
                   [1,1,1,1,1,1,1,0,0],
                   [1,1,1,1,0,1,1,0,0],
                   [0,0,0,0,0,0,0,0,0] ]

def getImg(imageURL,filename):
    r = requests.get(imageURL, stream = True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)

    img = cv2.imread(filename)
    h, w, _ = img.shape
    return h, w, img

def ImgBinarize(img,THRESHOLD_VALUE):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img[gray < THRESHOLD_VALUE] = 0
    img[gray >= THRESHOLD_VALUE] = 255
    return img

def ImgTrim(img,left,right,top,bottom):
    return img[top:bottom,left:right]

def BackColor(img, imgType):
    pis = pointImageSize_type1
    if imgType == 1:
        pis = pointImageSize_type1
    elif imgType == 2:
        pis = pointImageSize_type2

    black = 0
    white = 0
    for i in range(pis[1]):
        if img[i,pis[0]-1][0] == 255:
            white += 1
        elif img[i,pis[0]-1][0] == 0:
            black += 1
    if black > white:
        return "black"
    else:
        return "white"

def ColorInvers(img):
    THRESHOLD_VALUE = 150#グレースケールの閾値

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img[gray < THRESHOLD_VALUE] = 255
    img[gray >= THRESHOLD_VALUE] = 0
    return img

def numberJudge(img, imgType):
    ncp = numberCheckPoint_type1
    if imgType == 1:
        ncp = numberCheckPoint_type1
    elif imgType == 2:
        ncp = numberCheckPoint_type2

    numberDigit = [0] * 9
    for i in range(len(ncp)):
        if img[ncp[i][1],ncp[i][0]][0] == 255:
            numberDigit[i] = 1

    number = -1
    for i in range(len(numberIdentity)):
        flag = True
        count = 0
        for j in range(len(ncp)):
            if abs(numberIdentity[i][j] - numberDigit[j]) == 1:
                flag = False

        if flag:
            number = i
            break
    return number


def imgTypeJudge(img, msg):#
    if msg == "p":#
        type = 1#
    elif msg == "pp":#
        type = 2#
    else:#
        type = 1
        red = [0,0,200]
        buffer = 30
        count = 0
        for i in range(20):
            for j in range(3):
                if red[j] - 30 <= img[0,i][j] and img[0,i][j] <= red[j] + 30:
                    count += 1
        if count >= 18 * 3:
            type = 1
        else:
            type = 2
    return type

def getPointList(imgPath, msg):#
    originalImg = cv2.imread(imgPath)
    imgType = imgTypeJudge(originalImg, msg)

    pi_l = pointImage_left_type1
    pis = pointImageSize_type1
    pi_t = pointImage_top_type1
    if imgType == 1:
        pi_l = pointImage_left_type1
        pis = pointImageSize_type1
        pi_t = pointImage_top_type1
    elif imgType == 2:
        pi_l = pointImage_left_type2
        pis = pointImageSize_type2
        pi_t = pointImage_top_type2

    number = [ [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    TVALUE_list = [120,140,160,180]

    k = 0
    for i in range(12):
        for j in range(3):
            numberCount = [-1]*10
            for k in range(len(TVALUE_list)):
                img_k = cv2.imread(imgPath)
                img_k = cv2.resize(img_k,(1280,720))
                if imgType == 1:
                    img_k = ImgTrim(img_k,pointImage_left_type1[j],pointImage_left_type1[j]+pointImageSize_type1[0], pointImage_top_type1[i],pointImage_top_type1[i]+pointImageSize_type1[1])
                elif imgType == 2:
                    img_k = ImgTrim(img_k,pointImage_left_type2[j],pointImage_left_type2[j]+pointImageSize_type2[0], pointImage_top_type2[i],pointImage_top_type2[i]+pointImageSize_type2[1])

                img_k = ImgBinarize(img_k,TVALUE_list[k])

                if BackColor(img_k, imgType) == "white":
                    img_k = ColorInvers(img_k)

                num = numberJudge(img_k, imgType)
                if 0 <= num and num <= 9:
                    numberCount[num] += 1

            Max = max(numberCount)
            for k in range(len(numberCount)):
                if numberCount[k] == Max:
                    number[i][j] = k
                    break

    for i in range(12):
        if number[i][0] == 0:
            number[i][0] = 10
            if number[i][1] == 0:
                number[i][1] = 10

    errorCount = 0
    pointList_str = []
    for i in range(12):
        point_str = ""
        for j in range(3):
            if number[i][j] == -1:
                point_str += "?"
                errorCount += 1
            elif number[i][j] == 10:
                point_str += ""
                errorCount += 1
            else:
                point_str += str(number[i][j])
        pointList_str.append(point_str)

    return pointList_str, errorCount, imgType

def ranksFormCheck(ranksForm):
    ranksForm = ranksForm.replace("a","10").replace("b","11").replace("c","12")
    ranksCheckFlag = True
    #ポイントの値チェック
    ranks = []
    if ranksForm.isdigit():
        if 6 <= len(ranksForm) and len(ranksForm) <= 9:
            digit2Num = len(ranksForm)-6
            for i in range(6-digit2Num):
                ranks.append(int(ranksForm[i]))
            for i in range(digit2Num):
                ranks.append(int(ranksForm[6-digit2Num+2*i] + ranksForm[6-digit2Num+2*i+1]))

            if len(ranks) != 6:
                ranksCheckFlag = False
            for i in range(len(ranks)):
                if ranks[i] <= 0 or 13 <= ranks[i]:
                    ranksCheckFlag = False
                for j in range(i+1,len(ranks)):
                    if ranks[i] >= ranks[j]:
                        ranksCheckFlag = False
        else:
            ranksCheckFlag = False
    else:
        ranksCheckFlag = False
    return ranksCheckFlag

def checkInputImgSize(attachment):
    checkFlag = False
    inputImgURL = attachment.url
    h ,w ,inputImg = getImg(inputImgURL, "ky.png")
    if 1.77 < w/h and w/h < 1.80 and w > 500:
        checkFlag = True
    return checkFlag, inputImg

def main(img, attachment):
    checkFlag = True
    msg = ""
    pointListMsg = ""
    img = cv2.resize(img,(1280,720))
    imgPath = "ky.png"
    cv2.imwrite(imgPath,img)
    pointList_str, errorCount, imgType = getPointList(imgPath, attachment)#

    fullURL = attachment.url
    splittedFullURL = fullURL.split("/")
    RIimageName = splittedFullURL[6]
    if len(RIimageName) < 60:
        if errorCount < 24:
            totalPoint = 0
            NANflag = False
            pointListMsg = ""
            for i in range(len(pointList_str)):
                pointListMsg += pointList_str[i] + " "
                if pointList_str[i].isdigit():
                    totalPoint += int(pointList_str[i])
                else:
                    NANflag = True

            msg = "```\n得点を読み取りました\n"
            if NANflag:
                msg += "❗ '?'は読み取れなかった数字です\n"
            if totalPoint != 984:
                msg += "❗ 得点の合計が984点ではありません(" + str(984-totalPoint) + "点足りません)\n"
            else:
                msg += "読み取った得点の合計は" + str(totalPoint) + "です\n"
            msg += "```"

            #DBへの登録
            status = "makeScoreTable"

        else:
            msg = "```\n画像から得点を読み取れませんでした\n```"
            checkFlag = False
    else:
        msg = "```\nファイル名が長すぎます。30文字以内に変更して再アップロードしてください。\n```"
        checkFlag = False
    return msg, pointListMsg, checkFlag