Author: Karthik Puthraya
Email: karthik@puthraya.com

This is a simple Su-Do-Ku solver written in Python. The program uses a simple approach to reduce the current puzzle as much as possible without guessing. Upon hitting a dead-end, the program makes an informed guess. If the guess turns out to be inconsistent, the program backtracks and makes a different guess. 

Please email me to discuss any obvious improvements to the code. Thank you.

Usage: sudoku [-v] [FILE]

Each line in the FILE is interpreted to be an input puzzle.
Each of the 9 rows are appended to each to form a 81-character input puzzle
Unknown entries in the puzzle are denoted by a period(.)

Example: 
The following input line
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
solves the following puzzle

4 0 0 | 0 0 0 | 8 0 5
0 3 0 | 0 0 0 | 0 0 0
0 0 0 | 7 0 0 | 0 0 0
------+-------+------
0 2 0 | 0 0 0 | 0 6 0
0 0 0 | 0 8 0 | 4 0 0
0 0 0 | 0 1 0 | 0 0 0
------+-------+------
0 0 0 | 6 0 3 | 0 7 0
5 0 0 | 2 0 0 | 0 0 0
1 0 4 | 0 0 0 | 0 0 0

Use the -v flag to print the debug statements.
