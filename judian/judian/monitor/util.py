#! python3
import re
import sys
import json
import datetime
import socket

class MonitorConfigurationError(ValueError):
    """A config error for a Monitor"""
    pass

class AlerterConfigurationError(ValueError):
    """A config error for an Alerter"""
    pass

class LoggerConfigurationError(ValueError):
    """A config error for a Logger"""
    pass

class SimpleMonitorConfigurationError(ValueError):
    """A general config error"""
    pass


def get_config_dict(config, section):
    """將 section 裡的 option name / value 變成 dict"""
    options = config.items(section)
    ret = {}
    for (key, value) in options:
        ret[key] = value
    return ret

def subclass_dict_handler(mod, base_cls):
    def _check_is_subclass(cls):
        if not issubclass(cls, base_cls):
            raise TypeError(('%s.register may only be used on subclasses '
                             'of %s.%s') % (mod, mod, base_cls.__name__))

    _subclasses = {}

    def register(cls):
        """Decorator for monitor classes."""
        _check_is_subclass(cls)
        assert cls.type != "unknown", cls
        _subclasses[cls.type] = cls
        return cls

    def get_class(type_):
        return _subclasses[type_]

    def all_types():
        return list(_subclasses)

    return (register, get_class, all_types)

def get_config_option(config_options, key, **kwargs):
    """Get a value out of a dict, with possible default, required type and requiredness."""
    exception = kwargs.get('exception', ValueError)

    if not isinstance(config_options, dict):
        raise exception('config_options should be a dict')

    default = kwargs.get('default', None)
    required = kwargs.get('required', False)
    value = config_options.get(key, default)
    if required and value is None:
        raise exception('config option {0} is missing and is required'.format(key))
    required_type = kwargs.get('required_type', 'str')
    allowed_values = kwargs.get('allowed_values', None)
    allow_empty = kwargs.get('allow_empty', True)
    if isinstance(value, str) and required_type:
        if required_type == 'str' and value == '' and not allow_empty:
            raise exception('config option {0} cannot be empty'.format(key))
        if required_type in ['int', 'float']:
            try:
                if required_type == 'int':
                    value = int(value)
                else:
                    value = float(value)
            except ValueError:
                raise exception('config option {0} needs to be an {1}'.format(key, required_type))
            # verify minimum & maximum
            minimum = kwargs.get('minimum')
            if minimum is not None and value < minimum:
                raise exception('config option {0} needs to be >= {1}'.format(key, minimum))
            maximum = kwargs.get('maximum')
            if maximum is not None and value > maximum:
                raise exception('config option {0} needs to be <= {1}'.format(key, maximum))
        elif required_type == '[int]':
            try:
                value = [int(x) for x in value.split(",")]
            except ValueError:
                raise exception('config option {0} needs to be a list of int[int,...]'.format(key))
        elif required_type == 'bool':
            value = bool(value.lower() in ['1', 'true', 'yes', 'on'])
        elif required_type == '[str]':
            value = [x.strip() for x in value.split(",")]
    if isinstance(value, list) and allowed_values:
        if not all([x in allowed_values for x in value]):
            raise exception('config option {0} needs to be one of {1}'.format(key, allowed_values))
    else:
        if allowed_values is not None and value not in allowed_values:
            raise exception('config option {0} needs to be one of {1}'.format(key, allowed_values))
    return value

def short_hostname():
    """Get just our machine name.

    TODO: This might actually be redundant. Python probably provides it's own version of this."""
    # 把名字中的 '.' 都去掉只傳回第一部份，如 'abc.def.01' 只回傳 'abc'
    # 若名字無 '.' 則不影響
    return (socket.gethostname() + ".").split(".")[0] # 'A.B.C' 只取 'A'

def format_datetime(the_datetime):
    """Return an isoformat()-like datetime without the microseconds."""
    if the_datetime is None:
        return ""

    if isinstance(the_datetime, datetime.datetime):
        the_datetime = the_datetime.replace(microsecond=0)
        return the_datetime.isoformat(' ') # '2019-01-28 14:42:50'
    return the_datetime

DATETIME_MAGIC_TOKEN = '__simplemonitor_datetime'
FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class JSONEncoder(json.JSONEncoder):
    _regexp_type = type(re.compile(''))

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {DATETIME_MAGIC_TOKEN: obj.strftime(FORMAT)}
        if isinstance(obj, self._regexp_type):
            return "<removed compiled regexp object>"
        return super(JSONEncoder, self).default(obj)

class JSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self._original_object_pairs_hook = kwargs.pop('object_pairs_hook', None)
        kwargs['object_pairs_hook'] = self.object_pairs_hook
        super(JSONDecoder, self).__init__(*args, **kwargs)

    _datetime_re = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}')

    def object_pairs_hook(self, obj):
        if len(obj) == 1 and obj[0][0] == DATETIME_MAGIC_TOKEN and \
                isinstance(obj[0][1], str) and \
                self._datetime_re.match(obj[0][1]):
            return datetime.datetime.strptime(obj[0][1], FORMAT)
        elif self._original_object_pairs_hook:
            return self._original_object_pairs_hook(obj)
        else:
            return dict(obj)


def json_dumps(data):
    return JSONEncoder().encode(data).encode('ascii')

def json_loads(string):
    return JSONDecoder().decode(string.decode('ascii'))

if __name__ == '__main__':
    config_options = {
        'test_string': 'a string',
        'test_int': '3',
        'test_[int]': '1,2, 3',
        'test_[str]': 'a, b,c',
        'test_bool1': '1',
        'test_bool2': 'yes',
        'test_bool3': 'true',
        'test_bool4': '0'
    }
    #ret1 = get_config_option(config_options, 'test_string')
    #ret2 = get_config_option(config_options, 'test_int', required_type='int')
    #ret3 = get_config_option(config_options, 'test_[int]', required_type='[int]')
    #ret4 = get_config_option(config_options, 'test_[str]', required_type='[str]')
    #for i in list(range(1, 4)):
    #    ret5 = get_config_option(config_options, f'test_bool{i}', required_type='bool')
    #ret6 = get_config_option(['not a dict'], '')
    #ret7 = get_config_option(config_options, 'missing_value', required=True)
    #ret8 = get_config_option(config_options, 'test_string', required_type='int')
    #ret9 = get_config_option(config_options, 'test_string', required_type='float')
    #ret10 = get_config_option(config_options, 'test_int', required_type='int', minimum=4)
    #ret11 = get_config_option(config_options, 'test_int', required_type='int', maximum=2)
    #ret12 = get_config_option(config_options, 'test_[str]', required_type='[int]')
    #ret13 = get_config_option(config_options, 'test_[str]', required_type='[str]', allowed_values=['d'])
    #ret14 = get_config_option(config_options, 'test_string', allowed_values=['other string', 'other other string'])
    ret15 = get_config_option({'empty_string': ''}, 'empty_string', required_type='str', allow_empty=False)
    print()
