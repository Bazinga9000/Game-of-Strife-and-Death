# Game-of-Strife-and-Death
evolving game of life and death



# How to Use:
1) `pip install pygame`

2) Run the file

# Controls (Shown in-game):

Left and Right - View other Generations

A - ASAP Generation

F - Fast Generation

S - Slow Generation

B - Battle the 2 creatures on the grid

I - Do one Iteration

Left/Right Control - Input Custom Creature Names

Left Alt: Input Custom Rulestring

Escape - Clear Grid/Exit Custom Input

1-9 - Save in Slot

F1-F9 - Load from Slot

G - Sort by Generation Created

R - Sort by Rank

P - Sort by Population

O - Sort by overall Score

U - Sort by overall Population

W - Warp to Generation

# Custom Rulestrings:

Custom Rulestring Format:

Birth Range/Survival Range/Neutral Behavior/Neighborhood

(If you want multiple values for the first two, simply put them next to each other, as in "23" would be 2 and 3)

Birth Range - Number of neighbors required for a dead cell to come to life

Survival Range - Number of neighbors required for a live cell to stay living

Neutral Behavior - Governs how cells born to equal numbers of red and blue parents behave

If 0, when a cell is born with equal numbers of both red and blue, it is neutral and counts towards the population of neither creature
If 1, the cell turns purple and is counted towards both of the populations

Neighborhood - Governs what cells are considered "neighbors" during iteration

If 0, it is the normal "King's Move"/"Moore" neighborhood
If 1, it is the orthogonal only "Von Neumann" neighborhood
If 2, it is the "Von Neumann" neighborhood, except it goes out two cells instead of one
If 3, it is the Knight's Move


Changing the rulestring causes the game to autosave your evolution to prevent accidental mishaps
