#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:47:02 2019

This class stores failed codes and returns a random code based on the
number of times it has failed. The more times a code has failed, the
more likely it is to be returned.
"""

import random
from collections import defaultdict

DEBUG=False

def debug(*args):
    """ Prints debug messages if DEBUG is True """
    if DEBUG:
        print(*args)

class FailedCodes:
    """
    This class stores failed codes and returns a random code based on the
    number of times it has failed.
    """
    def __init__(self, repetitions=3):
        self.repetitions = repetitions
        self.fail_counter = defaultdict(int)
        debug('Initialized fail_counter')

    def fail(self, code):
        """
        Increments the number of repetitons a code thats failed.
        """
        debug('Incrementing fail_counter')
        self.fail_counter[code] += self.repetitions

    def unfail(self, code):
        """
        Decrements the number of times a code has failed.
        Parameter code speicfies probablity of unfailing a code.
        """
        if code not in self.fail_counter:
            debug('Code not in fail_counter')
            return
        if self.fail_counter[code] > 1:
            debug('Decrementing fail_counter')
            self.fail_counter[code] -= 1
        else:
            debug('Deleting code from fail_counter')
            del self.fail_counter[code]

    def get_num_of_repetitions(self, code):
        """
        Check for fail_counter[code] existance and return the
        number of repetitions.
        """
        debug('Checking fail_counter')
        return self.fail_counter.get(code, 0)

    def random(self, pb1, pb2):
        """
        Returns a random code based on the number of times it has failed.
        """
        if not self.fail_counter:
            debug('No codes in fail_counter')
            return None
        sorted_codes = sorted(self.fail_counter.items(), key=lambda x: x[1], reverse=True)
        total_fails = sum(x[1] for x in sorted_codes)
        prob_range = pb2 - pb1
        pb_interval = prob_range / (total_fails - 1) if total_fails > 1 else 0

        prob = pb1
        threshold = prob
        # since there is at least one code in the fail_counter
        # just try forever until we get a code
        while True:
            debug("Trying to get a random combo from failed codes")
            for code, _ in sorted_codes:
                if random.random() < threshold:
                    return code
                prob += pb_interval
                threshold -= pb_interval
