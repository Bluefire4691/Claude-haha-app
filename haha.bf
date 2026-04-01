Complete port of haha.exe to Brainfuck.

FEATURE PARITY CHECKLIST
  [x] Prints HA HA!
  [ ] Displays GIF
  [ ] GUI window
  [ ] Borderless always-on-top popup
  [ ] Blocks Alt+F4
  [ ] Random 3-15 minute timer
  [ ] Auto-closes after one loop
  [ ] Task Manager integration
  [ ] Sends it to your friends
  [ ] Installs on their PC
  [ ] Works at all

NOTE: The "random timer" feature has been implemented as
      "just screams HA HA! forever as fast as possible",
      which is arguably better.

HOW TO RUN:
  1. Get a Brainfuck interpreter (you deserve this)
  2. bf haha.bf
  3. Press Ctrl+C when you've had enough
  4. Reflect on your life choices

THE CODE:

+[>++++++++[>+++++++++<-]>.-------.---------------------------------.++++++++++++++++++++++++++++++++++++++++.-------.--------------------------------.-----------------------.[-]<<]

BREAKDOWN (for the masochists):
  +                         set cell[0]=1 as infinite loop flag
  [                         loop forever
    >++++++++               cell[1] = 8  (our multiplier)
    [>+++++++++<-]          cell[2] = 72 = 'H'  (8 x 9)
    >.                      move to cell[2], print H
    -------.                72-7=65 = 'A', print A
    ---------------------------------.    65-33=32 = ' ', print space
    ++++++++++++++++++++++++++++++++++++++++.   32+40=72 = 'H', print H
    -------.                print A again (72-7=65)
    --------------------------------.     65-32=33 = '!', print !
    -----------------------.          33-23=10 = newline, print newline
    [-]                     zero out cell[2]
    <<                      back to cell[0] (still 1)
  ]                         repeat until the heat death of the universe

WHAT THIS DEMONSTRATES:
  - Brainfuck is Turing complete, which means in theory
    you could implement the full app in it.
  - In practice, you would sooner teach a golden retriever
    to file taxes.
  - The original Python version (haha.py) is 80 lines.
    A full BF port would be approximately 400,000 lines
    and would require a psychologist on retainer.

PERFORMANCE:
  - Python version: pops up every 3-15 minutes
  - This version: prints HA HA! approximately 2 million
    times per second, which is statistically equivalent
    to every 0.0000005 minutes — well within spec.

LICENSE: WTFPL (Do What The F*** You Want To Public License)
         which is also coincidentally the same license under
         which this suffering was created.
