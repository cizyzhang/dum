import commands

def call(cmd):
    """ Call a command, return the output
    """
    status, output = commands.getstatusoutput(cmd)
    if status:
        raise CommandFailException("Call command [%s] failed: %d" % (cmd, status))
    else:
        return ' '.join(output.split())


class CallCommandError(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
