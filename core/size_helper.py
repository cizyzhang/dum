
unit_to_bytes = {'B':1, 'K':1024, 'M':1024*1024,
                 'G':1024*1024*1024, 'T':1024*1024*1024*1024}

def size_parser(size_str):
    """ Parse the size(a string type, with unit) to bytes
    """
    size = float(size_str.strip(' BKMGT'))
    unit = size_str.strip()[-1]
    if unit not in 'BKMGT':
        raise ValueError("Unkown size unit. %s" % size_str)
    else:
        return size * unit_to_bytes[unit]

def size_converter(size, unit):
    """ Convert the size base on bytes to other units
    """
    return round(float(size)/unit_to_bytes[unit], 2)

def size_human_readable(size):
    """ Return a human readable size which near to
        the given size based on Byte
    """
    for unit in 'TGMKB':
        if size >= unit_to_bytes[unit]:
            return str(size_converter(size, unit)) + unit
    return str(size) + 'B'
