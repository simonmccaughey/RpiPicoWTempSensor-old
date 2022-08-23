


class Status:
  
  
  def __init__(self):
    self.wifi = None
    self.client = None
    self.last_time = None
    self.set_temp = None
    self.temp = None
    self.state = None
    self.time = None
    self.screen = None
    self.sensor = None
    
  def fields(self):
    return ['wifi', 'client', 'last_time', 'set_temp', 'temp', 'state', 'time', 'screen', 'sensor']

