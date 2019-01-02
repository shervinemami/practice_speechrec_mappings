#!/usr/bin/env python
# A very mininal game that helps practice names of keys for Dragonfly speech recognition grammars.
# By Shervin Emami 2019, "http://shervinemami.info/".
# Tested on Ubuntu 18.04 using python 2.7.


#--------------------------------------
# INSERT LETTER MAP HERE:
letterMap = {
    "(acid) ": "a",         # alpha is a bit like up. axis is like backspace. "(aim|and) ": "a",        # careful of 8, @, lace, lack. My "aim" sometimes gets picked up as "and".
    "(brain) ": "b",        #  "brown" is like down. "black" is like "ebike", "best" sometimes gets picked up as "this" or "guess". "B|the" sometimes gets picked up as "enter"
    "(char) ": "c",
    "(dozen) ": "d",        # "does" is like "geez", "drax" is like "right". "dam" is like down. "dim" is like "ding". "dug" is like dot. "des" is like "this". "desk" is like "verse", "dose", "this".
    "(ebike) ": "e",        # "ebike" is like "end black", "evo" isn't getting picked up! careful of x, see, end, as, up
    "(foxy) ": "f",        # My "fox" is like "false" # careful of F1, F2 ...
    "(golf) ": "g",             # My "gang" is like "can"
    "(hotel) ": "h",        # careful of 8 and quote
    "(itchy) ": "i",        # itchy is like teach
    "(julia) ": "j",
    "(krife) ": "k",        #kidding? krog? # krux is like plus. careful of equal, colon, capital queen, geez.  My "kaput" is like "up". My "kilo" sometimes gets picked up as "killer"
    "(lazy) ": "l",      # My "lima" is like "clean" and "end". My L sometimes gets picked up as "help". "L" is like Dragon keyword "spell" :-(
    "(miley) ": "m",       # Mosfet is somehow like "plus" and "space"! # Mix is a bit like minus?  # My "mike" is similar to "my"
    "(newish) ": "n",   # noosh is maybe like mosfet. niche is like unix. # nose?  "Nippy" is like "up"
    "(omez) ": "o",     # orange is like end. oryx is like "echo".  My "osh" is like "as". My "omar" is like "home up"
    "(pingu) ": "p",     # My "pom" is like "upon" and "up home"
    "(queen) ": "q",    # "queen" is like "clean"
    "(rude) ": "r",          # rolex is like krux. "rod" is like "right"
    "(salty) ": "s",     # "sook" is like "up", "size" is like "keys". careful of snake, space,
    "(trish) ": "t",        # tricky is like keys # teach is like itchy
    "(unix) ": "u",          # "urge"? # careful of yang
    "(video) ": "v",            # My "vix" is like "mix". My "vax" is like "backspace". My "van" is a bit like "then"
    "(wintel) ": "w",              # My "wes" is like "worse"
    "(x-ray) ": "x",
    "(yazzam) ": "y",     # yazzam is like home, yeast is like left. yellow is like "end left", yoke is like black. # "yang" is like "end". Careful of letter "u", home. "why" is like "white" that is like "why tay"
    "(zooki) ": "z",     # zood? zooki? zooch & zener are like insert! zulu isn't getting picked up! "zed" is like "said" and "set"
}

#--------------------------------------



import random
import time
import operator

#---------------------------------------
# Keyboard input code, taken from "https://github.com/akkana/scripts/blob/master/keyreader.py" on Jan 1st 2019.
import sys
import os
import termios, fcntl
import select

