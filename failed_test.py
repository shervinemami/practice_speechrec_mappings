"""
This is a test file for the FailedCodes class.
"""

from collections import Counter
import pytest # pylint: disable=unused-import

from failed import FailedCodes

def test_failed_codes():
    """
    Test the FailedCodes class.
    """
    failed_codes = FailedCodes()
    failed_codes.fail('a')
    failed_codes.fail('a')
    failed_codes.fail('b')
    failed_codes.fail('c')
    failed_codes.fail('d')
    failed_codes.fail('d')
    failed_codes.fail('d')

    result_counts = Counter([failed_codes.random(0.5, 0.01) for _ in range(1000)])

    # Check that the returned results are not None
    assert None not in result_counts.keys()

    # Check that the most frequent code is returned more often
    assert result_counts['d'] > result_counts['a']
    assert result_counts['d'] > result_counts['b']
    assert result_counts['d'] > result_counts['c']
