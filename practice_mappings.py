#!/usr/bin/env python
# A very mininal game that helps practice names of keys for Dragonfly or knausj Talon speech recognition grammars.
# By Shervin Emami 2023, "http://shervinemami.com/".
# Tested on Ubuntu 23.04 using python 3.10.

# Python 2/3 compatibility
from __future__ import print_function

import os
import sys
import random
import time
import operator
import argparse

from failed import FailedCodes

# Instantiate the argument parser
parser = argparse.ArgumentParser(usage='%(prog)s [options] [combo_length]')

# Process the command-line args before doing anything else, so we can load files based on the args.
combo = 3
parser.add_argument('combo_length', type=int, nargs='?', help='How many characters you will try to say at the same time. Default is 3.')
parser.add_argument('-d', '--dragonfly', action='store_true', help='Use Dragonfly mode ("lettermap.py" + "punctuationmap.py"). Default is Talon mode.')
parser.add_argument('-a', '--alphabetical', action='store_true', help='Sort the characters alphabetically. Default is random (ie: unsorted).')
parser.add_argument('-s', '--symbols', action='store_true', help='Include some symbols in the mix. Default is just alphabet letters, not symbols.')
parser.add_argument('-n', '--no_numbers', action='store_true', help='Skip numerals, only use letters (and possibly symbols). Default is to include numbers.')
parser.add_argument('-c', '--no_crucial', action='store_true', help='Skip crucial symbols (commas and spaces). Default is to include crucial symbols.')
parser.add_argument('-p', '--capitals_percentage', type=int, default=0, help='Percentage of characters that will be a capital letter. Default is 0.')
parser.add_argument('-r', '--random_seed', type=int, help='Allows following a determinstic sequence of random values. Default is the system timer.')
parser.add_argument('-A', '--adaptive', action='store_true', default=False, help='Adaptive mode. Store errors and adaptively offer the most common errors first. Default is no adaptive mode.')
args = parser.parse_args()

print("Practice keyboard mappings, such as to practice voice coding. By Shervin Emami (http://shervinemami.com), 2023.")
print("By default, it will run as Talon knausj mode. Or to use Dragonfly mode, add '--dragonfly'.")
print("See 'https://github.com/shervinemami/practice_speechrec_mappings' for more details")
print("")

if args.combo_length:
    combo = args.combo_length

if args.random_seed:
    print("Using", args.random_seed, "as the random seed instead of the current time")
    random.seed(args.random_seed)

if args.adaptive:
    print("Adaptive mode is enabled. Failed combos will be stored and offered later, randomly.")

if args.dragonfly:
    # Import the "letterMap" dictionary from the "lettermap.py" file that's in the MacroSystem folder.
    # Make sure you adjust this path to where it's located on your machine, relative to this script.
    sys.path.append('../MacroSystem')
    from lettermap import letterMap

    # Also potentially include symbols, not just alphabet letters
    try:
        # Long version of punctuation characters, that are slower but more reliable, hence good for general use at any time:
        from punctuationmap import longPunctuationMap
    except:
        pass
else:
    # Talon filenames. You can use "~" to refer to the Talon user folder.
    CSV_filename = "~/.talon/user/knausj_talon/settings/alphabet.csv"
    keys_filename = "~/.talon/user/knausj_talon/core/keys/keys.py"

    import csv


crucialMap = {
    "space":    " ",
    "dot":      ".",
}
numberMap = {
    "zero":     "0",
    "one":      "1",
    "two":      "2",
    "three":    "3",
    "four":     "4",
    "five":     "5",
    "six":      "6",
    "seven":    "7",
    "eight":    "8",
    "nine":     "9",
}

#---------------------------------------
# Keyboard input code, taken from "https://github.com/akkana/scripts/blob/master/keyreader.py" on Jan 1st 2019.
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


