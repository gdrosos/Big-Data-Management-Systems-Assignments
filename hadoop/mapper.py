#!/usr/bin/env python
"""A more advanced Mapper, using Python iterators and generators."""

import sys
from scipy.spatial.distance import euclidean


CENTER1=(746.85881, 937.08133)
CENTER2=(738.38908, 61.71138)
CENTER3=(-534.54334, -977.20239)
CENTER_DICT = {CENTER1:1, CENTER2:2, CENTER3:3}

def read_input(file):
    for line in file:
        # split the line into words
        yield line.split()

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)
    for words in data:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        point = tuple([float(i) for i in words])
        center_mapper = {}
        center_mapper[CENTER1] = euclidean(point, CENTER1)
        center_mapper[CENTER2] = euclidean(point, CENTER2)
        center_mapper[CENTER3] = euclidean(point, CENTER3)
        center = min(center_mapper, key=center_mapper.get)
        output_point = ','.join(str(v) for v in list(point))
        #output_center = ','.join(str(v) for v in list(center))
        #print '%s%s%s' % (output_point, separator, output_center)
        print '%s%s%s' % (output_point, separator, CENTER_DICT.get(center))

if __name__ == "__main__":
    main()