# A-star_Search_Algo
Holds example code for the CS3353 Midterm I assignment (A* Search Algorithm)

## Build/Run Instructions

In order to build, simply enter the project directory and type the following command into your terminal of choice:

\> python3 a-star.py

## Input Grid

The input grid can in fact be edited to be a matrix of any size with any obstruction number/orientation. To edit the grid, locate the a-star.py file and edit the X_MAX and Y_MAX parameters at the top of the file with the length and width specifications of your grid. Once that step is completed, you are now able to edit the physical graph with any obstructions that you want to test. Scroll down to the gen-graph() method. Here, you can edit the grid however you please. A 0 represents a traversable cell while a 1 represents an obstruction.

## Output

The output of the prograph is through the console. Both the obstructions and shortest path will be shown. An 'X' represents and obstacle and an '*' represents a location on the shortest path.