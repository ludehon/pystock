import pytest
from words import wordFreq

# usage : pytest -q tests.py
class Tester:
    def test_count(self):
        wf = wordFreq()
        content = "these are english words apple aapl  TESLA, micron mu: "
        wf.addWords(content)
        assert(len(wf.count.keys()) == 3)
        assert(wf.count["apple"] == "1")
        assert(wf.count["tesla"] == "1")
        assert(wf.count["micron"] == "1")
        