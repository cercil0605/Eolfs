from bluepy.btle import Scanner, DefaultDelegate
import json
import datetime

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            data= {
                "date": str(datetime.datetime.now()).replace(" ","_").replace(":", "-"),
                "address": str(dev.addr)
            }
            data_json=open("test.json","a")
            json.dump(data,data_json,indent=2)
            data_json.write("\n")
            print("Discovered device", dev.addr)
            
        elif isNewData:
            print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print("  %s = %s" % (desc, value))