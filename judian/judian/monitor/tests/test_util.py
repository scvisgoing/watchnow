import unittest
import datetime
#import util # 若你執行的目錄是在 monitor底下這沒問題
from monitor import util # 我們現在執行 python manage.py test 是在 judian 目錄下

class TestUtil(unittest.TestCase):
    def test_Config(self):
        config_options = {
            'test_string': 'a string',
            'test_int': '3',
            'test_[int]': '1,2, 3',
            'test_[str]': 'a, b,c',
            'test_bool1': '1',
            'test_bool2': 'yes',
            'test_bool3': 'true',
            'test_bool4': 'on',
            'test_bool5': '0'
        }
        self.assertEqual(util.get_config_option(config_options, 'test_string'), 'a string')
        self.assertEqual(util.get_config_option(config_options, 'test_int', required_type='int'), 3)
        self.assertEqual(util.get_config_option(config_options, 'test_[int]', required_type='[int]'), [1, 2, 3])
        self.assertEqual(util.get_config_option(config_options, 'test_[str]', required_type='[str]'), ['a', 'b', 'c'])
        for i in list(range(1, 5)):
            self.assertEqual(util.get_config_option(config_options, f'test_bool{i}', required_type='bool'), True)
        self.assertEqual(util.get_config_option(config_options, 'test_bool5', required_type='bool'), False)
        # Raise test
        with self.assertRaises(ValueError):
            util.get_config_option(['not a dict'], '') # 第一個參數若非字典將引發例外
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'missing_key', required=True) # 傳入一個不存在的key卻又指定它為必要則引發例外
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_string', required_type='int') # 傳入個字串卻要將它轉成 int 會引發例外
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_string', required_type='float')
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_int', required_type='int', minimum=4) # 驗證 minimum
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_int', required_type='int', maximum=2) # 驗證 maximum
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_[str]', required_type='[int]') # 試圖'a,b,c'轉成 int list
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_[str]', required_type='[str]', allowed_values=['d']) # 測試 allowed_values for list
        with self.assertRaises(ValueError):
            util.get_config_option(config_options, 'test_string', allowed_values=['other string', 'other other string']) # 測試 allowed_values for string
        with self.assertRaises(NotImplementedError):
            util.get_config_option('not a dict', "doesn't matter", exception=NotImplementedError)
        with self.assertRaises(ValueError):
            util.get_config_option({'empty_string': ''}, 'empty_string', required_type='str', allow_empty=False)

        with self.assertRaises(util.MonitorConfigurationError):
            util.get_config_option('not a dict', "doesn't matter", exception=util.MonitorConfigurationError)

    def test_Format(self):
        self.assertEqual(util.format_datetime(None), "")
        self.assertEqual(util.format_datetime("a string"), "a string")
        self.assertEqual(
            util.format_datetime(datetime.datetime(2018, 5, 8, 13, 37, 0)),
            "2018-05-08 13:37:00"
        )

    # TODO : test util.get_config_dict(config, monitor)
    # TODO : test util.JSONEncoder class by json_dumps(data)
    # TODO : test util.JSONDecoder class by json_loads(string)
    # TODO : test util.subclass_dict_handler(mod, base_cls)
