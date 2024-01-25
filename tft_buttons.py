from machine import Pin

class Buttons():
    def __init__(self):
        self.name = "ws_pico_13"
        self.key0 = Pin(15,Pin.IN,Pin.PULL_UP)
        self.key1 = Pin(17 ,Pin.IN,Pin.PULL_UP)
        self.key2 = Pin(19,Pin.IN,Pin.PULL_UP)
        self.key3 = Pin(21,Pin.IN,Pin.PULL_UP)
        self.up = Pin(18,Pin.IN,Pin.PULL_UP)
        self.down = Pin(2,Pin.IN,Pin.PULL_UP)
        self.left = Pin(16,Pin.IN,Pin.PULL_UP)
        self.right = Pin(20,Pin.IN,Pin.PULL_UP)
        self.center = Pin(3,Pin.IN,Pin.PULL_UP)
