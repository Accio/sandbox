## example from https://hypothesis.readthedocs.io/en/latest/quickstart.html

from hypothesis import given
from hypothesis.strategies import text

def encode(input_string):
    count = 1
    prev = ""
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    entry = (character, count)
    lst.append(entry)
    return lst


def decode(lst):
    q = ""
    for character, count in lst:
        q += character * count
    return q


@given(text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s

if __name__ == "__main__":
    ## the following function automatically uses the search strategy (text())
    ## to test the function, and it finds the bug with ''
    test_decode_inverts_encode()
