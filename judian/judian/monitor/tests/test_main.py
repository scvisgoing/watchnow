import sys
import unittest

# python 3.4+ should use builtin unittest.mock not mock package
from unittest.mock import patch
import configparser
# 因現在 D:\\learn2earn\\watchnow\\judian\\judian 是第一順位所以打 import monitor 它是套件(誰叫我們資料夾取這名)
from monitor import monitor #import monitor.monitor
from monitor import util

class TestMonitor(unittest.TestCase):

    def test_MonitorConfigInterval(self):
        # 故意丟個不存在的 main config file 應該會導致 sys.exit(1)
        with self.assertRaises(SystemExit):
            testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/nonexist.ini"] # 因為現在目錄是在 judian 下而非 monitor 下囉
            with patch.object(sys, 'argv', testargs):
                monitor.main()
        # main config file 沒填 interval 也會導致 sys.exit(1)
        with self.assertRaises(SystemExit):
            testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/monitor-nointerval.ini"]
            with patch.object(sys, 'argv', testargs):
                monitor.main()
        # 測試 monitor config 是否存在
        testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/monitor.ini"]
        with patch.object(sys, 'argv', testargs):
            result = monitor.main() # 現在先傳回 monitor config
            self.assertNotEqual(result, '', 'Wrong monitors setting file')

    # TODO : test monitor config file (monitors.ini / monitors.json), that about class Monitor & class Loggers

