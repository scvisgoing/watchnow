#! python3
"""
用來解析 INI 檔
config = EnvironmentAwareConfigParser()
try:
    config.read(options.config)
except Exception as e:
    print(...)
"""
import os
import re
import functools
from configparser import ConfigParser, NoSectionError, NoOptionError
from configparser import BasicInterpolation

class EnvironmentAwareInterpolation(BasicInterpolation):
    r = re.compile('%env:([a-zA-Z0-9_]+)%')

    def before_get(self, parser, section, option, value, defaults):
        parser.get(section, option, raw=True, fallback=value)
        matches = self.r.search(value)
        old_value = value
        while matches:
            env_key = matches.group(1)
            if env_key in os.environ:
                value = value.replace(matches.group(0), os.environ[env_key])
            else:
                raise ValueError('Cannot find {0} in environment for config interpolation'.format(env_key))
            matches = self.r.search(value)
            if value == old_value:
                break
            old_value = value
        return value

class EnvironmentAwareConfigParser(ConfigParser):
    """A subclass of ConfigParser which allows %env:VAR% interpolation via the
    get method."""

    r = re.compile('%env:([a-zA-Z0-9_]+)%')

    def __init__(self, *args, **kwargs):
        """Init with our specific interpolation class (for Python 3)"""
        interpolation = EnvironmentAwareInterpolation()
        kwargs['interpolation'] = interpolation
        ConfigParser.__init__(self, *args, **kwargs)

    def read(self, filenames):
        """Load a config file and do environment variable interpolation on the section names."""
        result = ConfigParser.read(self, filenames)
        for section in self.sections():
            original_section = section
            matches = self.r.search(section)
            while matches:
                env_key = matches.group(1)
                if env_key in os.environ:
                    section = section.replace(matches.group(0), os.environ[env_key])
                else:
                    raise ValueError('Cannot find {0} in environment for config interpolation'.format(env_key))

                matches = self.r.search(section)
            if section != original_section:
                self.add_section(section)
                for (option, value) in self.items(original_section):
                    self.set(section, option, value)
                self.remove_section(original_section)
        return result

    def get(self, *args, **kwargs):
        return ConfigParser.get(self, *args, **kwargs)
