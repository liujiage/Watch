import unittest
import configparser

def getIps():
    ips = []
    with open('./res/file.txt') as f:
        # search [IP]
        for index in f:
            if index.strip().upper() == '[IP]': break
        # get all ip
        for ip in f:
            if len(ip.strip()) == 0: break;
            ips.append(ip.strip())
    return ips


class MyTestCase(unittest.TestCase):
    def test_read_config(self):
        parser = configparser.ConfigParser()
        parser.read('./res/config.txt')
        print(parser.sections())

    def test_read_file(self):
        f = open('./res/file.txt','r')
        for x in f:
            print(x)
        f.close()

    def test_read_ip(self):
        print getIps()


if __name__ == '__main__':
    unittest.main()
