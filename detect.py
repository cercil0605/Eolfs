# 必要なライブラリのインポート
import cv2
import datetime
import time
import zipfile
import requests
import bluepy
def scan_func(devices_n,filename): #scan devices func (not tested)
    f=open("text/"+str(filename)+".txt","w") #begin file write 上書きmode
    f.write("======================================================\n")
    f.write("time"+"                       "+"address\n") #時間 アドレス 必要であればRSSI（電波強度）

    for device in devices_n: #3s検知開始
        str_dt=str(datetime.datetime.now()).replace(" ","_").replace(":", "-")
        f.write("{} {}\n".format(str_dt,str(device.addr)))
    
    f.write("======================================================")
    f.close()
    

# Webカメラを使う
cap = cv2.VideoCapture(-1) #一旦動画に
before=None
count=1
fps = int(cap.get(cv2.CAP_PROP_FPS)) #動画のFPSを取得
url="https://os3-380-23410.vs.sakura.ne.jp/api/v1/records"
data={''}
size=(640,480) #画面サイズ
flaging=1
#録画
fourcc=cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#detect bluetooth
scanner=bluepy.btle.Scanner(0)
devices=scanner.scan(3)


print("Begin Human Detect")
print(str(datetime.datetime.now())) #時刻

while (True): #1フレームごと
    ret, frame = cap.read()
    #print(type(cap))
    # <class 'cv2.VideoCapture'>
    #print(cap.isOpened())
    aa=0
    if ret == False:
        break

    # grayscale
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

    # 差分
    for target in contours :
        x, y, w, h = cv2.boundingRect(target)
        if w < 120 and h < 120 : #感度調整を現場で行う w　横　h 高さ
            continue 
        areaframe = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2) #緑枠で囲む
        aa=1
        


    if aa==1:
        
        if flaging==1:
            str_dt=str(datetime.datetime.now()).replace(" ","_").replace(":", "-")
            scan_func(devices,str_dt) #ここで導入してみる
            video=cv2.VideoWriter("img/"+str_dt+".mp4",fourcc,fps,size)
            flaging=0

        video.write(frame) #video capture begin

        if count==90: #fpsでカウントする 3s=90frame (30fps camera)
            zip=zipfile.ZipFile("file/"+str_dt+".zip","w") #make zip
            video.release() #save video
            zip.write("img/"+str_dt+".mp4",compress_type=zipfile.ZIP_DEFLATED) #add mp4 to zip
            zip.write("text/"+str_dt+".txt",compress_type=zipfile.ZIP_DEFLATED) #add text to zip
            zip.close()

            file={
                'file1':open ("file/"+str_dt+".zip","rb")
            } #send file
            res = requests.post(url,files=file)
            print(res)

            print("detected")
            #time.sleep(10) #sleep 10sec ここが怪しい10s待ててる？
            count == 0 #reset
            break  #一旦抜ける
        else:
             count = count + 1 #1frameごとにカウント？
    

    #if cv2.waitKey(1) == 13:break #press enter 



print("End Human Detect")
print(str(datetime.datetime.now()))