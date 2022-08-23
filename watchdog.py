
import machine
from machine import Timer

class WDT:
  def __init__(self):
    self.timer = Timer()  
    #self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.do_check)  
    self.iteration = 0
    self.max = 60
  def setmax(self, max):
    self.max = max

  def do_check(self, arg):
    self.iteration += 1
    #print('Elapsed--->>> ' , self.iteration)
    #if(self.iteration % 5 == 0):
    #  print('WDT Iteration ', self.iteration)
    if self.iteration > self.max:
      print('watchdog reset...')
      machine.reset()

  def feed(self):
    #print('iteration = ' + str(self.iteration))
    self.iteration = 0
    #print('fed! ')









