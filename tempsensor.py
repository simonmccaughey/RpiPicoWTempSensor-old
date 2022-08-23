

from ds18x20 import DS18X20
from onewire import OneWire
from machine import Pin
import uasyncio as asyncio

import ulogging as logging

class TempSensor(object):
  
  def __init__(self, callback=None):
    self.log = logging.getLogger('TempSensor')
    self.log.info("starting...")
    ow = OneWire(Pin(22))

    self.callback = callback
    self.ds = DS18X20(ow)
    self.roms = None
    self.log.info("scanning for 1-wire devices...")
    
    #TODO make this write a sensible error when no device is found
    #self.timer_temperature = Timer(3)
    #self.timer_temperature.init(period=5000, mode=Timer.PERIODIC, callback=self.read_temp)  
    self.last_temps = []
    self.loop = asyncio.get_event_loop()
    self.loop.create_task(self.run_temp_sensor())
    
  def set_debug():
    log.setLevel(logging.DEBUG)
    
  def sensor_status(self):
    if len(self.roms) > 0:
      return True
    return False

  def close(self):
    #self.timer_temperature.deinit()
    self.log.info('TempSensor: Stopping timer')

  async def run_temp_sensor(self):    
    counter = 0
    while self.roms is None or len(self.roms) == 0:
      try:
        counter += 1
        if(counter > 10):
          await asyncio.sleep(10)
        await asyncio.sleep(1)
        self.log.info('Scanning for ROMs [attempt:' + str(counter) + ']')
        self.roms = self.ds.scan()
        self.log.info("found " + str(self.roms))
        
      except Exception as e:
        self.log.error("Exception reading ROMs:" + str(e))
        
    
    
    #print('temperatures:', end=' ')
    counter = 0
    while True:
      self.log.debug("---------------------")
      try:
        
        self.ds.convert_temp()
        #print("sleep for 1")
        await asyncio.sleep_ms(1000)
        #print("sleep done")
        for rom in self.roms:
          #print("checking rom.." , rom)
          temp = self.ds.read_temp(rom);
          temp = str(round(float(temp),1))
          self.log.debug('Last: ' + str(self.last_temps) + ' - now: ' + str(temp)) 
          #counter makes us send something around every minute, even if the temperature hasnt changed
          counter = counter + 1
          need_to_report = False
          
          if(temp not in self.last_temps and temp is not None):
            need_to_report = True
            self.last_temps.insert(0, temp)
            if(len(self.last_temps) > 5):
              self.last_temps.pop()
            #print('TempSensor: ' + temp, end=' ')

            #print('about to report', end=' ')
          if(counter > 60):
            counter = 0
            need_to_report = True
          self.log.debug('counter : ' + str(counter) + ', need to report : ' + str(need_to_report)) 
          if(need_to_report):
            self.loop.create_task(self.run_callback(temp))
            
      except Exception as e:
        self.log.warning("Unexpected error:" +  str(e))
      except :
        self.log.warning("Super-Unexpected error:")
          #pass
      #print('')
  async def run_callback(self, temp):
    if self.callback is not None:
      self.log.info('reporting...' + temp)
      #print("calling loop")
      self.callback(temp)
      self.log.debug('reported')

def my_callback(temp):
  print('>>>>> ' + temp)
  
def mysleep():
  await asyncio.sleep_ms(1000)

if __name__ == "__main__":
  #reset the event loop (otherwise lots of tasks run at the same time)
  ##NOTE: currently not working - do a soft reset between runs
  loop = asyncio.get_event_loop()
  loop.close()
  
  #optionally configure extra logging
  #logging.basicConfig(level=logging.DEBUG)
  sensor = TempSensor(my_callback)
  
  loop.run_forever()









