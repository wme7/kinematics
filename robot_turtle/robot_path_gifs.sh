#! /bin/bash

for path in path/data/*.csv; do
    path_name=$(basename $path .csv)
    uv run python robot_path.py -p $path --gif $path_name.gif --fps 24
done