# examples

This directory contains encoded mazes of classic micromouse competitions of several past years.

To decode the files, use `Maze.load(filepath)`. Maze class is defined in `core/maze.py`

## Encode format
* The first two bytes of each file contains the width of the maze
* The subsequent bytes are in binary, with each byte storing wall information of one cell
* The four Least Significant Bits of every byte contains the wall boolean in the following order - top, left, bottom, right(LSB)
