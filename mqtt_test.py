from umqtt.simple import MQTTClient
from machine import Pin,I2C
from time import sleep
import bme280,ina226,pcf8563
import sys

led=Pin(22,Pin.OUT)

state = 0
def mqtt_cb(topic, msg):
    global state
    print((topic, msg))                                 #如果存在多个订阅时，需要用topic进行区分
    if msg == b"on":
        led.value(1)
        state = 1
    elif msg == b"off":
        led.value(0)
        state = 0
    elif msg == b"toggle":
        state = 1 - state
        led.value(state)
            
iic_int=I2C(1, scl=Pin(14), sda=Pin(12), freq=400000 )
bme280 = bme280.BME280(iic_int)
ina226 = ina226.INA226(iic_int,addr=0x44)
ina226.set_calibration(R_SHUNT=0.08785)
rtc=pcf8563.PCF8563(iic_int)

server = "jniot.xyz"
port=1883
USER="wangshj72"                                        #扇贝物联的注册账户
DEV_ID="wangshj72_environment"                          #设备列表中的设备id
DEV_USER="17"                                           #设备列表中的连接用户
PSWD="ekH4DNA6u"                                        #设备列表中链接密钥          
TOPIC_IO = USER+'/'+DEV_ID
TOPIC_DATA = USER+'/data'
mc = MQTTClient(DEV_ID, server,port,DEV_USER,PSWD,keepalive=10)
                                                        #实例化客户端信息
mc.set_callback(mqtt_cb)                                #配置订阅信息的回调处理函数，没有订阅可以不设置
mc.connect()                                            #执行链接动作，这个动作之后服务器上就可以看到设备上线了
mc.subscribe(TOPIC_IO)                                  #设置订阅IO动作，在服务端开始按钮对应on，停止按钮对应off
while True:
    mc.check_msg()                                      #检查订阅的信息，非阻塞，没有信息就继续，有信息会调用回调
    c=bme280.get()
    i=ina226.read_all()
    print(i)
    Pressure=c[1]/1000
    Temperature=c[0]
    Humidity=c[2]
    batteryV=i[0]
    payload ='{"key":"Temperature", "vlue":"%f"}'%(Temperature)
    mc.publish(TOPIC_DATA,payload)                     #发布数据
    payload ='{"key":"Humidity", "vlue":"%f"}'%(Humidity)
    mc.publish(TOPIC_DATA,payload)
    payload ='{"key":"Pressure", "vlue":"%f"}'%(Pressure)
    mc.publish(TOPIC_DATA,payload)
    payload ='{"key":"batteryV", "vlue":"%f"}'%(batteryV)
    mc.publish(TOPIC_DATA,payload)
    sleep(3)
mc.disconnect()