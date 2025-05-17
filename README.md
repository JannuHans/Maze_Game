Maze Escape - Smart Rat vs Intelligent Man (Pygame Project)
============================================================

Overview:
---------
Maze Escape is a Python-based grid game built using the Pygame library. You control a rat trying to reach a green hole while avoiding traps and being chased by a man who uses an AI-based A* pathfinding algorithm. The game gets harder or easier depending on your performance.

Objective:
----------
- Control the RAT using your keyboard (WASD).
- Reach the HOLE to win.
- Avoid the TRAPS and the MAN.
- If you reach the hole, difficulty increases.
- If you’re caught or trapped, difficulty decreases.

Game Elements:
--------------
- RAT: You (the player)
- MAN: Enemy that intelligently follows you
- HOLE: Target location to win
- WALL: Maze boundaries
- TRAPS: Stepping on one ends the game

Controls:
---------
W – Move Up  
A – Move Left  
S – Move Down  
D – Move Right  
R – Restart game after win/loss

How it Works:
-------------
- The maze is randomly generated with walls and traps.
- The RAT, MAN, HOLE, and TRAPS are placed randomly in open spaces.
- The MAN uses the A* pathfinding algorithm to move toward the RAT.
- Each time you win or lose, the game resets and the difficulty adjusts.

Technologies Used:
------------------
- Python 3
- Pygame
- heapq (for A* algorithm)
- random (for generating maze)

How to Run:
-----------
1. Install Python 3
2. Install pygame:
   pip install pygame
3. Save the script as maze_escape.py and run:
   python maze_escape.py

File Structure:
---------------
maze_escape.py      --> Main game script  
README.txt / README.md  --> Game instructions and documentation  
requirements.txt    --> List of required Python modules (just pygame)

Future Ideas:
-------------
- Add sound effects and music
- Add scoring and high score tracking
- Use images for characters
- Create multiple levels
- Make it playable in a browser

