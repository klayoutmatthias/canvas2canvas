#!/usr/bin/env python3

import asyncio
import websockets
import time
# NOTE: import db to enable stream format readers
import klayout.db as db
import klayout.lay as lay

class LayoutViewServer(object):

  def __init__(self, url):
    self.layout_view = None
    self.url = url

  def run(self):
    start_server = websockets.serve(self.connection, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

  async def send_image(self, websocket, data):
    print("@@@ sent image ..")
    await websocket.send(data)

  def image_updated(self, websocket):
    pixel_buffer = self.layout_view.get_screenshot_pixels()
    print(f"@@@ got image ... {pixel_buffer.width()},{pixel_buffer.height()}")
    asyncio.create_task(self.send_image(websocket, pixel_buffer.to_png_data()))

  async def connection(self, websocket, path):

    self.layout_view = lay.LayoutView()
    self.layout_view.load_layout(self.url)
    self.layout_view.max_hier()

    writer_task = asyncio.create_task(self.timer(websocket))
    reader_task = asyncio.create_task(self.reader(websocket))
    await reader_task

  async def timer(self, websocket):
    print("Starting timer ...")
    self.layout_view.on_image_updated_event = lambda: self.image_updated(websocket)
    while(True):
      self.layout_view.timer()
      await asyncio.sleep(0.01)

  def mouse_event(self, function, tokens):
    x = int(tokens[1])
    y = int(tokens[2])
    b = int(tokens[3])
    k = int(tokens[4])
    buttons = 0
    if (k & 1) != 0:
      buttons |= lay.ButtonState.ShiftKey
    if (k & 2) != 0:
      buttons |= lay.ButtonState.ControlKey
    if (k & 4) != 0:
      buttons |= lay.ButtonState.AltKey
    if (b & 1) != 0:
      buttons |= lay.ButtonState.LeftButton
    if (b & 2) != 0:
      buttons |= lay.ButtonState.RightButton
    if (b & 4) != 0:
      buttons |= lay.ButtonState.MidButton
    function(db.Point(x, y), buttons)

  async def reader(self, websocket):
    while(True):
      msg = await websocket.recv()
      if msg == "q":
        break
      print(f"From Client: {msg}") # @@@
      tokens = msg.split(",")
      if tokens[0] == "resize":
        self.layout_view.resize(int(tokens[1]), int(tokens[2]))
      elif tokens[0] == "mouse_move":
        self.mouse_event(self.layout_view.send_mouse_move_event, tokens)
      elif tokens[0] == "mouse_pressed":
        self.mouse_event(self.layout_view.send_mouse_press_event, tokens)
      elif tokens[0] == "mouse_released":
        self.mouse_event(self.layout_view.send_mouse_release_event, tokens)
      elif tokens[0] == "mouse_enter":
        self.layout_view.send_enter_event()
      elif tokens[0] == "mouse_leave":
        self.layout_view.send_leave_event()
      elif tokens[0] == "mouse_dblclick":
        self.mouse_event(self.layout_view.send_mouse_double_clicked_event, tokens)

server = LayoutViewServer("https://github.com/KLayout/klayout/blob/master/testdata/gds/t10.gds?raw=true")
server.run()

