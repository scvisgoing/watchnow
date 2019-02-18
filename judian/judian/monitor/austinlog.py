#! python3
"""
Logger setting, this may change in future since it may move to the django settings

Here we just want to learn about the usage
"""
import logging
import datetime
# 基礎設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
                    #,handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
# basicConfig() also have a filename parameter to specify log file name.

# 定義 handler 輸出 sys.stderr
CONSOLE = logging.StreamHandler()
CONSOLE.setLevel(logging.INFO)
CONSOLE.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
# 加入 hander 到 root logger
ROOT_LOGGER = logging.getLogger(__name__)
ROOT_LOGGER.addHandler(CONSOLE)
# We let the log file has dynamic name
NOW = datetime.datetime.now().strftime('%Y-%m-%d %I-%M-%S') # '2018-12-27 03-19-50'
ROOT_LOGGER.addHandler(logging.FileHandler('austinlog_'+NOW+'.log', 'w', 'utf-8'))

# root 輸出
logging.info('austin loggin.info ok')

# 定義另兩個 logger
LOGGER1 = logging.getLogger('myapp.area1')
LOGGER2 = logging.getLogger('myapp.area2')

LOGGER1.debug('天高地遠')
LOGGER1.info('天龍地虎')
LOGGER2.warning('天發殺機')
LOGGER2.error('地動天搖')

# simplemonitor logger
SM_LOGGER = logging.getLogger('simplemonitor')
