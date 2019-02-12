#! python3

import logging
import datetime
# 基礎設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
                    #,handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
# basicConfig() also have a filename parameter to specify log file name.
 
# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
# 加入 hander 到 root logger
root_logger = logging.getLogger(__name__)
root_logger.addHandler(console)
# We let the log file has dynamic name
now = datetime.datetime.now().strftime('%Y-%m-%d %I-%M-%S') # '2018-12-27 03-19-50'
root_logger.addHandler(logging.FileHandler('austinlog_'+now+'.log', 'w', 'utf-8'))
 
# root 輸出
logging.info('austin loggin.info ok')
 
# 定義另兩個 logger
logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')
 
logger1.debug('天高地遠')
logger1.info('天龍地虎')
logger2.warning('天發殺機')
logger2.error('地動天搖')

# simplemonitor logger
sm_logger = logging.getLogger('simplemonitor')
