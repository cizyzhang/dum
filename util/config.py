import os
from ConfigParser import ConfigParser

def get_config_path(filename):
    return os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', filename)

class Configuration(object):
    """ This class is used to parse configure file.
        You can get an item like this:
            config = Configuration('dum.cfg')
            config.common.file  ==>  '/root/test'
    """
    def __init__(self, filename):
        config_file = get_config_path(filename)
        self._config = ConfigParser()
        self._config.read(config_file)

    def __getattr__(self, section):
        if self._config.has_section(section):
            return Section(self._config, section)
        else:
            return object.__getattribute__(self, section)


class Section(object):
    """ This is a section in the configuration file. It is
        seperated from the Configuration class to improve clarity.
    """

    def __init__(self, config, section):
        self._config = config
        self._section = section

    def __getattr__(self, attribute):
        if attribute in self._config.options(self._section):
            return self._config.get(self._section, attribute)
        else:
            return object.__getattribute__(self, attribute)

    def get_boolean(self, attribute):
        return self._config.getboolean(self._section, attribute)
