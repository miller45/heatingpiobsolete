import oled
import tempsensors
import relay
import time
import mqttcom
import configparser
import math

print("Starting HeatingPI V0.2")

hpConfig = configparser.ConfigParser()
hpConfig.read("config.ini")

myOled = oled.OLED()
myOled.showSplashScreen()

mySens = tempsensors.TempSensors("28-3c01f0964f8c", "28-3c01f0965e56")
# mySens = tempsensors.TempSensors("28-0317607252ff", "28-051760bdebff")

relayBoard = relay.RelayBoard()

mqttClient = mqttcom.MQTTComm(hpConfig["mqtt"]["server_address"], hpConfig["mqtt"]["base_topic"])

mqttClient.ping()
pollPeriod = int(hpConfig["control"]['poll_period'])
MQTTSpamPeriod = int(hpConfig["mqtt"]['tele_period'])

rotate = 0
lstateCounter = 0
ltime = 0
spamltime = 0
t1 = -99
t2 = -99

try:
    while True:
        currtime = math.trunc(time.time() * 1000)  # time in microseconds
        if currtime - pollPeriod > ltime:
            ltime = currtime
            t1 = float(mySens.read_temperature1())
            t2 = float(mySens.read_temperature2())
            myOled.showTemperatures(t1, t2)
        if currtime - MQTTSpamPeriod > spamltime:
            spamltime = currtime
            mqttClient.sendTemperature("T1", t1)
            mqttClient.sendTemperature("T2", t2)
        if lstateCounter != mqttClient.stateCounter:
            lstateCounter = mqttClient.stateCounter
            if mqttClient.relay1State:
                relayBoard.switchRelay1On()
            else:
                relayBoard.switchRelay1Off()
            if mqttClient.relay2State:
                relayBoard.switchRelay2On()
            else:
                relayBoard.switchRelay2Off()
            if mqttClient.relay3State:
                relayBoard.switchRelay3On()
            else:
                relayBoard.switchRelay3Off()

except:
    relayBoard.cleanup()
