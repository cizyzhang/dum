#!/app/python/2.7.1/RHEL64/bin/python2.7

""" This script is used to monitor the usage of disk.
    It will print or send a message if disk's usage bigger than you give.
"""

import os
import argparse
import logging

from util import set_log, Configuration

from core.disk import DirHunter, DiskUsage
from core.mailbox import send_mail


config = Configuration('dum.cfg')


def parse_arguments():
    parser = argparse.ArgumentParser('dum.py',
                                     description = 'Disk Usage Monitor ...')
    parser.add_argument('-m', '--mount', dest='mount', type=str, required=True,
                        help='full path of mount point')
    parser.add_argument('-u', '--usage', dest='usage', type=str, required=True,
                        help='the warning usage line')
    parser.add_argument('-l', '--log', dest='log', default=False, action='store_true',
                        help='enable log function')

    return parser.parse_args()


def cmp_usage(usage1, usage2):
    """ These two arguments' type is string.
        Return true if usage1 > usage2, else return false
    """
    return int(usage1.split('%')[0]) > int(usage2.split('%')[0])


def gen_content(mount_point):
    dir_hunter = DirHunter(mount_point)
    return dir_hunter.gen_detail()
#    return dir_hunter.gen_summary() + dir_hunter.gen_detail()


def main():
    args = parse_arguments()
    if args.log:
        set_log(config.log.path)
    
    logging.info("Beginning of Disk usage monitor ...")
    try:
        disk_usage = DiskUsage(args.mount)
        if cmp_usage(disk_usage.get_usage(), args.usage):
            logging.info("Disk usage[%s] is over the warning line[%s]." %\
                         (disk_usage.get_usage(), args.usage))
            send_mail(subject = '[Warning] %s space has been used of %s' % (disk_usage.get_usage(), args.mount),
                      to = config.maillist.subscribers,
                      content = gen_content(args.mount))

    except Exception as err:
        logging.error("Error message: %s" % err)
    finally:
        logging.info("Ending of Disk usage monitor ...")


if __name__ == "__main__":
    main()
