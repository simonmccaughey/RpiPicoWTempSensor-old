#import ubinascii

import gc
#import micropython


import uasyncio as asyncio
from client import TcpClient
from temperaturedisplay import TemperatureDisplay
from tempsensor import TempSensor

from aswitch import Pushbutton

from machine import Pin
#import utime as time

from config import Config
from led_control import LedBlinker
from status import Status
import sys


import ulogging as logging
import network


class Thermostat:
  
  def __init__(self):
    self.log = logging.getLogger('main')
    self.log.info('starting ')
    self.status = Status()
    self.log.info('Blinker')
    self.led = LedBlinker()
    self.led.blink_fast()
    self.log.info('Config')
    self.config =  Config()

    self.connected = False
    self.zone = self.config.zone

    self.set_temp = 0
    self.log.info('Display')
    self.display = TemperatureDisplay()
    #display the version briefly at startup
    self.display.bottom_line_text('20220822 12:44')
    
    #check if we are in non-start mode
    if(self.config.mode == '0'):
      self.display.status('Connect mode')
      self.config.mode = 1;
      self.config.save()
      sys.exit()

    
    self.log.info('Sensor')
    self.sensor = TempSensor(self.read_temp)
    
    self.client = None

    #D0	16
    #D1	5
    #D2	4
    #D3	0
    #D4	2
    #D5	14
    #D6	12
    #D7	13
    #D8	15
    #TX	1
    #RX	3
    #self.setup(14, 1)
    #self.setup(12, 2)
    #self.setup(13, 3)
    #self.setup(15, 4)
    #self.setup(2,  5)
    
    self.display.status('Starting...')
    self.log.info('TCP Client')
    self.client = TcpClient(self.text_received, self.status_update, self.cb)
    loop = asyncio.get_event_loop()
    loop.create_task(self.print_status())
  
  def press(self, p):
    print('Button pressed!! ', p)

  
  def setup(self, gpio, no):
    pin = Pin(gpio, Pin.IN, machine.Pin.PULL_UP)
    pb = Pushbutton(pin, self.press, (no,))

  def read_temp(self, temp):
    
    #print('temperatures:', end=' ')
    try:
      #print(temp, end=' ')
      self.display.temperature(temp)
      self.status.temp = temp
      #print('about to send', end=' ')
      self.client.send("TempRead %s %s\n" % (self.zone, temp))
      self.log.info('sent : ' + str(temp))
    except Exception as e:
      self.log.warning("Unexpected error:" + str(e))
    except :
      self.log.warning("Super-Unexpected error:")
        #pass
    #print('')

  def button_pressed(self, pin):
    
    ##TODO up/down setting on 2 pins
    self.set_temp += 0.5
    self.log.info('new temp ' + str(self.set_temp))
    #if client_connected:
    #  client.send("TempSet %s %s\n" % (zone, set_temp))

  def cb(self, n):
    pass
    #self.display.cb(n)
    
  def text_received(self, line):
    parts = line.split(' ')

     
    if(parts[0] == 'ACK'):
      time = parts[2][0:5]
      self.display.time(time)
      self.status.last_time = parts[2]
      return
  
    #blink the LED to show we got data
    self.led.blink()
    self.log.debug('Line: ' + str(parts))
    
    if(parts[0] == 'Update'):
      if(parts[1] == self.zone):
        self.log.debug('update display now')
        time = parts[3][0:5]
        self.log.info('program time : ' + time)
        self.display.showprogram(parts[2], time)
        self.set_temp = parts[6]
        self.display.temperature_set(self.set_temp)
        self.status.set_temp = self.set_temp
        self.status.time = time
        self.status.state = parts[2]

  def status_update(self, wifi_connected, client_connected, ip):
    
    
    #NOTE: sometimes wifi status is reported as False even when 
    #      the client is connected and working perfectly
    status = ''
    self.status.wifi = wifi_connected
    self.status.client = client_connected
    
    self.log.info('>>> Status : ' + str(wifi_connected) + ' - ' + str(client_connected))
    
    if client_connected is False:
      if wifi_connected is False:
        status = 'WiFi...'
        self.led.blink_fast()
      else:
        status = 'Client...'
        self.led.blink_slow()
        #print('Display: ', display)
        #print('ip :     ', ip)
        if ip is not None:
          ip_address = '    ' + ip
          self.display.bottom_line_text(ip_address[-16:])
        
      self.display.status(status)
      
    
  def print_status(self):
    while(True):
      await asyncio.sleep_ms(2000)
      self.status.screen = self.display.display_status()
      self.status.sensor = self.sensor.sensor_status()
      
      #self.status.print()
  
  def tidy_up(self):
    
      #some stuff to do when the program exits
      #turn the LED off
      self.led.off()
      self.sensor.close()
      self.client.close()
      self.led.close()
      self.display.bottom_line_text('------')
      
      self.log.info('All done!')



try:

  #restart webrepl, it works better after wifi is connected (apparently)
  import gc
  #import webrepl
  #webrepl.start()
  gc.collect()
  
  print('Begin...')
  t = Thermostat()
  print('Thermostat created')
  gc.collect()
  #import pico_web
  
  #loop = asyncio.get_event_loop()
  #loop.run_forever()
  #gc.collect()
  print('import web...')
  import pico_web
  gc.collect()
  print('import completed')
  pico_web.myWs.set_status(t.status)
  pico_web.app.run(debug=True, host='0.0.0.0', port=80)
except Exception as e:
  print('Exception : ' + str(e))
  print('E' + str(e.value))
  print('E' + str(e.errno))
  raise e
except:
  print('Something else!')
  raise
finally:
  t.tidy_up()
  
  ##this code makes it auto reboot, but it also swallows errors
  ## maybe it should go in main??
  import time 
  print('Program finished, rebooting in 10 seconds (CTRL-c to cancel)')
  for x in range(10):
    print('.', end='')
    time.sleep(1)

  machine.reset()















