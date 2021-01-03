import sys
import os,network
import machine
import socket
import time
from machine import I2C,Pin
ctl_pow=Pin(19,Pin.OUT)
ctl_pow.on()
#ctl_pow.pull(Pin.PULL_HOLD)
led_pow=Pin(22,Pin.OUT)
led_wifi=Pin(23,Pin.OUT)
led_pow.on()
led_wifi.off()
sys.path[1] = '/flash/lib'
SSID="15-3-201"
PASSWORD="1234567890abc"
wlan=None
def connectWifi(ssid,passwd):
  global wlan
  cnt=0
  print("Start Wifi  NIC.")
  wlan=network.WLAN(network.STA_IF)                     #create a wlan object
  wlan.active(True)                                     #Activate the network interface
  print()
  print("Connect Wifi.",end="")
  wlan.disconnect()                                     #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                             #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    led_wifi.off()
    time.sleep(0.2)
    led_wifi.on()
    time.sleep(0.3)
    print(".",end="")
  led_wifi.on()  
  print(" OK.")
  print("IP ADDR:",wlan.ifconfig())  
  print()
  print()  
  return True
#time.sleep(2)
led_wifi.on()
connectWifi(SSID,PASSWORD)



