import logging

from util import call, RunCommandError

logger = logging.getLogger(__name__)

def send_mail(subject, to, content='', tmpfile=None):
    if tmpfile:
        cmd = "(echo %s; cat %s) | mail -s %s %s" % (content, tmpfile, subject, to)
    else:
        cmd = "echo %s | mail -s %s %s" % (content, subject, to)
    try:
        call(cmd)
    except RunCommandError as err:
        logger.error('send mail failed, err: %s' % err)
