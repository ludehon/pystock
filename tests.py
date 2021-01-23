import pytest
from words import wordFreq

# usage : pytest -q tests.py
class Tester:
    def test_count(self):
        wf = wordFreq()
        content = "these are english words apple aapl  TESLA, pltr: "
        wf.addWords(content)
        assert(len(wf.count.keys()) == 3)
        assert(wf.count["aapl"] == 1)
        assert(wf.count["tsla"] == 1)
        assert(wf.count["pltr"] == 1)
        