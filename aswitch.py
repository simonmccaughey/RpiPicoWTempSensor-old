# aswitch.py Switch and pushbutton classes for asyncio
# Delay_ms A retriggerable delay class. Can schedule a coro on timeout.
# Switch Simple debounced switch class for normally open grounded switch.
# Pushbutton extend the above to support logical state, long press and
# double-click events
# Tested on Pyboard but should run on other microcontroller platforms
# running MicroPython and uasyncio.

# The MIT License (MIT)
#
# Copyright (c) 2017 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import uasyncio as asyncio
import utime as time

# launch: run a callback or initiate a coroutine depending on which is passed.


class Pushbutton(object):
  def __init__(self, pin, cb, args=()):
    self.pin = pin # Initialise for input
    self.cb = cb
    self.args = args
    self.sense = pin.value()  # Convert from electrical to logical value
    self.state = self.rawstate()  # Initial state
    self.loop = asyncio.get_event_loop()
    self.loop.create_task(self.check())  # Thread runs forever

    # Current non-debounced logical button state: True == pressed
  def rawstate(self):
    return bool(self.pin.value() ^ self.sense)

  async def check(self):
    while True:
      state = self.rawstate()
      # State has changed: act on it now.
      if state != self.state:
        self.state = state
        if state:
          # Button is pressed
          self.loop.call_soon(self.cb, self.args)
      # Ignore state changes until switch has settled
      await asyncio.sleep_ms(50)




