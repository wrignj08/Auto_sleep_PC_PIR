import time
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

mouse = Mouse(usb_hid.devices)
key_L=Keycode.L
PIR = DigitalInOut(board.GP1)
windows_key = Keycode.GUI
keyboard=Keyboard(usb_hid.devices)

last_time = time.monotonic()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


import neopixel
pixel_pin = board.GP0
num_pixels = 5
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.02, auto_write=False, pixel_order=ORDER
)


locked = False 
led.value = False
lock_time = 10

while True:
    
    inactive_timer = time.monotonic() - last_time
    
    if not locked:
    	led_count = int((inactive_timer/lock_time)*num_pixels)
    	for i in range(0,led_count):
    	    pixels[i] = (255, 0, 0)
    	    pixels.show()
    	for i in range(led_count,num_pixels):
    	    pixels[i] = (0, 0, 0)
    	    pixels.show()
    
    if inactive_timer >2:
        led.value = True 
    else:
        led.value = False 
    
    if inactive_timer >lock_time:
        if not locked: 
            keyboard.press(windows_key,key_L)
    	    keyboard.release(windows_key,key_L)
    	    
    	    locked = True
    	    led.value = locked

    if PIR.value == True:
        last_time = time.monotonic()
        if locked:
            mouse.move(-10,-10)
            time.sleep(.5)
            mouse.move(10,10)          
        
    	    locked = False
    	    led.value = locked
    	



