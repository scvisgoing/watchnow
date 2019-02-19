"""
Test main function inside monitor.py
"""
import sys
import unittest

# python 3.4+ should use builtin unittest.mock not mock package
from unittest.mock import patch
#import configparser
# 因現在 D:\\learn2earn\\watchnow\\judian\\judian 是第一順位所以打 import monitor 它是套件(誰叫我們資料夾取這名)
from monitor import monitor #import monitor.monitor
#from monitor import util
from monitor.envconfig import EnvironmentAwareConfigParser
from monitor.util import get_config_dict

class TestMonitor(unittest.TestCase):
    """ (1) Test main config file, monitor config file is ok.
        (2) Test monitor.ini
        (3) Test quiet, verbose, debug
    """

    def test_config_file_exist(self):
        """Test if main config file and monitor config file exist"""
        # 故意丟個不存在的 main config file 應該會導致 sys.exit(1)
        with self.assertRaises(SystemExit):
            # 因為現在目錄是在 judian 下而非 monitor 下囉
            testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/nonexist.ini"]
            with patch.object(sys, 'argv', testargs):
                monitor.main()
        # main config file 沒填 interval 也會導致 sys.exit(1)
        with self.assertRaises(SystemExit):
            testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/monitor-nointerval.ini"]
            with patch.object(sys, 'argv', testargs):
                monitor.main()
        # 測試 monitor config 是否存在(simple.ini裡要指定 monitors 的值)
        testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/simple.ini"]
        with patch.object(sys, 'argv', testargs):
            result = monitor.main() # 現在先傳回 monitor config
            self.assertNotEqual(result, '', 'Wrong monitors setting file')
        # empty.ini contains wrong format
        with self.assertRaises(ValueError):
            testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/empty.ini"]
            with patch.object(sys, 'argv', testargs):
                monitor.main()
        # only test allow_pickle = SHIT to pass coverage
        with self.assertRaises(ValueError):
            testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/boolean.ini"]
            with patch.object(sys, 'argv', testargs):
                monitor.main()

    def test_monitor_ini(self):
        """test_monitor_ini"""
        config = EnvironmentAwareConfigParser()
        config.read('monitor/tests/mocks/ini/monitor.ini')
        self.assertEqual(config.getint("monitor", "interval"), 60)
        self.assertEqual(config.get("monitor", "monitors"), 'monitors.json')
        self.assertEqual(config.get("monitor", "thomasenv"), '100')
        print('GGGGGGGGG')
        with self.assertRaises(ValueError):
            config.get("monitor", "thomasxxx")
        with self.assertRaises(ValueError):
            config.getboolean("monitor", "allow_pickle", fallback='true')
        # 若要讀別的檔一定要再生成一個 configParser
        config = EnvironmentAwareConfigParser() # 光有下面那行不行
        config.read('monitor/tests/mocks/ini/simple.ini')
        self.assertIn('interval', get_config_dict(config, "monitor"))
        

    def test_main_arguments(self):
        """Test monitor.py arguments"""
        # -q,--quiet不會印出東西
        testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/simple.ini", "--quiet"]
        with patch.object(sys, 'argv', testargs):
            monitor.main()
        # -v,--verbose會印出東西
        testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/simple.ini", "--verbose"]
        with patch.object(sys, 'argv', testargs):
            monitor.main()
        # -d,--debug會印出東西
        testargs = ["monitor.py", "-f", "monitor/tests/mocks/ini/simple.ini", "--debug"]
        with patch.object(sys, 'argv', testargs):
            monitor.main()
# TODO : test monitor config file (monitors.ini / monitors.json),
# that about class Monitor & class Loggers
