import json
import datetime 
import bluepy
#make json data format
#[
#{"time": time(str), "address": address(bluetooth)},
#{"time": time2(str), "address": address2(bluetooth)}
#]

scanner = bluepy.btle.Scanner(0)
devices=scanner.scan(3)
f=open("samplefile.txt","a")
f.write("======================================================\n")
f.write("time"+" "+"address\n")

for device in devices:
  str_dt=str(datetime.datetime.now()).replace(" ","_").replace(":", "-")
  #print('address : %s' % device.addr)
  #print('addrType: %s' % device.addrType)
  #print('RSSI    : %s' % device.rssi)
  #print('Adv data:')
  f.write("{} {}\n".format(str_dt,str(device.addr)))
  #for (adtype, desc, value) in device.getScanData():
    #print(' (%3s) %s : %s ' % (adtype, desc, value))