# Try to load a given Talon alphabet CSV file, potentially ignoring the header (first row)
def load_talon_lettermap(CSV_filename):
    CSV_filename = os.path.expanduser(CSV_filename)   # Allow to hard-code "~" in this source file as the user's home folder

    new_lettermap = {}  # Create an empty Dictionary
    with open(CSV_filename, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            if ("Spoken Form" not in row) and (len(row) >= 2):
                #print(row[0], "=== ", row[1])
                # Note that in Shervin's Dragonfly lettermap file, the phrase is the 1st word and the character is the 2nd word,
                # but in Talon's alphabet csv file, the character is the 1st word and the phrase is the 2nd word.
                # So we swap them here.
                new_lettermap[row[1]] = row[0]
    return new_lettermap

# Pull the dictionary mappings from the following lines in the file until a "}" line is found.
# Stores the mappings directly into the dict in-place.
# Assumes pyfile has already been opened and the file pointer is now at a new line containing the dictionary mappings (ie: after a "{").
def extract_dictionary_from_part_of_python_file(pyfile, d={}):
    # Scan the line to find the phrase, and the symbol it maps to.
    # The line is typically something like the string: '  "question mark": "?",   # A random comment.\n'
    for line in pyfile:
        # Remove whitespace at the start of the string, then see if it starts with a '"' or "'" single-quote or double-quote character.
        line = line.lstrip()
        #print("line: ", line)
        if len(line) >= 6 and (line[0] == '"' or line[0] == "'"):
            # Make sure this phrase starts with an actual alphabetical letter, not a symbol such as ','.
            if line[1].isalpha():
                # Remove the potential whitespace & potential random stuff & line-ending at the end of the string after the comma.
                # This should generate something like: '"question mark": "?"'
                words = line.split(',')[0]
                if len(words) >= 1:
                    # Split up the string by ':'
                    words = words.split(':')     # eg: ['"question mark"', '"?"']
                    if len(words) >= 2 and len(words[0]) >= 1 and len(words[1]) >= 1:
                        phrase = words[0].lstrip('"').rstrip('"')          # eg: 'question mark'
                        symbol = words[1].lstrip(' "').rstrip('"')         # eg: '?'
                        if len(phrase) >= 1 and len(symbol) >= 1:
                            # If the symbol starts with a '\' character, remove it, but leave whatever is after it.
                            if symbol[0] == '\\':
                                symbol = symbol[1]
                            # If the symbol starts & ends with a "'" character, remove it, but leave whatever is after it.
                            if symbol[0] == "'" and len(symbol) > 1 and symbol[-1] == "'":
                                symbol = symbol[1]
                            #print("phrase=<" + phrase + ">, \t symbol=<" + symbol + ">.")
                            # Add the mapping to our dictionary.
                            d[phrase] = symbol
        elif line.lstrip()[0] == "}":  # Check for a close brace, but skip close braces that are inside strings, since the user probably has a close brace in their alphabet!
            break

# Try to load the symbolmap from a given Talon keys.py file
def load_talon_symbolmap(filename):
    filename = os.path.expanduser(filename)     # Allow to hard-code "~" in this source file as the user's home folder

    new_symbolmap = {}  # Create an empty Dictionary
    with open(filename, 'r') as pyfile:
        current_line = ""
        # Skip all lines in the Python file until we find the "punctuation_words" declaration line.
        for line in pyfile:
            if "punctuation_words = {" in line:
                break
        extract_dictionary_from_part_of_python_file(pyfile, new_symbolmap)
        # Skip all lines in the Python file until we find the "symbol_key_words" declaration line.
        for line in pyfile:
            if "symbol_key_words = {" in line:
                break
        extract_dictionary_from_part_of_python_file(pyfile, new_symbolmap)
    #print(new_symbolmap)
    return new_symbolmap
#--------------------------------------


if not args.dragonfly:
    # First try loading the alphabet CSV into a dictionary.
    new_lettermap = load_talon_lettermap(CSV_filename)
    if len(new_lettermap) > 0:
        letterMap = new_lettermap

    # Now try converting the "punctuation_words" and "" definitions in the user's "keys.py" file into a dictionary.
    # Note that we aren't importing the python file directly, because that would require importing talon, which requires integration. 
    new_symbolmap = load_talon_symbolmap(keys_filename)
    if len(new_symbolmap) > 0:
        longPunctuationMap = new_symbolmap

# Sort the dictionary alphabetically, to allow showing characters in alphabetical order if desired.
#letterMap = sorted(letterMap.iterkeys())
letterMap = sorted(letterMap.items(), key=operator.itemgetter(1))
if not args.no_numbers:
    numbersAsList = sorted(numberMap.items(), key=operator.itemgetter(1))
    letterMap.extend(numbersAsList)
# Include the crucial list twice, so they will get chosen more often than other symbols.
if not args.no_crucial:
    crucialAsList = sorted(crucialMap.items(), key=operator.itemgetter(1))
    letterMap.extend(crucialAsList)
    letterMap.extend(crucialAsList)

# Possibly include symbols in addition to letters.
if args.symbols:
    # Add double entries for the main characters, so they will get chosen more often than the other symbols.
    letterMap.extend(letterMap)
    # Other symbols
    try:
        symbolsAsList = sorted(longPunctuationMap.items(), key=operator.itemgetter(1))
        letterMap.extend(symbolsAsList)
        #print("SYMBOLS", symbolsAsList)
        #print("LETTERMAP", letterMap)
    except:
        print("Warning: Couldn't find extra symbol files")


print("Press the "+ str(combo) + " shown keys as fast as you can, using either a speech recognition engine or a physical keyboard!")

keyreader = KeyReader(echo=True, block=True)
tallyCorrect = 0
tallyWrong = 0
averagedSpeed = -1    # Initialize with the first measurement
nextAlphabet = 0

# prepare reverse letterMap
reverseLetterMap = {v: k for k, v in letterMap}
# prepare failed combos object
# TODO: probabilities and repetitions should be configurable from command line
failed_combos = FailedCodes(repetitions=3)
while (True):
    truth = ""
    chars = []
    words = []
    # Get failed combo from storage first, if exists, if not, FailedCodes.random returns None
    # 0.5 is the probability of getting the failed combo
    # 0.1 is the probability of getting the least failed combo (but still failed)
    truth_candidate = failed_combos.random(0.5, 0.1)
    # in adaptive mode, devote 20% of attempts to fix failed combos
    if args.adaptive and truth_candidate is not None and random.random() < 0.5:
        nf = failed_combos.get_num_of_repetitions(truth_candidate)
        print(f"Retrying preivously failed combo '{truth_candidate}' ({nf} repetitions to go)")
        truth = truth_candidate
        chars = truth
        words = [reverseLetterMap[c] for c in truth]
    else:
        for i in range(combo):
            if args.alphabetical:
                r = nextAlphabet         # Pick the next letter
                nextAlphabet = nextAlphabet + 1
                if nextAlphabet >= len(letterMap):
                    nextAlphabet = 0
            else:
                r = random.randint(0, len(letterMap) - 1)    # Pick a random letter
            (word, char) = letterMap[r]
            if random.randint(0, 100) < args.capitals_percentage:    # Occasionally use a capital letter
                char = char.upper()
                word = word.upper()
            #print("%25s %25s" % (word, char))
            chars.append(char)
            words.append(word)
            truth += char

    # Print all the characters on a single line
    for i in range(combo):
        print(chars[i], end='')
    print("                                        ", end='')
    for i in range(combo):
        print(words[i], " ", end='')
    print()    


    timeStart = time.time()

    typed = ""
    for i in range(combo):
        key = keyreader.getch()
        typed += key

    timeEnd = time.time()
    rawSpeed = (timeEnd - timeStart) / combo
    # Perform a running average alpha filter to smoothen the result but give more priority to recent results
    if averagedSpeed < 0:
        averagedSpeed = rawSpeed
    alpha = 0.5    # The closer this is to 1.0, the stronger the filtering that will be applied.
    averagedSpeed = ((1.0 - alpha) * rawSpeed) + (alpha * averagedSpeed)

    print()
    if typed == truth:
        tallyCorrect = tallyCorrect+1
        wordErrorRate = 100.0 * (tallyWrong / float(tallyCorrect + tallyWrong))
        print("Correct.                                  Tally: %d correct = %.1f%% WER. Speed: %.2f s/key" % (tallyCorrect, wordErrorRate, averagedSpeed))
        failed_combos.unfail(truth)
    else:
        tallyWrong = tallyWrong+1
        print("### WRONG! ###### ", truth, typed, "############ Tally:", tallyCorrect, "correct,", tallyWrong, "wrong. ###################################")
        failed_combos.fail(truth)
    print()

