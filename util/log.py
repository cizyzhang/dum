import logging


def set_log(file=None, level=logging.DEBUG):
    msgfmt = '[%(levelname)7s][%(asctime)s][%(lineno)4d] <%(name)s> %(message)s'
    datafmt = '%m/%d/%Y %I:%M:%S %p'

    if filen is None:
        logging.basicConfig(format=msgfmt, datafmt=datafmt, level=level)
    else:
        logging.basicConfig(format=msgfmt, datafmt=datafmt, level=level, filename=file)
