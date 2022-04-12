#!/usr/bin/env python
"""A Python Mapper, using Python iterators and generators."""

import sys
import math

CENTER1=(746.85881, 937.08133)
CENTER2=(738.38908, 61.71138)
CENTER3=(-534.54334, -977.20239)
CENTER_DICT = {CENTER1:1, CENTER2:2, CENTER3:3}

def read_input(file):
    for line in file:
        yield line.replace("\n", "").split(" ")

def euclidean(p1, p2):
    return math.sqrt(abs(p1[0] - p2[0])**2 + abs(p1[1] - p2[1])**2)

def main(separator='\t'):
    data = read_input(sys.stdin)
    for words in data:
        point = tuple([float(i) for i in words])
        center_mapper = {}
        center_mapper[CENTER1] = euclidean(point, CENTER1)
        center_mapper[CENTER2] = euclidean(point, CENTER2)
        center_mapper[CENTER3] = euclidean(point, CENTER3)
        center = min(center_mapper, key=center_mapper.get)
        output_point = ','.join(str(v) for v in list(point))
        print(f"{output_point}{separator}{CENTER_DICT.get(center)}")


if __name__ == "__main__":
    main()
