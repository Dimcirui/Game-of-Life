# Game of Life  
## Brief Discription to the Rules  
We call a square in the board a 'cell', each of which is in one of the 2 possible states, live or dead.  
Every cell interacts with it's 8 neighbors around.  
Here's how a cell interacts with its neighbors at each step:  
1.Any dead cell with exactly three live neighbours becomes a live cell.  
2.Any cell with two or three live neighbours keeps its states.  
3.In other cases, any cell keeps dead (no matter whether it's live or dead).
## Basic Functions:  
1.Simplified GUI  
2.Customize board size  
3.Customize number of initial live cells  
4.Several basic graphics  
5.Allowing live cell addition and deletion in the game  
## Known Bugs:  
No one yet  
## Change Log:   
### [1.0.2] - 2020-11-12  
+ Optimized interface layout  
+ Fixed bug: Gosper Glider Gun cannot run normally  
### [1.0.1] - 2020-11-12
+ Fixed bug: When the "Add/Delete Live Cells" function is enabled, clicking other buttons will cause additional cells to be added/deleted in the upper left corner of the game interface. 
### [1.0.0] - 2020-11-12  
+ Added simplified GUI  
+ Added several basic graphics  
+ Added rule description  
+ Live cells are now allowed to be added and removed during gameplay  
- Removed terminal interface  
### [0.0.1] - 2020-6-21  
+ Created this project   
