import os
import sys
import logging

sys.path.append(os.path.realpath(os.path.abspath("%s/../" % os.path.dirname(__file__))))
from util import call, RunCommandError

logger = logging.getLogger(__name__)

def send_mail(subject, to, content='', tmpfile=None):
    if tmpfile:
        cmd = "(echo \"%s\"; cat %s) | mail -s \"%s\" %s" % (content, tmpfile, subject, to)
    else:
        cmd = "echo \"%s\" | mail -s \"%s\" %s" % (content, subject, to)
    try:
        call(cmd)
    except RunCommandError as err:
        logger.error('send mail failed, err: %s' % err)
