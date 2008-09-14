Monkey in a Tangle
===================================

Entry in PyWeek #7  <http://www.pyweek.org/7/>
Team: Ohio State U. Game Creation Club
Members: morgan.goose, Alfred Rossi (AlfredR), Jane, jsharpna

DEPENDENCIES:

You might need to install some of these before running the game:

  Python:     http://python.org/
  PyGame:     http://pygame.org/
  PyMunk:     http://code.google.com/p/pymunk/

RUNNING THE GAME:

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py

HOW TO PLAY THE GAME:

  --KEYS--
  left      Move left
  right     Move right
  z         Picks up
  x         Drops an item
  c         Attaches held item to chain
  v         Detaches item from chain
  Space/Up  Jump
  r         Restarts level


  The game mechanics work like this: You're a monkey with a tether. 
  You'd like to box yourself some bananas but your hands are circular 
  so what do you do? You tether them! (Why not?).

  In the upper right hand corner you'll see the number of bananas 
  you need to box and how many you've boxed so far. Once your box is 
  full you will move to the next level. If you don't complete the 
  level before time runs out you must restart the level.

  z picks up your tether

  x drops it
  
  c attaches the held end of your tether to certain movable items in 
  the game (and non-movable hooks on the ground). You have to be holding 
  the tether and pressing against the item you'd like to 
  rope.
  
  v detaches the rope from an item, you need to be pressing against 
  the connected item. You can jump with space (or up) and you move 
  the arrow keys.

NOTES:
  A fast computer is probably necessary to play the game. It will 
  likely be unplayable on anything slower than a 1.8 GHz x86

  We'd also like to give a special thanks to pymike for the use of 
  his ezmenu library.

LICENSE:
  Licensed under the BSD3 license. See LICENSE.txt for more information.

