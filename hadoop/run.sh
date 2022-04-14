#!/bin/bash
bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar \
-file mapper.py \
-file reducer.py \
-mapper "python mapper.py" \
-reducer "python reducer.py" \
-input input/points.txt \
-output output
