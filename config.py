


import json
import os

class Config:
  wifi_ssid = None
  wifi_password = None
  host = None
  port = None
  client_name = None
  zone = None
  mode = None
      

	
  def __init__(self):
    self.load()

  def load(self):
      ## check the file exists
      #try:
      if('config.json' in str(os.listdir())):
        f = open('config.json')
        print ('contents: ')
        print (f.read())
        f.close()
        f = open('config.json')
        dict  = json.load(f)
        f.close()
        print('load config from file completed.' + str(dict))
        for key, value in dict.items():
          setattr(self, key, value)
        print('values set')
      else:
        #set defaults
        print('Setting defaults')
        dict={}
        for field in self.fields():
          setattr(self, field, '')
        print('Saving')
        self.save()
        print('Saved.')
        
        #except:
        #  print("Unexpected error:", sys.exc_info()[0])
        #  print('no configuration file - creating defaults')
        #  wifi_ssid = 'none'
        #  wifi_password = 'none'
        #  host = '192.168.2.1'
        #  port = '123455'
        #  client_name = 'wemos'
        #  zone = 'Water'
        #  self.save()

      
    
    
  def save(self):
    f = open('config.json', 'w')
    dict = {}
    for field in self.fields():
      dict[field] = getattr(self, field)
    json.dump(dict, f)
    f.close()
    print('Saving: ' + json.dumps(dict))


  def fields(self):
    return ['wifi_ssid', 'wifi_password', 'host', 'port', 'client_name', 'zone', 'mode']


if __name__ == "__main__":
  c = Config()
  print(c.host)
  #c.host = '123443'
  #print(c.host)
  #c.save()



