#!/usr/bin/env python
"""A more advanced Reducer, using Python iterators and generators."""

from itertools import groupby
from operator import itemgetter
import sys

POINT_DICT= {
        1:[],
        2:[],
        3:[]
    }

NEW_CENTERS={}

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)

    for point, group in data:
        x, y = point.split(",")
        POINT_DICT[int(group)].append((float(x),float(y)))
    
    for i in POINT_DICT:
        x = [p[0] for p in POINT_DICT[i]]
        y = [p[1] for p in POINT_DICT[i]]
        centroid = (sum(x) / len(POINT_DICT[i]), sum(y) / len(POINT_DICT[i]))
        NEW_CENTERS[i]= centroid
    
    for i in POINT_DICT:
        for k in POINT_DICT[i]:
            print '%s%s%s' % (k, separator, NEW_CENTERS[i])

if __name__ == "__main__":
    main()