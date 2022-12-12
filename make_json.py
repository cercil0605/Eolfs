import json
import datetime 
import bluepy

scanner = bluepy.btle.Scanner(0) #init
devices=scanner.scan(3) #scan 3sec
f=open("samplefile.txt","a") #begin file write 上書きmode
f.write("======================================================\n")
f.write("time"+"                       "+"address\n") #時間 アドレス 必要であればRSSI（電波強度）

for device in devices: #3s検知開始
  str_dt=str(datetime.datetime.now()).replace(" ","_").replace(":", "-")
  #print('address : %s' % device.addr)
  #print('addrType: %s' % device.addrType)
  #print('RSSI    : %s' % device.rssi)
  #print('Adv data:')
  f.write("{} {}\n".format(str_dt,str(device.addr)))
  #for (adtype, desc, value) in device.getScanData():
    #print(' (%3s) %s : %s ' % (adtype, desc, value))

f.close()