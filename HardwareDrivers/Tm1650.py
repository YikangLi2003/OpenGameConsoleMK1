# Hardware driver of numeric LED segments with tm1650
# MicroPython version: v1.19.1 on 2022-06-18
# Test device: Espressif ESP32-WROOM-32

from micropython import const

# addresses of digit display unit
DIG = (const(0x68), const(0x6a), const(0x6c), const(0x6e))

# command for display settings
SETTING = const(0b01001000) 

# Levels of intensity
INT = (
    const((0,0,1)),
    const((0,1,0)),
    const((0,1,1)),
    const((1,0,0)),
    const((1,0,1)),
    const((1,1,0)),
    const((1,1,1)),
    const((0,0,0))
    )

POWERON = const(1) # power on led segments
POWEROFF = const(0) # power off led segments
SEG7 = const(1) # seven-segment mode: 1
SEG8 = const(0) # eight_segment mode: 0

# mapping of single character and display content
ENCODE = {
    " ":0,
    "0":63,
    "1":6,
    "2":91,
    "3":79,
    "4":102,
    "5":109,
    "6":125,
    "7":7,
    "8":127,
    "9":111,
    }

class LedDigitalTube:
    def __init__(self, si2c):
        self.si2c = si2c # machine.SoftI2C object for communication
        self.si2c.init(freq=9000000)
        self._intensity = INT[0]
        self._segmode = SEG8
        self._state = POWERON
        self._set()        
        self.clear()
    
    def _write(self, byte_1, byte_2):
        # write one set of data into the chip
        self.si2c.start()
        self.si2c.write(bytearray([byte_1, byte_2]))
        self.si2c.stop()
    
    def _set(self):
        # set intensity, segment display mode and work state
        self._write(SETTING,\
        eval("0b0{}{}{}{}00{}".format(*self._intensity, self._segmode, self._state)))
    
    def digits(self, nums):
        # accept a string 4 characters long and display
        for pos in range(4):
            self._write(DIG[pos], ENCODE[nums[pos]])
        
    def digit(self, pos, num):
        # display one digit and its position then display
        self._write(DIG[pos], ENCODE[num])
    
    def segments(self, data):
        # accept display data in a list and display
        # no encoding
        # such as (0b00101001, 0b10100101, 0b10100101, 0b11001101)
        for pos in range(4):
            self._write(DIG[pos], data[pos])
    
    def segment(self, pos, data):
        # accept display data and position for only one set of led tubes then display
        # no encoding
        # such as pos=1, data=ob10101010
        self._write(DIG[pos], data)
    
    def clear(self):
        # turn off every led tube
        for pos in range(4):
            self._write(DIG[pos], 0)
    
    def intensity(self, i):
        # adjust the intensity within 8 levels
        self._intensity = INT[i]
        self._set()
    
    def segmode(self, mode):
        # set display mode (8-segment or 7-segment)
        if mode == "7":
            self._segmode = SEG7
        elif mode == "8":
            self._segmode = SEG8
        self._set()
    
    def switch(self, state):
        # power on/off led tubes
        self._state = state
        self._set()
