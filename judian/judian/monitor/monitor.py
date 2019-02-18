#! python3
# coding: utf-8
import os, sys
from optparse import OptionParser, SUPPRESS_HELP
#import austinlog # 2019/1/25 定義一個 sm_logger 給 simplemonitor 用
from monitor.austinlog import SM_LOGGER as sm_logger
from monitor.envconfig import EnvironmentAwareConfigParser

VERSION = "1.7"

def program_start_options():
    # 2019/1/24 simplemonitor migrate
    parser = OptionParser() # https://blog.csdn.net/dcrmg/article/details/78045570
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help=SUPPRESS_HELP)
    parser.add_option("-q", "--quiet",   action="store_true", dest="quiet",   default=False, help=SUPPRESS_HELP)
    parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help=SUPPRESS_HELP)
    parser.add_option("-f", "--config", dest="config", default="monitor.ini", help="configuration file")
    parser.add_option('-l', '--log-level', dest="loglevel", default="warn", help="Log level: critical, error, warn, info, debug")
    parser.add_option("-t", "--test",    action="store_true", dest="test",    default=False, help="Test config and exit")
    #parser.add_option("-N", "--no-network", dest="no_network", default=False, action="store_true", help="Disable network listening socket")
    parser.add_option("-H", "--no-heartbeat", action="store_true", dest="no_heartbeat", default=False, help="Omit printing the '.' character when running checks")
    parser.add_option('-1', '--one-shot', action='store_true', dest='one_shot', default=False, help='Run the monitors once only, without alerting. Require monitors without "fail" in the name to succeed. Exit zero or non-zero accordingly.')
    parser.add_option('--loops', dest='loops', default=-1, help=SUPPRESS_HELP, type=int)
    
    # below is useless
    #parser.add_option('-C', '--no-colour', '--no-color', action='store_true', dest='no_colour', default=False, help='Do not colourise log output')
    #parser.add_option('--no-timestamps', action='store_true', dest='no_timestamps', default=False, help='Do not prefix log output with timestamps')
    #parser.add_option("-p", "--pidfile", dest="pidfile", default=None, help="Write PID into this file")
    #parser.add_option("-f", "--file", dest="filename", metavar="FILE", help="write report to FILE")
    (options, args) = parser.parse_args()
    if options.quiet:
        #print('Warning: --quiet is deprecated; use --log-level=critical')
        options.loglevel = 'critical'
    if options.verbose:
        #print('Warning: --verbose is deprecated; use --log-level=info')
        options.loglevel = 'info'
    if options.debug:
        #print('Warning: --debug is deprecated; use --log-level=debug')
        options.loglevel = 'debug'

    sm_logger.setLevel(options.loglevel.upper())

    if not options.quiet:
        sm_logger.info('=== JudianMonitor v%s', VERSION)
        sm_logger.info('Loading main config from %s', options.config)
    if not os.path.exists(options.config):
        sm_logger.critical('Configuration file "%s" does not exist!', options.config)
        sys.exit(1)
    config = EnvironmentAwareConfigParser()
    try:
        config.read(options.config) # 準備 monitor.ini
    except Exception as e:
        sm_logger.critical('Unable to read configuration file')
        sm_logger.critical(e)
        sys.exit(1)

    try:
        interval = config.getint("monitor", "interval")
    except Exception:
        sm_logger.critical('Missing [monitor] section from config file, or missing the "interval" setting in it')
        sys.exit(1) # interval = 60

    if config.has_option("monitor", "monitors"):
        monitors_file = config.get("monitor", "monitors")
    else:
        monitors_file = "monitors.ini"

    sm_logger.info("Loading monitor config from %s", monitors_file)

    try:
        allow_pickle = config.getboolean("monitor", "allow_pickle", fallback='true')
    except ValueError:
        sm_logger.critical('allow_pickle should be "true" or "false".')
        sys.exit(1)
    return allow_pickle, monitors_file, config, options, interval

def main():
    r"""This is where it happens \o/"""
    allow_pickle, monitors_file, config, options, interval = program_start_options()
    print()
    return monitors_file







if __name__ == "__main__":
    main()

