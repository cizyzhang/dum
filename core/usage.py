import os
import sys
import logging

sys.path.append(os.path.realpath(os.path.abspath("%s/../" % os.path.dirname(__file__))))
from util import call, RunCommandError

logger = logging.getLogger(__name__)

class DiskUsage(object):
    """ Use 'df -h' to get disk usage
    """
    def __init__(self, mount_point):
        self._mount = mount_point
        self._info = self._get_info()

    def _get_info(self):
        cmd = 'df -h | grep -w ' + self._mount
        try:
            output = call(cmd)
        except RunCommandError as err:
            logger.error('Call cmd [%s] failed, err: %s' % err)
        
        return output.split()


    def get_total(self):
        return self._info[0]

    def get_used(self):
        return self._info[1]

    def get_free(self):
        return self._info[2]

    def get_usage(self):
        return self._info[3]