class KeyReader :
    '''
    Read keypresses one at a time, without waiting for a newline.
    echo: should characters be echoed?
    block: should we block for each character, or return immediately?
           (If !block, we'll return None if nothing is available to read.)
    '''
    def __init__(self, echo=False, block=True):
        '''Put the terminal into cbreak and noecho mode.'''
        self.fd = sys.stdin.fileno()

        self.block = block

        self.oldterm = termios.tcgetattr(self.fd)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)

        # Sad hack: when the destructor __del__ is called,
        # the fcntl module may already be unloaded, so we can no longer
        # call fcntl.fcntl() to set the terminal back to normal.
        # So just in case, store a reference to the fcntl module,
        # and also to termios (though I haven't yet seen a case
        # where termios was gone -- for some reason it's just fnctl).
        # The idea of keeping references to the modules comes from
        # http://bugs.python.org/issue5099
        # though I don't know if it'll solve the problem completely.
        self.fcntl = fcntl
        self.termios = termios

        newattr = termios.tcgetattr(self.fd)
        # tcgetattr returns: [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        # where cc is a list of the tty special characters (length-1 strings)
        # except for cc[termios.VMIN] and cc[termios.VTIME] which are ints.
        self.cc_save = newattr[6]
        newattr[3] = newattr[3] & ~termios.ICANON
        if not echo:
            newattr[3] = newattr[3] & ~termios.ECHO

        if block and False:
            # VMIN and VTIME are supposed to let us do blocking reads:
            # VMIN is the minimum number of characters before it will return,
            # VTIME is how long it will wait if for characters < VMIN.
            # This is documented in man termios.
            # However, it doesn't work in python!
            # In Python, read() never returns in non-canonical mode;
            # even typing a newline doesn't help.
            cc = self.cc_save[:]   # Make a copy so we can restore VMIN, VTIME
            cc[termios.VMIN] = 1
            cc[termios.VTIME] = 0
            newattr[6] = cc
        else:
            # Put stdin into non-blocking mode.
            # We need to do this even if we're blocking, see above.
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

        termios.tcsetattr(self.fd, termios.TCSANOW, newattr)

    def __del__(self):
        '''Reset the terminal before exiting the program.'''
        self.termios.tcsetattr(self.fd, self.termios.TCSAFLUSH, self.oldterm)
        self.fcntl.fcntl(self.fd, self.fcntl.F_SETFL, self.oldflags)

    def getch(self):
        '''Read keyboard input, returning a string.
           Note that one key may result in a string of more than one character,
           e.g. arrow keys that send escape sequences.
           There may also be multiple keystrokes queued up since the last read.
           This function, sadly, cannot read special characters like VolumeUp.
           They don't show up in ordinary CLI reads -- you have to be in
           a window system like X to get those special keycodes.
        '''
        # Since we can't use the normal cbreak read from python,
        # use select to see if there's anything there:
        if self.block:
            inp, outp, err = select.select([sys.stdin], [], [])
        try:
            return sys.stdin.read()
        except (IOError, TypeError) as e:
            return None
#--------------------------------------




# Allow custom combo length
combo = 3
capitalPercentage = 0
showAlphabetically = False
startOfArgs = 1
if len(sys.argv) > 1 and sys.argv[1] == "-a":
    showAlphabetically = True
    startOfArgs = startOfArgs+1
if len(sys.argv) > startOfArgs:
    combo = int(sys.argv[startOfArgs])
if len(sys.argv) > startOfArgs+1:
    capitalPercentage = int(sys.argv[startOfArgs+1])

print "Press the", combo, "shown keys as fast as you can, using either a speech recognition engine or a physical keyboard!"

# Sort the dictionary alphabetically, to allow showing characters in alphabetical order if desired.
#letterMap = sorted(letterMap.iterkeys())
letterMap = sorted(letterMap.items(), key=operator.itemgetter(1))

keyreader = KeyReader(echo=True, block=True)
tallyCorrect = 0
tallyWrong = 0
averagedSpeed = -1    # Initialize with the first measurement
nextAlphabet = 0

while (True):
    truth = ""
    for i in xrange(combo):
        if showAlphabetically:
            r = nextAlphabet         # Pick the next letter
            nextAlphabet = nextAlphabet + 1
            if nextAlphabet >= len(letterMap):
                nextAlphabet = 0
        else:
            r = random.randint(0, len(letterMap) - 1)    # Pick a random letter
        (word, char) = letterMap[r]
        if random.randint(0, 100) < capitalPercentage:    # Occasionally use a capital letter
            char = char.upper()
            word = word.upper()
        print (word, char)
        truth += char

    timeStart = time.time()

    typed = ""
    for i in xrange(combo):
        key = keyreader.getch()
        typed += key

    timeEnd = time.time()
    rawSpeed = (timeEnd - timeStart) / combo
    # Perform a running average alpha filter to smoothen the result but give more priority to recent results
    if averagedSpeed < 0:
        averagedSpeed = rawSpeed
    alpha = 0.3    # The closer this is to 1.0, the stronger the filtering that will be applied.
    averagedSpeed = ((1.0 - alpha) * rawSpeed) + (alpha * averagedSpeed)

    print
    if typed == truth:
        tallyCorrect = tallyCorrect+1
        print "Correct.                                  Tally:", tallyCorrect, "correct,", tallyWrong, "wrong. Speed: %.2f s/key" % averagedSpeed
    else:
        tallyWrong = tallyWrong+1
        print "### WRONG! ###### ", truth, typed, "############ Tally:", tallyCorrect, "correct,", tallyWrong, "wrong. ###################################"
    print
