
from machine import Pin
import uasyncio as asyncio

import time 
from machine import Timer
import ulogging as logging

class LedBlinker:
  
  def __init__(self):
    self.log = logging.getLogger('LedBlinker')
    self.timer = Timer()  
    self.led=Pin("LED", Pin.OUT)
    self.blink_period = -1
    self.state = 0
    #start the timer
    self.timer.init(period=100,mode=Timer.PERIODIC, callback=self.callback)  
    
  #on and off take a second argument, so that internal 
  #functions can call them without changing the mode
  def on(self, period=-1):
    self.led.value(1)
    self.blink_period = period
  
  def off(self, period=-1):
    self.led.value(0)
    self.blink_period = period
  
# Blink the LED leaving it in the desired final state
  def blink(self):
    self.off()
    #doesnt work in here??
    #asyncio.sleep_ms(100)
    time.sleep_ms(50)
    self.on()
    
  def blink_fast(self):
    self.log.info('Blink fast')
    self.blink_period = 200
    
  def blink_slow(self):
    self.log.info('Blink slow')
    self.blink_period = 500
    
  def callback(self, arg):
    #print('callback')
    self.timer.deinit()
    if self.blink_period == -1:
      self.timer.init(period=1000,mode=Timer.PERIODIC, callback=self.callback)  
    else:
      self.timer.init(period=self.blink_period,mode=Timer.PERIODIC, callback=self.callback)  
      #toggle the led here
      next = 1
      if self.led.value() == 1:
        next = 0
      self.led.value(next)
    
    
  def close(self):
    self.timer.deinit()
    self.log.info('Cancel blink timer')


if __name__ == "__main__":
  print('Running main')

  m = LedBlinker()
  m.on()
    #while True:
    #  await asyncio.sleep_ms(500)
    #  m.blink()
    
  m.blink_fast()
  try:
    while True:
      pass
  
  finally:
    m.off()
    m.close()






