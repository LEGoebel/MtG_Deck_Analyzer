import unittest
from mtg_analyzer.deck_analyzer import parse_decklist

class TestDeckAnalyzer(unittest.TestCase):
    def test_parse_decklist_valid(self):
        decklist = [
            "4 Lightning Bolt",
            "2 Mountain",
            "1 Black Lotus",
            "2 Mable, Heir to Cragflame"
        ]
        expected_output = [
            {'cmc': 1.0, 'colors': ['R'], 'count': 4, 'name': 'Lightning Bolt'},
            {'cmc': 0.0, 'colors': [], 'count': 2, 'name': 'Mountain'},
            {'cmc': 0.0, 'colors': [], 'count': 1, 'name': 'Black Lotus'},
            {'cmc': 3.0, 'colors': ['R', 'W'],'count': 2,'name': 'Mable, Heir to Cragflame'}
        ]
        result = parse_decklist(decklist)
        self.assertEqual(result, expected_output)
    
    def test_parse_decklist_empty(self):
        decklist = []
        expected_output = []
        result = parse_decklist(decklist)
        self.assertEqual(result, expected_output)
    
    def test_parse_decklist_invalid_format(self):
        decklist = [
            "4Lightning Bolt",
            "2 Mountain",
            "Not a valid card"
        ]
        expected_output = [
            {'count': 2, 'name': 'Mountain', 'cmc': 0.0, 'colors': []}
            # Die ungültigen Zeilen werden ignoriert
        ]
        result = parse_decklist(decklist)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
