from simple_websocket_server import WebSocketServer, WebSocket
import time
import traceback
import hashlib

class request(WebSocket):

    def handle(self):
        try:
            data  = self.data.strip()
            ip = str(self.address[0]).replace("::ffff:", "")+"-"+str(self.address[1])
            if data.startswith("C-WATCH-DATA:"):
                data = data.replace('C-WATCH-DATA:', '')
                print "receive data C-WATCH-DATA:", data, ip
                self.send_message('S-WATCH-DATA-ACK:OK')
            elif data.startswith("C-WATCH-COMMAND:"):
                data = data.replace('C-WATCH-COMMAND:','')
                print "receive data C-WATCH-COMMAND: ", data, ip
                self.send_message('S-WATCH-COMMAND-ACK:OK')
            elif data.startswith("M-WATCH-COMMAND:"):
                data = data.replace('M-WATCH-COMMAND:', '')
                print "receive data M-WATCH-COMMAND: ", data, ip
                self.send_message('S-WATCH-COMMAND-ACK:OK')
                # send  stop command to all of client
                for k,v in clients.iteritems():
                    print "send stop ", k
                    v.send_message("S-WATCH-COMMAND:stop")
            else:
                self.send_message('S-ERROR-ACK:UNKNOWN-PROTOCOL')
        except Exception:
            time.sleep(1)
            traceback.print_exc()

    def connected(self):
        ip = str(self.address[0]).replace("::ffff:", "")+"-"+str(self.address[1])
        # hashlib.md5(b'123').hexdigest()
        clients[ip] = self
        print(self.address, 'connected')

    def handle_close(self):
        ip = str(self.address[0]).replace("::ffff:", "") + "-" + str(self.address[1])
        del clients[ip]
        print(self.address, 'closed')

clients = {}
server = WebSocketServer('', 1111, request)
server.serve_forever()