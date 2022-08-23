from ssd1306 import SSD1306_I2C
import machine
from machine import I2C, Pin
from writer import Writer
import freesans34_num
import ulogging as logging

class TemperatureDisplay(object):
 
  #pin 5 is D1 and pin 4 is D2
  def __init__(self, sda_pin_num=8, scl_pin_num=9):
    self.log = logging.getLogger('Display')
    self.log.info('Opening I2C using sda=' + str(sda_pin_num) + ', scl=' + str(scl_pin_num))
    self.i2c = I2C(0, sda=Pin(sda_pin_num, machine.Pin.OUT), scl=Pin(scl_pin_num, machine.Pin.OUT))
    scan = self.i2c.scan()
    self.log.info('I2C Bus: ' + str(scan))
    
    if len(scan) == 0:
      self.log.info('No screen detected')
      self.display = None
    else:
      self.display = SSD1306_I2C(128, 64, self.i2c)
      self.display.contrast(0x01)
      #clear the screen
      self.display.fill(0)

      #display.text('Temperature',3,3)
      #self.display.text('00:00',75,57)
      self.writer = Writer(self.display, freesans34_num, verbose=False)
      Writer.set_clip(True, True)
      Writer.set_textpos(16, 20)
      #wri2.printstring('23.0')
      #write out the degrees sign on the screen (fixed location)
      self.display.text('O', 105, 17)

      self.display.show()
      
  def cb(self, n):
    self.text(str(n),113,17)

  def temperature(self, temperature):
    if self.display is not None:
      Writer.set_textpos(16, 20)
      self.writer.printstring(str(round(float(temperature),1)))
      self.display.show()
    
  def temperature_set(self, temperature):
    temp = round(float(temperature),1)
    if temp == -999.0:
      t = 'none'
    else:
      t = temp
    #extra space here to cover 'bottom_line_text'
    self.text('t=%s     ' % t, 0,57)

  def bottom_line_text(self, text):
    self.text(text, 0,57)
    
  def showprogram(self, on_off, time):
    #invert the colour if it is 'On'
    col = 0 if on_off == 'On' else 1
    #put a load of spaces along the display to colour it in
    if time == '00:00':
      #dont show the time if it is 00:00
      self.text(on_off + '                                 ', 0,0, col)
    else:
      self.text(on_off + '/' + time + '                    ', 0,0, col)
      

  def status(self, error):
    self.text(error + '                                  ', 0,0, 0)


  def time(self, time):
    self.text(time, 89,57)

  def text(self, text, x, y, col=1):
    if self.display is None:
      self.log.info('Fake display text: ', text)
    else:
      fill_col = 1 - col
      self.display.fill_rect(x, y, len(text)*8, 8, fill_col)
      self.display.text(text, x, y, col)

      self.display.show()
  def display_status(self):
    if self.display is None:
      return False
    return True
    
    
    
    
if __name__ == "__main__":

  display = TemperatureDisplay()
  display.temperature(23.2)
  #display.temperature_set('12.4')
  display.status('Off')
  #display.cb(3)
  display.time('12:34')
  display.text('On/10:23 ', 0,0, 0)
  #display.text('Off until 11:33', 0,0)
  display.text('t=24.5', 0,57)
  #display.text('22:33', 89,57)

  #display.text('Off/11:44', 0,0, 1)
  #display.text('           ', 0,0, 1)
  #display.text('On/10:23                                  ', 0,0, 0)

  #display.status('On', '12:22')















