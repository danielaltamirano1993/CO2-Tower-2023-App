# version 3.3 17.4.2019
# author: RKW
# connetion to phone wifi. Reconnects after lost connection.
# test if carbonIntensity exists and if value is a float.
# keep values between 0 and 30.
# ESP32-LEDstrip: 
# GND(GI0)-GND(white), IO16(IO4)-signal(green), 3.3V(NC)-VCC(red)
# Blink blue LED 0: remainder of loop, show red and green.
# Blink blue LED 1: no valid data available, use old data.
# Blink blue LED center: new data equal to old data.


import machine
import neopixel
import urequests
import network
import utime


def blinking(noOfBlinks):
    for i in range(noOfBlinks):
        led.on()
        utime.sleep(0.2)
        led.off()
        utime.sleep(0.2)
    utime.sleep(1)


def get_carbon_intensity():
    led.off()
    sta_if = network.WLAN(network.STA_IF)
    utime.sleep(1)
    if sta_if.isconnected():
        blinking(1)
    sta_if.active(True)
    utime.sleep(1)
    sta_if.connect('AndroidAP', 'fbas2451')
    utime.sleep(10)
    blinking(2)
        return 0
       
 
def scale(a1, a2, b1, b2, s):
    value = (b1 + ((s - a1) * (b2-b1) / (a2-a1)))
    if (value > b2):
        value = b2
    if (value < b1):
        value = b1
    return value

led = machine.Pin(2, machine.Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(16), 30)
# max brightness = 255
brightness = 50
blink_all(20)
# showBlink=100 equals about 1 minute
showBlink = 800
co2_skaleret_old = 15
# permanently color red LEDs:
for i in range(co2_skaleret_old):
    np[i] = (brightness, 0, 0)
    np.write()
# permanently colour green LEDs:
for i in range(30-co2_skaleret_old):
    np[co2_skaleret_old+i] = (0, brightness, 0)
    np.write()
    
    
