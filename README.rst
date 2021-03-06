=================
Practice Speechrec Mappings
=================
A very mininal game that helps practice names of keys for Dragonfly speech recognition grammars.
By Shervin Emami 2019, shervin.emami@gmail.com.

Background:
----------------
When using speech recognition for voice coding / programming / computer control, it's quite important to have high accuracy of each
letter of the alphabet, and the various symbols that will be used. Rather than speak each character or variable name directly, it's 
far more accurate to use a mapping of words to characters, such as by saying the word "alpha" instead of just the letter "a". I created 
this game / tool to help me find a good mapping of alphabet words, and to train myself to use the mapping. I have only tested it with 
Dragonfly / aenea, based on DWK's simple grammar at "https://github.com/dwks/aenea-grammar-simple/blob/master/keyboard.py"

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


Usage:
----------------

.. code:: shell

    python practice_mappings.py [-a] [-s] [<combo> [<capitals>]]

    where:
        -a         Sort the characters alphabetically instead of randomly
        -s         Include some symbols in the mix, not just alphabet letters
        <combo>    How many characters you will try to say at the same time. Default is 3.
        <capitals> Percentage of characters that will be a capital letter. Default is 0.

eg:

.. code:: shell

    python practice_mappings.py
    python practice_mappings.py -s 4 10


Sample output:
----------------

.. code:: shell

    $ python ./practice_mappings.py -s 3 10
    usage: python practice_mappings.py [-a] [-s] [<combo> [<capitals>]]
    See 'https://github.com/shervinemami/practice_speechrec_mappings' for more details

    Press the 3 shown keys as fast as you can, using either a speech recognition engine or a physical keyboard!
    zlk                                        zimeesi  lazy  krife  
    zlk
    Correct.                                  Tally: 1 correct = 0.0% WER. Speed: 0.58 s/key

    1b                                         one  bony  space  
    1b 
    Correct.                                  Tally: 2 correct = 0.0% WER. Speed: 0.68 s/key

    yl4                                        yeelax  lazy  four  
    yl5
    ### WRONG! ######  yl4 yl5 ############ Tally: 2 correct, 1 wrong. ###################################

    vis                                        video  itchy  salty    
    ...
    
    
To use your own grammar and not myne, you'll need to put your alphabet character mapping into file "letterMap.py", such as:

.. code:: shell

    letterMap = { 
        "acid": "a",
        "bony": "b",
        "char": "c",
        ...
    }


