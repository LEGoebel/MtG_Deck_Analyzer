import unittest
from unittest.mock import patch
from mtg_analyzer.scryfall_api import get_card_data

class TestScryfallAPI(unittest.TestCase):
    @patch('mtg_analyzer.scryfall_api.requests.get')
    def test_get_card_data_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Black Lotus",
            "type_line": "Artifact",
            "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
            "set_name": "Alpha"
        }

        card_name = "Black Lotus"
        result = get_card_data(card_name)
        expected_output = {
            "name": "Black Lotus",
            "type_line": "Artifact",
            "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
            "set_name": "Alpha"
        }
        self.assertEqual(result, expected_output)

    @patch('mtg_analyzer.scryfall_api.requests.get')
    def test_get_card_data_not_found(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = {"details": "Card not found."}

        card_name = "Nonexistent Card"
        result = get_card_data(card_name)
        expected_output = None  # Angenommen, fetch_card_data gibt None zurück, wenn die Karte nicht gefunden wird
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
