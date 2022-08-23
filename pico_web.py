import picoweb
import os

from config import Config
#from machine import Pin
import uasyncio as asyncio


#define static files. It seems we can refer to app here before it gets initialised.
#ROUTES = [
#  ("/favicon.ico", lambda req, resp: (yield from app.sendfile(resp, "favicon.ico"))),
#]


app = picoweb.WebApp(__name__)

from status import Status
import machine


class Web:
  
  def __init__(self):
    self.status = Status()
    self.config = Config()
    self.menu = '<a href="/">home</a> | <a href="/conf">config</a> | <a href="/reset">reboot</a> | <a href="/kill">kill</a><p>'
    self.view = '<meta name="viewport" content="width=device-width, initial-scale=1.5">'
    
  def set_status(self, status):
    self.status = status
  
  def index(self, req, resp):
    yield from picoweb.start_response(resp)
    
    
    #output = ''
    #output += 'HTTP/1.1 200 OK\nConnection: close\nServer: nanoWiPy\nContent-Type: text/html\n\n')
    yield from resp.awrite('<html><head><title>%s - Config</title>'%self.config.zone)
    yield from resp.awrite(self.view + '</head><body>%s<table>' % self.menu)

    yield from resp.awrite('<tr><td>Zone</td><td>%s</td></tr>' % (self.config.zone))
    for key in self.status.fields():
      value = getattr(self.status, key)
      yield from resp.awrite('<tr><td>%s</td><td>%s</td></tr>' % (key, value))
  

    #yield from resp.awrite('<tr><td>WiFi connected</td><td>' + str(self.status.wifi) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Client connected</td><td>' + str(self.status.client) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Set Temperature</td><td>' + str(self.status.set_temp) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Temperature</td><td>' + str(self.status.temp) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Current program</td><td>' +  str(self.status.state) + '/' + str(self.status.time) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Screen Online</td><td>' + str(self.status.sensor) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Sensor Online</td><td>' + str(self.status.sensor) + '</td></tr>')
    #yield from resp.awrite('<tr><td>Last network input</td><td>' + str(self.status.last_time) + '</td></tr>')

    yield from resp.awrite('</table><p><font size=-2>%s<br>%s</body></html>' % (os.uname().version, os.uname().release ))
     
  def conf(self, req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite('<html><head><title>%s - Config</title>' % self.config.zone)
    yield from resp.awrite(self.view)
    yield from resp.awrite('</head><body>%s<form action="/save" method="get"><table>' % self.menu)

    for key in self.config.fields():
      value = getattr(self.config, key)
      print('----> ' + key + ' ' + str(value))
      yield from resp.awrite('<tr><td><label for="%s">%s</label></td>' % (key, key))
      yield from resp.awrite('<td><input type="text" name="%s" value="%s"></input></td></tr>' % (key,value))
    
    yield from resp.awrite('<tr><td></td><td><input type="submit" value="Save"></td></tr></table></form></body></html>')
    

  def save(self, req, resp):
    
    print('query: ' + str(req.qs))
    yield from resp.awrite('HTTP/1.1 302 Found\nLocation: /conf\n\n')
    
    for pair in req.qs.split('&'):
      key, value = pair.split('=')
      print('Pair:' + pair)
      setattr(self.config, key, value)
    
    self.config.save()
  
  def reset(self, req, resp):
    self.reboot()
    yield from resp.awrite('HTTP/1.1 302 Found\nLocation: /\n\n')
    
  def kill(self, req, resp):
    self.config.mode="0"
    self.config.save()
    self.reboot()
    yield from resp.awrite('HTTP/1.1 302 Found\nLocation: /\n\n')
    
  def reboot(self):
    loop = asyncio.get_event_loop()
    loop.create_task(self.do_reboot())
    
  async def do_reboot(self):
    await asyncio.sleep_ms(1000)
    machine.reset()
    

myWs = Web()

@app.route('/')
def index(req, resp):
  return myWs.index(req, resp)
  
@app.route('/conf')
def conf(req, resp):
  return myWs.conf(req, resp)

  
@app.route('/save')
def save(req, resp):
  return myWs.save(req, resp)

@app.route('/reset')
def reset(req, resp):
  return myWs.reset(req, resp)

@app.route('/kill')
def reset(req, resp):
  return myWs.kill(req, resp)

  
@app.route('/favicon.ico')
def fav(req, resp):
  yield from app.sendfile(resp, "favicon.ico", content_type='image/x-icon')


def run():
  led = Pin(2, Pin.OUT)
  
  while(True):
    await asyncio.sleep_ms(1000)
    led.on()
    await asyncio.sleep_ms(1000)
    led.off()
    


if __name__ == "__main__":
  import uasyncio as asyncio

  loop = asyncio.get_event_loop()
  try:
    #loop.create_task(run())

    print('Running webserver now...')
    app.run(debug=True, host='0.0.0.0', port=80)
  finally:
     loop.stop()
     loop.close()
    







