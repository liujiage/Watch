from __future__ import print_function
from optparse import OptionParser
from websocket import create_connection
import psutil
import threading
import time
import traceback

'''
@Author Jiage
@Function send the data to collector
@Date 12 June 2021
'''
def send(_options):
    while True:
        try:
            ws = create_connection("ws://" + _options.host + ":" + str(_options.port) + "/")
            cpu_percent = psutil.cpu_percent(interval=1)
            mem_usage = psutil.virtual_memory().percent
            mem_avail_mb = psutil.virtual_memory().available / 1024 / 1024
            mem_total_mb = psutil.virtual_memory().total / 1024 / 1024
            message = str(cpu_percent) + "," + str(mem_usage) + "," + str(mem_total_mb) + "," + str(mem_avail_mb)
            print("Send message is " + message)
            ws.send(message)
            print("Sent")
            print("Receiving...")
            result = ws.recv()
            print("Received '%s'" % result)
            ws.close()
            interval = int(_options.interval)
            time.sleep(interval)
        except Exception:
            time.sleep(60)
            traceback.print_exc()

'''
@Author Jiage
@Function start a watcher 
@Date June 2021
'''
if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]', version='%prog 1.0')
    parser.add_option('--host', default='localhost', type='string', action='store', dest='host', help='hostname (localhost)')
    parser.add_option('--port', default=1111, type='int', action='store', dest='port', help='port (1111)')
    parser.add_option('--interval', default=1, type=int, action='store', dest='interval', help='interval(sec)')
    (options, args) = parser.parse_args()

    sendTask = threading.Thread(target=send(options))
    sendTask.daemon = True
    sendTask.start()
    sendTask.join()