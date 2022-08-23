import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('BTWholeHome-CJW', '1029384756abc')
sta_if.isconnected()
sta_if.ifconfig()
