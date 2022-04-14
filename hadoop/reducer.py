#!/usr/bin/env python
"""A more advanced Reducer, using Python iterators and generators."""

import sys

point_dict= {
        1:[],
        2:[],
        3:[]
    }

new_centers={}

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)

    for point, group in data:
        x, y = point.split(",")
        point_dict[int(group)].append((float(x),float(y)))
    
    for i in point_dict:
        x = [p[0] for p in point_dict[i]]
        y = [p[1] for p in point_dict[i]]
        centroid = (sum(x) / len(point_dict[i]), sum(y) / len(point_dict[i]))
        new_centers[i]= centroid
    
    for i in point_dict:
            print(f"{i}{separator}{new_centers[i]}")

if __name__ == "__main__":
    main()
