# 必要なライブラリのインポート
import cv2
import datetime
import time

# Webカメラを使う
cap=cv2.VideoCapture("./img/sample2.mp4") #一旦動画に
before=None
count=1
fps = int(cap.get(cv2.CAP_PROP_FPS)) #動画のFPSを取得

print("動体検知を開始")
print(str(datetime.datetime.now())) #時刻

while True: #1フレームごと
    ret, frame = cap.read()
    aa=0
    if ret == False:
        break

    # 白黒画像に変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if before is None:
        before = gray.astype("float")
        continue

    # 現在のフレームと移動平均との差を計算
    cv2.accumulateWeighted(gray, before, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(before))

    # frameDeltaの画像を２値化
    thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
    
    # 輪郭のデータを取得
    contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]

    # 差分があった点
    for target in contours :
        x, y, w, h = cv2.boundingRect(target)
        if w < 40:
            continue 

        areaframe = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2) #緑枠で囲む
        aa=1
        if count == 90: #fpsでカウントする 3s=90frame (30fps camera)
            cv2.imwrite("sample.jpg",areaframe)
            print("detected")
            count == 0 #reset


    if aa==1:
        count = count + 1 #1frameごとにカウント？
    

    if cv2.waitKey(1) == 13:break



print("動体検知を終了します")
print(str(datetime.datetime.now()))

# ウィンドウの破棄
#cv2.destroyAllWindows()