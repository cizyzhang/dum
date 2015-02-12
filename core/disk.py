import os
import sys
import logging


sys.path.append(os.path.realpath(os.path.abspath("%s/../" % os.path.dirname(__file__))))
from util import call, RunCommandError, Configuration

from size_helper import size_parser, size_human_readable

logger = logging.getLogger(__name__)
config = Configuration('dum.cfg')


class DirHunter(object):
    """ Hunting those large directories, whose size over the specified
    """
    def __init__(self, mount_point):
        self._mount = mount_point
        self._maxsize = self._get_maxsize()

    def _get_maxsize(self):
        try:
            return size_parser(config.common.maxsize)
        except ValueError as err:
            logger.error("Parse size error: %s" % err)
            ### give a default size: 1G
            return 1024*1024*1024

    def gen_summary(self):
        summary = 'Summary of %s:\n' % self._mount
        for dir in sorted(os.listdir(self._mount)):
            size = self._get_dir_size(self._mount, dir)
            if not size:
                summary += '{:<12}'.format('-') + dir + '\n'
            else:
                summary += '{:<12}'.format(size_human_readable(size)) + dir + '\n'

        logger.info(summary)
        return summary

    def gen_detail(self):
        specified_dirs = [os.path.join(self._mount, dir)\
                          for dir in config.common.huntdirs.split()]

        detail = '\n'
        for dir in specified_dirs:
            detail += "Details of %s :\n" % dir
            logger.info("Hunt dirs of %s:" % dir)
            for subdir in sorted(os.listdir(dir)):
                if os.path.islink(os.path.join(dir, subdir)):
                    logger.debug("Ignore link file: %s" % subdir)
                    continue
                size = self._get_dir_size(dir, subdir)
                if not size:
                    logger.error("Unkown size of %s" % subdir)
                    detail += '{:<12}'.format('-') + subdir + '\n'
                if size > self._maxsize:
                    logger.info("Found large dir/file: %s" % subdir)
                    detail += '{:<12}'.format(size_human_readable(size)) + subdir + '\n'
        return detail


    def _get_dir_size(self, parent_dir, dir):
        ### Bug: If some subdir cann't be readable, it will print warning messages
        cmd = 'du -sb %s' % os.path.join(parent_dir, dir)
        try:
            return int(call(cmd).split()[0])
        except RunCommandError as err:
            logger.error("Run command failed: %s" % err)
            return None

