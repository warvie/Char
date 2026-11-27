Dead Ground — desktop version
=============================

What this is
------------
The same game, run as its own desktop window with the browser's frame-rate
cap switched off. In a normal browser tab, drawing is locked to your
screen's refresh rate (usually 60) and slowed to ~30 when the tab is in the
background; this launcher starts Chrome (or Edge) with those limits off.

How to play
-----------
1. Keep these files together in one folder:
     index.html
     Play Dead Ground.bat            (Windows)
     Play Dead Ground (Mac).command  (Mac)
2. Windows: double-click "Play Dead Ground.bat".
   Mac: double-click "Play Dead Ground (Mac).command".
   (If Mac blocks it: right-click > Open, once.)
3. The game opens in its own window. Turn on developer mode to see the FPS
   counter; it can now go past your screen's refresh rate.

Good to know
------------
- Needs Chrome or Edge installed, and internet on first run (the 3D library
  loads from the web once, then it's cached).
- Saves live in this desktop version's own profile, separate from your
  browser's saves.
- With the cap off, your graphics card runs as fast as it can: more heat and
  battery use, and frames beyond your screen's refresh rate aren't actually
  shown - the game just never has to wait on the screen.
- To update the game, replace index.html with a newer copy.
