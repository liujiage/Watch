from __future__ import print_function
from optparse import OptionParser
from websocket import create_connection
import os
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
            cpu_percent = round(float(os.popen(
                '''top -b -n1 | grep 'Cpu(s)' | awk '{print $2 + $4}' ''').readline()), 2)
            mem_total_mb, mem_used_mb, mem_avail_mb = map(float, os.popen('free -t -m').readlines()[-1].split()[1:])
            mem_usage = round((mem_used_mb / mem_total_mb) * 100, 2)
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