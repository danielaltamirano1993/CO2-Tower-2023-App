# version 3.3 17.4.2019
# author: RKW
# connetion to phone wifi. Reconnects after lost connection.
# test if carbonIntensity exists and if value is a float.
# scale-function stays within 0 and 30.
# resets hardware every 8 cycles (2 hours).
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

def blink_all(speed):
    for j in range(2):
        for i in range(30):
            np[i] = (0, 0, 255)
            np.write()
            utime.sleep_ms(speed)
            np[i] = (0, 0, 0)
            np.write()
            np[29-i] = (0, 0, 255)
            np.write()
            utime.sleep_ms(speed)
            np[29-i] = (0, 0, 0)
            np.write()
        

def get_carbon_intensity():
    led.off()
    sta_if = network.WLAN(network.STA_IF)
    utime.sleep(1)
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
    
while True:
    for j in range(8):
        co2_level = get_carbon_intensity()
        co2_skaleret = int(scale(50, 250, 0, 30, co2_level))
# test if reading is valid:
        if co2_level > 0:
            # new datapoint is above previous:
            if (co2_skaleret-co2_skaleret_old) > 0:
                for i in range(showBlink):
                    for j in range(co2_skaleret-co2_skaleret_old):
                        np[co2_skaleret_old + j] = (brightness, 0, 0)
                        np.write()
                    utime.sleep_ms(100)
                    for j in range(co2_skaleret-co2_skaleret_old):
                        np[co2_skaleret_old + j] = (0, brightness, 0)
                        np.write()
                    utime.sleep_ms(500)
# new datapoint is below previous:
            if (co2_skaleret_old-co2_skaleret) > 0:
                for i in range(showBlink):
                    for j in range(co2_skaleret_old-co2_skaleret):
                        np[co2_skaleret_old - j] = (0, brightness, 0)
                        np.write()
                    utime.sleep_ms(100)
                    for j in range(co2_skaleret_old-co2_skaleret):
                        np[co2_skaleret_old - j] = (brightness, 0, 0)
                        np.write()
                    utime.sleep_ms(500) 
# new and old are identical:
            if (co2_skaleret == co2_skaleret_old):
                for i in range(showBlink):
                    np[co2_skaleret_old] = (0, 0, brightness)
                    np.write()
                    utime.sleep_ms(5)
                    np[co2_skaleret_old] = (brightness, 0, 0)
                    np.write()
                    utime.sleep_ms(595)
# Blink LED no 0 for remainder of 15 minutes:
        for i in range(1500-showBlink):
            np[0] = (0, 0, brightness)
            np.write()
            utime.sleep_ms(5)
            np[0] = (brightness, 0, 0)
            np.write()
            utime.sleep_ms(595) 
    machine.reset()
