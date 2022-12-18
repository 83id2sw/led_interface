from time import sleep
import os, sys
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import urlparse3


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT) #green led
GPIO.setup(8, GPIO.OUT) #red led
GPIO.setup(5, GPIO.OUT) #blue led

pwmRed = GPIO.PWM(8, 500)
pwmRed.start(0)

pwmGreen = GPIO.PWM(6, 500)
pwmGreen.start(0)

pwmBlue = GPIO.PWM(5, 500)
pwmBlue.start(0)


def on_connect(self, mosq, obj, ec):
    self.subscribe("Hello_topic", 0)


def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    h = str(msg.payload).lstrip("b'#")
    t = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    lst = list(t)
    pwmRed.ChangeDutyCycle(float(lst[0]*100/255))
    pwmGreen.ChangeDutyCycle(float(lst[1]*100/255))
    pwmBlue.ChangeDutyCycle(float(lst[2]*100/255))


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


mqttc = paho.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect('192.168.5.18', 1883)

rc = 0
while True:
    while rc == 0:
        import time
        rc = mqttc.loop()
    print("rc: " + str(rc))