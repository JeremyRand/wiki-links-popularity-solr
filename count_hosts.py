#!/usr/bin/python3

from collections import Counter
from itertools import chain
from ast import literal_eval
from urllib.parse import urlparse
import sys

RELEVANT_LINE_START = "INSERT INTO `externallinks` VALUES "
RELEVANT_LINE_END = ";"

LINE_START_POSITION = len(RELEVANT_LINE_START)
LINE_END_POSITION = -1-len(RELEVANT_LINE_END)

def relevant_line(line):
    """Determine whether a MySQL external_links line is relevant for calculating frequency counts.

    Keyword arguments:
    line -- the line to check
    """
    return line.startswith(RELEVANT_LINE_START)

def line_generator(data):
    """Converts a MediaWiki MySQL external_links dump into a generator of lists of tuples.

    Keyword arguments:
    data -- the file object to read data from (e.g. sys.stdin)
    """
    return ((literal_eval("[" + line[LINE_START_POSITION:LINE_END_POSITION] + "]") if
             relevant_line(line) else []) for line in data)

# TODO: check whether port numbers in the URL are handled properly.
def host_generator(line):
    """Converts a list of external_links tuples into a generator of hostnames

    Keyword arguments:
    line -- the list of external_links tuples to convert
    """
    return (urlparse(row[3]).hostname for row in line)

def count_hosts_in_dump(data):
    """Converts a MediaWiki MySQL external_links dump into a Counter of hostname frequencies.

    Keyword arguments:
    data -- the file object to read data from (e.g. sys.stdin)
    """
    line_hosts = (host_generator(line) for line in line_generator(data))
    return Counter(chain.from_iterable(line_hosts))

RESULTS = count_hosts_in_dump(sys.stdin)

if None in RESULTS:
    del RESULTS[None]

# TODO: maybe divide all entries by the sum of all entries?  (So they all sum to 1.0)
# TODO: or maybe calculate percentile-like scores?

for host in sorted(RESULTS):
    print(host + "=" + str(RESULTS[host]) + ".0")

