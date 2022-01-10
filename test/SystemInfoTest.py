import unittest
import psutil
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(psutil.cpu_percent(interval=1))
        print(psutil.virtual_memory().percent)
        print(psutil.virtual_memory().available / 1024 / 1024)
        print(psutil.virtual_memory().total / 1024 / 1024)

    def test_os(self):
        CPU_Pct = round(float(os.popen(
            '''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()), 2)
        print("CPU Usage: " + str(CPU_Pct))
        tot_m, used_m, free_m = map(float, os.popen('free -t -m').readlines()[-1].split()[1:])

    def test(self):
        total = float(70)
        used = float(100)
        print(total / used)

    def test2(self):
        print("::ffff:10.30.0.30".replace("::ffff:",""))



if __name__ == '__main__':
    unittest.main()
