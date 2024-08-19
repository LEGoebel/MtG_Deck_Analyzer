import unittest
from unittest.mock import patch
from mtg_analyzer.scryfall_api import get_card_data

class TestScryfallAPI(unittest.TestCase):
    @patch('mtg_analyzer.scryfall_api.requests.get')
    def test_get_card_data_success(self, mock_get):
        # Mocking der API Antwort
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            # Wir brauchen / wollen hier nur auf einige der Felder testen. Die vollständige Antwort der API
            # ist mehrere tausend Zeichen lang.
            "name": "Black Lotus",
            "type_line": "Artifact",
            "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
            "set_name": "Vintage Masters",
            "cmc": 0,
            "colors": [],
            "rarity": "rare"
        }

        card_name = "Black Lotus"
        result = get_card_data(card_name)

        # Der erwartete Output sollte gleich dem erhaltenen Output sein.
        expected_output = {
            "name": "Black Lotus",
            "type_line": "Artifact",
            "oracle_text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
            "set_name": "Vintage Masters"
        }

        # Check if the relevant fields in the result match the expected output
        self.assertEqual(result['name'], expected_output['name'])
        self.assertEqual(result['type_line'], expected_output['type_line'])
        self.assertEqual(result['oracle_text'], expected_output['oracle_text'])
        self.assertEqual(result['set_name'], expected_output['set_name'])

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
