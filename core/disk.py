import os
import logging

from util import call, RunCommandError, Configuration

from size_helper import size_parser, size_converter

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
            return size_parser(config.comman.maxsize)
        except ValueError as err:
            logger.error("Parse size error: %s" % err)
            ### give a default size: 1G
            return 1024*1024*1024

    def gen_summary(self):
        summary = 'Summary of %s:\n' % self._mount
        for dir in os.lsdir(self._mount):
            size = self._get_dir_size(self._mount, dir)
            if not size:
                summary += '-\t %s\n' % dir
            else:
                summary += '%s\t %s\n' % (str(size_converter(size, 'G'))+'G', dir)

        logger.info(summary)
        return summary

    def gen_huntdir(self):
        specified_dirs = [os.path.join(self._mount, dir)\
                          for dir in config.common.huntdirs.strip()]

        detail = ''
        for dir in specified_dirs:
            detail += dir
            logger.info("Hunt dirs of %s:" % dir)
            for subdir in os.listdir(dir):
                if os.path.islink(os.path.join(dir, subdir)):
                    logger.debug("Ignore link file: %s" % subdir)
                    continue
                size = self._get_dir_size(dir, subdir)
                if not size:
                    logger.error("Unkown size of %s" % subdir)
                    continue
                if size > self._maxsize:
                    logger.info("Found large dir/file: %s" % subdir)
                    detail += '%s\t %s\n' % (str(size_converter(size, 'G'))+'G', subdir)
        return detail


    def _get_dir_size(self, parent_dir, dir):
        cmd = 'du -sb %s' % os.path.join(dir, subdir)
        try:
            return call(cmd).strip()
        except RunCommandError as err:
            logger.error("Run command failed: %s" % err)
            return ''

