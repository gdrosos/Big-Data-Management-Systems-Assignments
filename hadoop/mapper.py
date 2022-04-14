#!/usr/bin/env python
"""A Python Mapper, using Python iterators and generators."""

import sys
import math

center_dict = {}

def read_input(file):
    for line in file:
        yield line.replace("\n", "").split(" ")

def read_centers():
    with open("input/centers.txt", "r") as f:
        center1 = f.readline().strip().split(" ")
        center1 = tuple([float(i) for i in center1])
        center2 = f.readline().strip().split(" ")
        center2 = tuple([float(i) for i in center2])
        center3 = f.readline().strip().split(" ")
        center3 = tuple([float(i) for i in center3])
    return center1, center2, center3

def euclidean(p1, p2):
    return math.sqrt(abs(p1[0] - p2[0])**2 + abs(p1[1] - p2[1])**2)

def main(separator='\t'):
    c1, c2, c3 = read_centers()
    center_dict = {c1:1, c2:2, c3:3}
    data = read_input(sys.stdin)
    for words in data:
        point = tuple([float(i) for i in words])
        center_mapper = {}
        center_mapper[c1] = euclidean(point, c1)
        center_mapper[c2] = euclidean(point, c2)
        center_mapper[c3] = euclidean(point, c3)
        center = min(center_mapper, key=center_mapper.get)
        output_point = ','.join(str(v) for v in list(point))
        print(f"{output_point}{separator}{center_dict.get(center)}")

if __name__ == "__main__":
    main()

