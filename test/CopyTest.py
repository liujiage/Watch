import unittest
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

'''
https://stackoverflow.com/questions/52954532/how-to-copy-a-complete-directory-recursively-to-a-remote-server-in-python-param
https://github.com/jbardin/scp.py
'''
class SSh(object):

    def __init__(self, address, username, password, port=22):
        print "Connecting to server."
        self._address = address
        self._username = username
        self._password = password
        self._port = port
        self.sshObj = None
        self.connect()
        self.scp = SCPClient(self.sshObj.get_transport())

    def sendCommand(self, command):
        if(self.sshObj):
            stdin, stdout, stderr = self.sshObj.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata

                    print str(alldata)
        else:
            print "Connection not opened."

    def connect(self):
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(self._address, port=self._port, username=self._username, password=self._password, timeout=20, look_for_keys=False)
            print 'Connected to {} over SSh'.format(self._address)
            return True
        except Exception as e:
            ssh = None
            print "Unable to connect to {} over ssh: {}".format(self._address, e)
            return False
        finally:
            self.sshObj = ssh


if __name__ == "__main__":
    # Parse and check the arguments
    ssh = SSh("10.30.0.77", username="user_name", password="*******")
    print(ssh)
    #ssh.scp.put("Valigrind_BB.py") # This works perfectly fine
    #ssh.scp.put("temp", recursive=True) # IOError over here Is a directory
    #ssh.sendCommand('ls')