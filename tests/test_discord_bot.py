import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from discord_bot import client, on_message, on_ready

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):

    @patch('discord_bot.client')
    async def test_on_ready(self, mock_client):
        # Setze den Rückgabewert von user auf "BotUser", damit die Ausgabe bzw. der Vergleich korrekt ist
        mock_client.user = 'BotUser'
        with patch('builtins.print') as mock_print:
            await on_ready()
            mock_print.assert_called_with('Bot ist bereit! Eingeloggt als BotUser')

    @patch('discord_bot.get_card_data')
    async def test_on_message_analyze(self, mock_get_card_data):
        # Mocking der get_card_data Funktion
        mock_get_card_data.return_value = {'name': 'Lightning Bolt', 'type_line': 'Instant', 'oracle_text': 'Lightning Bolt deals 3 Damage to any target', 'set_name': 'Alpha', 'image_uris': {'normal': 'https://example.com/card.png'}}

        # Mocking des Events
        mock_message = AsyncMock()
        mock_message.content = '!analyze\n4 Lightning Bolt\n2 Lightning Bolt'
        mock_message.author = 'User'
        mock_message.attachments = []

        await on_message(mock_message)
        mock_message.channel.send.assert_called()  # Prüfen, ob die "send" Methode korrekt aufgerufen wurde

    @patch('discord_bot.get_card_data')
    async def test_on_message_card(self, mock_get_card_data):
        mock_get_card_data.return_value = {'name': 'Lightning Bolt', 'type_line': 'Instant', 'oracle_text': 'Lightning Bolt deals 3 Damage to any target', 'set_name': 'Alpha', 'image_uris': {'normal': 'https://example.com/card.png'}}
        mock_message = AsyncMock()
        mock_message.content = '!card Lightning Bolt'
        mock_message.author = 'User'
        mock_message.channel = AsyncMock()

        await on_message(mock_message)
        mock_message.channel.send.assert_called()

if __name__ == '__main__':
    unittest.main()