from websocket import create_connection
from websocket import WebSocket
import traceback
import time

def register():
    while True:
        try:
             ws = create_connection("ws://localhost:1111/")
             #watcher-command
             ws.send("C-WATCH-COMMAND:register")
             result = ws.recv()
             print("Received '%s'" % result)
             return ws
        except Exception:
            time.sleep(1)
            traceback.print_exc()

def receive():
    # register
    ws = register()
    # receive command from server side
    while True:
        try:
            time.sleep(5)
            result = ws.recv()
            print("Received '%s'" % result)
            print("Sending 'Hello, World'...")
            ws.send("C-WATCH-DATA:Hello World")
            print("Sent")
            print("Receiving...")
            result =  ws.recv()
            print("Received '%s'" % result)
            # ws.close()
        except Exception:
            time.sleep(1)
            traceback.print_exc()


if __name__ == '__main__':
    receive()