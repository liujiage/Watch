from optparse import OptionParser
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import traceback

'''
@Author Jiage
@Function deploy Watcher and Collector
@Date 16 June 2021
'''
def getIps(_file='./config.txt'):
    print 'get all ip from '+_file
    ips = []
    with open(_file) as f:
        # search [IP]
        for index in f:
            if index.strip().upper() == '[IP]': break
        # get all ip
        for ip in f:
            if len(ip.strip()) == 0: break;
            ips.append(ip.strip())
    print 'all ip is' + str(ips)
    return ips

'''
@Author Jiage
@Function deploy Watcher and Collector
@Date 16 June 2021
'''
def deploy(_options):
    print 'starting deploy.....'
    # get all target ip for deploying
    ips = getIps(_options.config)
    # copy file into all ip
    for ip in ips:
        try:
            with SSHClient() as ssh:
                print("connect ip: ",ip," port: ",22," user: ",options.user, "pwd: ",_options.pwd)
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, 22, _options.user, _options.pwd)
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(_options.local_path, recursive=True, remote_path=_options.remote_path)
                print "deploy ip {} successful ", ip
        except Exception:
            print "deploy ip {} failure ",ip
            traceback.print_exc()

if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]', version='%prog 1.0')
    parser.add_option('--cmd', default='deploy', type='string', action='store', dest='cmd', help='deploy')
    parser.add_option('--host', default='localhost', type='string', action='store', dest='host', help='hostname (localhost)')
    parser.add_option('--port', default=1111, type='int', action='store', dest='port', help='port (1111)')
    parser.add_option('--pwd', default='test', type='string', action='store', dest='pwd', help='password')
    parser.add_option('--user', default='', type='string', action='store', dest='user', help='user')
    parser.add_option('--config', default='./config.txt', type='string', action='store', dest='config', help='config')
    parser.add_option('--local_path', default='', type='string', action='store', dest='local_path', help='local path')
    parser.add_option('--remote_path', default='.', type='string', action='store', dest='remote_path', help='remote path')

    (options, args) = parser.parse_args()
    if options.cmd == 'deploy':
        print("deploy")
        deploy(options)

