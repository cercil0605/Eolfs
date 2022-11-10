import matplotlib.pyplot as plt
import cv2

im = cv2.imread("./img/aaa.jpg") #読み込み bgr
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #グレースケール
cv2.imwrite("./img/aaa.jpg", im_gray) #画像にグレースケールを上書き
