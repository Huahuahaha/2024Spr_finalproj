## Super Xiangqi 

Group Member: Jintao Cao, Xicheng Guo

## Game Rules:
![alt text](images/Board.png)

Traindiontal rules cite form(https://en.wikipedia.org/wiki/Xiangqi)

![alt text](images/Rules1.png)
![alt text](images/Rules2.png)
![alt text](images/Rules3.png)
Super Piece:
      巨将/巨帅 occupy four points. They move and capture by advancing one point. However, they can eat multiple pieces at one time because they occupy four points. Other pieces can eat them when either of the points of 巨将/巨帅 is occupied.
## Program guide:
Our program can fight both with AI and your friends. Players type into their piece row and column coordinates and their target position.

![alt text](images/demo.png)

## Complexity of heuristic evaluation function：
# Heuristic evaluation function ('calculate()')：
This function iterates through every cell on the game board to calculate a score. For each cell, it checks if the cell is empty or a wall, and if not, it assigns a score based on the type of piece and additional game state considerations (like the total number of pieces).
Assuming the board is of size 𝑁×M(Our actual game board is 9×10+8), the function performs a constant amount of work for each cell, resulting in a time complexity of O(N^2).
  
# All Legal Moves ('game.get_all_moves()'):
The complexity of this function depends on how it identifies legal actions. For the game Xiangqi, identifying whether an action is legal requires analyzing three aspects.
The first is to choose whether there is a chess piece in the original position of the moved chess piece. This can be understood as whether the user selects the wrong initial position of the chess piece. In our code, get_start_location() plays a role in identifying this situation. Its complexity is O(1).
The second is to choose whether the target position of moving the chess piece is legal. In our code, get_end_location() plays a role in identifying this situation. Its complexity is O(1).
The third is to choose a way to move the chess pieces that conforms to the movement rules of the corresponding chess pieces. In our code, independent movement codes are written for each type of chess piece, and the code get_all_moves() is used to count and record the positions of the remaining chess pieces on the chessboard that can be moved before each movement. When a move occurs, the program goes back into the record to see if the move exists. If it exists then the move is legal. If it does not exist, this move is illegal. Therefore, we cannot give an accurate complexity analysis in this aspect. The complexity will vary depending on the number of pieces remaining and the type of pieces remaining. What we can give is that get_all_moves() is O((9*10+8) + number of remaining pieces * complexity of the respective move function).

## Performance Measurement:
