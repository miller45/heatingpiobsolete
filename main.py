#!/usr/bin/env python
import oled
import tempsensors
import relay
import time

print("Starting HeatingPI")

myOled = oled.OLED()
myOled.showSplashScreen()

mySens = tempsensors.TempSensors("28-0317607252ff", "28-051760bdebff")

myRelay = relay.RelayBoard()

rotate = 0

try:
    while True:
        time.sleep(1)
        t1 = float(mySens.read_temperature1())
        t2 = float(mySens.read_temperature2())
        myOled.showTemperatures(t1, t2)
        if rotate == 0:
            myRelay.switchRelay1On()
            rotate = 1
        elif rotate == 1:
            myRelay.switchRelay1Off()
            rotate = 2
        elif rotate == 2:
            myRelay.switchRelay2On()
            rotate = 3
        else:
            myRelay.switchRelay2Off()
            rotate = 0
except:
    myRelay.cleanup()
