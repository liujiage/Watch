from websocket import create_connection
import traceback


def command(_str):
    try:
        ws = create_connection("ws://localhost:1111/")
        # watcher-command
        ws.send("M-WATCH-COMMAND:stop")
        print("Sent")
        print("Receiving...")
        result = ws.recv()
        print("Received '%s'" % result)
        ws.close()
    except Exception:
        traceback.print_exc()
    finally:
        ws.close()

if __name__ == '__main__':
    command('stop')