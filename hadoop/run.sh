#!/bin/bash


# hadoop dfs -copyFromLocal /Users/gdrosos/Desktop/Damianos/HadoopAssignment /user/gdrosos/HadoopAssignment/
# hadoop fs -mkdir /user/gdrosos/HadoopAssignment/input
#  hadoop fs -mkdir /user/gdrosos/HadoopAssignment/output
# hadoop dfs -copyFromLocal /Users/gdrosos/Desktop/Damianos/Big-Data-Management-Systems-Assignments/hadoop/points.txt /user/gdrosos/HadoopAssignment/input/data.txt


hadoop  jar /opt/homebrew/Cellar/hadoop/3.3.2/libexec/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
-file /user/gdrosos/HadoopAssignment/mapper.py    -mapper /user/gdrosos/HadoopAssignment/mapper.py\
-file /user/gdrosos/HadoopAssignment/reducer.py   -reducer /user/gdrosos/HadoopAssignment/reducer.py \
-input /user/gdrosos/HadoopAssignment/input/*  -output /user/gdrosos/HadoopAssignment/output

# hadoop  jar /opt/homebrew/Cellar/hadoop/3.3.2/libexec/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
#     -mapper /user/gdrosos/HadoopAssignment/mapper.py\
#   -reducer /user/gdrosos/HadoopAssignment/reducer.py \
# -input /user/gdrosos/HadoopAssignment/points.txt -output /user/gdrosos/HadoopAssignment/output.txt