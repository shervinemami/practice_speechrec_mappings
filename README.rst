=================
Practice Speechrec Mappings
=================
A very mininal game that helps practice key mappings for Talon or Dragonfly speech recognition grammars.
Can be very useful for quickly finding clashes between combinations of letters and symbols and numbers.
Has only been tested on Linux. It might work on Windows or OS X but it hasn't been tested.
By Shervin Emami 2019-2023, shervin.emami@gmail.com.

Background:
----------------
When using speech recognition for voice coding / programming / computer control, it's quite important to have high accuracy of each
letter of the alphabet, and the various symbols that will be used. Rather than speak each character or variable name directly, it's 
far more accurate to use a mapping of words to characters, such as by saying the word "alpha" instead of just the letter "a". I created 
this game / tool to help me find a good mapping of alphabet words, and to train myself to use the mapping. I have tested Dragonfly mode with
both Dragonfly on Kaldi-Active-Grammar, and Dragonfly / aenea on Nuance Dragon, but only with my custom phonetic mapping (files are included), 
based on DWK's simple grammar at "https://github.com/dwks/aenea-grammar-simple/blob/master/keyboard.py"

This program prints random characters with their word mapping, and checks the accuracy & speed of what I type. To start with, I run
"practice_mappings 3" and then "practice_mappings 5" for a while, and I simply say the words shown on the left, until I'm quite happy with the
accuracy. ie: without trying to memorize the mappings I just read out the mappings, and I try to talk fairly fast but not ultra fast, until
I'm rarely making a mistake. Whenever I make a mistake, I look at it to see if I need to change my mapping (both in Dragonfly and in this
game).
Eventually when I'm quite happy with the accuracy, meaning that my character mapping is ambiguous enough that I can use it quite
reliably, then I run the game again but I concentrate on the individual character shown on the right, by trying to memorize the word mapping.
After some time I start getting better at memorizing the mapping, so I add some capital letters by running "practice_mappings 5 30",
and I keep practising to get faster & faster. I occasionally also play the game sometimes using an actual keyboard, to compare my
speed when using speech vs keyboard.

Note that there's also a separate "measure_typing_rate.py" program that is intended for rare use-cases such as measuring the keypress latency.


Usage:
----------------

.. code::

    python practice_mappings.py [-dragonfly] [-alphabetical] [-symbols] [<combo-length> [<capitals-percentage> [<random-seed>]]]

    where:
        -dragonfly            Use Dragonfly mode ('lettermap.py' + 'punctuationmap.py'). Default is Talon mode.
        -alphabetical         Sort the characters alphabetically. Default is random (ie: unsorted).
        -symbols              Include some symbols in the mix. Default is just alphabet letters, not symbols.
        <combo-length>        How many characters you will try to say at the same time. Default is 3.
        <capitals-percentage> Percentage of characters that will be a capital letter. Default is 0.
        <random-seed>         Allows following a determinstic sequence of random values. Default is None (ie: system timer).

eg:

.. code:: shell

    python practice_mappings.py
    python practice_mappings.py -symbols 5 20
    python practice_mappings.py -dragonfly -symbols 5 20 12345


Sample output:
----------------

Talon mode:

.. code:: shell

    $ python ./practice_mappings.py -symbols 3 10
    usage: python practice_mappings.py [-dragonfly] [-alphabetical] [-symbols] [<combo-length> [<capitals-percentage>]]
    By default, it will run as Talon knausj mode. Or to use Dragonfly mode, add '-dragonfly'.
    See 'https://github.com/shervinemami/practice_speechrec_mappings' for more details

    Press the 3 shown keys as fast as you can, using either a speech recognition engine or a physical keyboard!
    zlk                                        zap  look crunch  
    zlk
    Correct.                                  Tally: 1 correct = 0.0% WER. Speed: 0.58 s/key

    1b                                         one  bat space  
    1b 
    Correct.                                  Tally: 2 correct = 0.0% WER. Speed: 0.68 s/key

    y(4                                        yank  L paren  four  
    y[4
    ### WRONG! ######  y(4 y[4 ############ Tally: 2 correct, 1 wrong. ###################################

    vis                                        vest  sit  salty    
    ...

Dragonfly mode:

.. code:: shell

    $ python ./practice_mappings.py -dragonfly -symbols 3 10
    zlk                                        zimeesi  lazy  krife  
    zlk
    Correct.                                  Tally: 1 correct = 0.0% WER. Speed: 0.58 s/key

    1b                                         one  bony  space  
    1b 
    Correct.                                  Tally: 2 correct = 0.0% WER. Speed: 0.68 s/key

    ...
    
    
To use your own Talon grammar, make sure you installed knausj into "~/.talon/user/knausj_talon".
In Talon mode it will use these 2 files on your computer:

.. code:: shell

    ~/.talon/user/knausj_talon/settings/alphabet.csv
    ~/.talon/user/knausj_talon/core/keys/keys.py

If you've installed them in different locations on your computer, you'll need to modify these 2 file locations in 'practice_mappings.py'.

Or for Dragonfly mode, to use your own Dragonfly grammar and not myne, you'll need to put your alphabet character mapping into file "letterMap.py", such as:

.. code:: shell

    letterMap = { 
        "acid": "a",
        "bony": "b",
        "char": "c",
        ...
    }


