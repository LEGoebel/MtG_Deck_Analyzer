import unittest
from unittest.mock import patch, MagicMock
from mtg_analyzer.deck_analyzer import parse_decklist, analyze_deck, create_mana_curve_chart, create_color_distribution_pie_chart, create_combined_chart


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
        
    @patch('mtg_analyzer.deck_analyzer.create_combined_chart')
    def test_analyze_deck(self, mock_create_combined_chart):
        deck = [
            {'count': 4, 'name': 'Lightning Bolt', 'cmc': 1.0, 'colors': ['R']},
            {'count': 2, 'name': 'Mountain', 'cmc': 0.0, 'colors': []}
        ]
        result = analyze_deck(deck)
        expected_mana_curve = {0: 2, 1: 4, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, '10+': 0}
        expected_color_distribution = {'W': 0, 'U': 0, 'B': 0, 'R': 4, 'G': 0, 'C': 2, 'M': 0}
        self.assertEqual(result['mana_curve'], expected_mana_curve)
        self.assertEqual(result['color_distribution'], expected_color_distribution)
        self.assertAlmostEqual(result['average_cmc'], 0.67, places=2)

    @patch('mtg_analyzer.deck_analyzer.plt.savefig')
    def test_create_mana_curve_chart(self, mock_savefig):
        mana_curve = {0: 2, 1: 4, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, '10+': 0}
        create_mana_curve_chart(mana_curve)
        mock_savefig.assert_called()

    @patch('mtg_analyzer.deck_analyzer.plt.savefig')
    def test_create_color_distribution_pie_chart(self, mock_savefig):
        color_distribution = {'W': 1, 'U': 2, 'B': 1, 'R': 3, 'G': 0, 'C': 1, 'M': 2}
        create_color_distribution_pie_chart(color_distribution)
        mock_savefig.assert_called()

if __name__ == '__main__':
    unittest.main()
