# coding: utf-8
from __future__ import print_function
import sqlite3
from optparse import OptionParser
from simple_websocket_server import WebSocket, WebSocketServer
'''
@Author Jiage
@Function save the data into database
@Date 12 June 2021
'''
class Storage(object):

    # init database table
    def __init__(self):
        print("init database....")
        self.conn = sqlite3.connect("./watch.db")
        c = self.conn.cursor()
        count = \
        c.execute("SELECT COUNT(*) as count FROM sqlite_master where type='table' and name='data_hour'").fetchone()[0]
        if count == 1:
            c.close()
            return
        c.executescript('''
        create table data_hour(
            id INTEGER PRIMARY KEY NOT NULL,
            ip VARCHAR (20) NOT NULL,
            cpu_usage  FLOAT,
            mem_usage  FLOAT,
            mem_total_mb INTEGER,
            mem_avail_mb INTEGER,
            ts DATETIME DEFAULT (CURRENT_TIMESTAMP)
            )
        ''')
        self.conn.commit()
        c.close()

    # save the data into database
    def Save(self, _ip, _cpu_usage, _mem_usage, _mem_total_mb, _mem_avail_mb):
        print("save data from ", _ip)
        c = self.conn.cursor()
        c.execute("insert into data_hour(ip,cpu_usage,mem_usage,mem_total_mb,mem_avail_mb) values('%s',%f,%f,%f,%f)"
                  % (_ip, _cpu_usage,_mem_usage, _mem_total_mb,_mem_avail_mb) )
        self.conn.commit()
        c.close()

'''
@Author Jiage
@Function receive the data from client
   handle process request
   connected connect event
   handle_close close connect
@Date 12 June 2021
'''
class Receive(WebSocket):
    def handle(self):
        ip = str(self.address[0])
        ip = ip.replace("::ffff:","")
        dataSet = self.data.split(",")
        cpu_usage = float(dataSet[0])
        mem_usage = float(dataSet[1])
        mem_total_mb = float(dataSet[2])
        mem_avail_mb = float(dataSet[3])
        STORAGE.Save(_ip=ip, _cpu_usage=cpu_usage,
                     _mem_usage=mem_usage, _mem_total_mb=mem_total_mb,
                     _mem_avail_mb=mem_avail_mb)
        self.send_message(self.data+"-ACK-OK")

'''
@Author Jiage
@Function start the server to receive the data and then save it into database
@Date 12 June 2021
'''
if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]', version='%prog 1.0')
    parser.add_option('--host', default='', type='string', action='store', dest='host', help='hostname (localhost)')
    parser.add_option('--port', default=1111, type='int', action='store', dest='port', help='port (1111)')
    (options, args) = parser.parse_args()
    clients = []
    STORAGE = Storage()
    server = WebSocketServer(options.host, options.port, Receive)
    server.serve_forever()