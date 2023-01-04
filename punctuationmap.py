# coding: utf-8
# Dictionary of my non-alphabet keyboard mappings, ie: for punctuation and similar letters that exist on the keyboard but aren't in the English alphabet.
# Saying the phrase on the left should generate the symbol on the right.
# Symbols that are easier to say should be placed in the top of the list, since some screens won't need to show the symbols on the bottom of the list.
# Order is preserved, since we use the order as the way to find the index that directly controls the mouse position.

from collections import OrderedDict     # Allows ordered dictionaries even in Python 2
punctuationMap1 = OrderedDict()
punctuationMap2 = OrderedDict()

# Short version of keyboard characters (that aren't numbers or letters), that have a small name and therefore are fast to say but less reliable:
punctuationMap1["tilda"] = u"~"
punctuationMap1["quotes"] = u'"'
punctuationMap1["at"] = u"@"
punctuationMap1["hash"] = u"#"
punctuationMap1["dollar"] = u"$"
punctuationMap1["percent"] = u"%"
punctuationMap1["caret"] = u"^"
punctuationMap1["plus"] = u"+"
punctuationMap1["minus"] = u"-"
punctuationMap1["equals"] = u"="
punctuationMap1["colon"] = u":"
punctuationMap1["slash"] = u"/"
punctuationMap1["pipe"] = u"|"
punctuationMap1["comma"] = u","
punctuationMap1["dot"] = u"."
punctuationMap1["question"] = u"?"

# These are part of normal keyboard characters, but since they are harder to say than most symbols, they are being added late so that they're less likely to be used (eg: Y axis on small screens probably won't use symbols this far down)
punctuationMap2["underscore"] = u"_"
punctuationMap2["semicolon"] = u";"
punctuationMap2["backtick"] = u"`"
punctuationMap2["exclamation"] = u"!"
punctuationMap2["ampersand"] = u"&"
punctuationMap2["asterisk"] = u"*"
punctuationMap2["backslash"] = u"\\"
punctuationMap2["round bracket"] = u"("
punctuationMap2["close round"] = u")"
punctuationMap2["square bracket"] = u"["
punctuationMap2["close square"] = u"]"
punctuationMap2["curly brace"] = u"{"
punctuationMap2["close curly"] = u"}"
punctuationMap2["less than"] = u"<"
punctuationMap2["greater than"] = u">"


# Long version of punctuation characters, that are slower but more reliable, hence good for general use at any time:
longPunctuationMap = {
    "pipe symbol": "|",     # "pipe" on its own is too short for Kaldi
    "minus": "-",
    "dot": ".",            # "dot" often ends up causing the phrase "enter" to be taken as "end dot" (or "end up"). "dot" is slightly bad in Kaldi, but "fullstop" is bad in Dragon.
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(asterisk|Asterix)": "*",
    "colon": ":",
    "(semicolon|semi colon)": ";",
    "at symbol": "@",       # "at" on its own is too short for Kaldi
    #"[double] quote": '"',
    "quotes": '"',
    "single quote": "'",
    "apostrophe": "'",
    "hash": "#",
    "dollar": "$",
    "dollar sign": "$",
    "percent": "%",
    "percentage": "%",
    "ampersand": "&",
    "slash": "/",
    "equals": "=",
    "plus": "+",
    "space": " ",
    "question": "?",
    "question mark": "?",
    "exclamation": "!",
    "exclamation mark": "!",
    #"bang": "!",               # "bang" sounds like "aim" that I might use for "a"
    "caret": "^",
    "tilde": "~",
    "back tick": "`",
}
