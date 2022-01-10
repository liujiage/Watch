import logging
import paramiko
from paramiko import SSHClient
from scp import SCPClient
logging.basicConfig()

host = "10.30.0.48"
port = 22
username = "user_name"
password = "**********"
command = "ls"
target = "/home/user_name/"
#ssh = paramiko.SSHClient()

with SSHClient() as ssh:
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    # stdin, stdout, stderr = ssh.exec_command(command)
    # lines = stdout.readlines()
    # print(lines)
    with SCPClient(ssh.get_transport()) as scp:
       # scp.put('config.txt',remote_path=target)
       scp.put('a',recursive=True, remote_path=target)
       #scp.put('/Users/liujiage/PycharmProjects/watch/test/b', recursive=True, remote_path=target)




