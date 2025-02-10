import re


def filter_ascii(string):
    ascii_pattern = re.compile(r'[^\x00-\x7F]')
    return ascii_pattern.sub('', string)
