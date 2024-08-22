from typing import Final
import os
import csv
from dotenv import load_dotenv
import discord
from mtg_analyzer.deck_analyzer import parse_decklist, analyze_deck, create_mana_curve_chart
from mtg_analyzer.scryfall_api import get_card_data

# .env Datei laden
load_dotenv()

# Discord Token aus der Umgebungsvariable laden
TOKEN: Final[str] =  os.getenv('SECRET_KEY')

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Bot Startup
@client.event
async def on_ready():
    print(f'Bot ist bereit! Eingeloggt als {client.user}')
    
# Handling incoming messages
@client.event
async def on_message(message):
    # Ignoriere Nachrichten, die vom Bot selbst kommen
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')

    if message.content.startswith('!analyze'):
        decklist_input = []

        # Überprüfe, ob eine Textdatei angehängt ist
        if message.attachments:
            attachment = message.attachments[0]
            if attachment.filename.endswith('.txt'):
                # Lade die Textdatei herunter
                txt_path = f"./{attachment.filename}"
                await attachment.save(txt_path)
                
                # Lese die Textdatei
                with open(txt_path, 'r', encoding='utf-8') as txtfile:
                    decklist_input = [line.strip() for line in txtfile if line.strip()]
                
                # Lösche die temporäre Textdatei nach der Verarbeitung
                os.remove(txt_path)
            else:
                await message.channel.send("Bitte lade eine gültige Textdatei (.txt) hoch.")
                return
        else:
            decklist_input = message.content[len('!analyze'):].strip().splitlines()

        # Überprüfe das Format der Eingabe
        if all(line.strip() and line.split(' ', 1)[0].isdigit() for line in decklist_input):
            deck = parse_decklist(decklist_input)
            analysis = analyze_deck(deck)
            
            await message.channel.send(file=discord.File('deck_analysis.png'))
            await message.channel.send(f"Durchschnittliche CMC: {analysis['average_cmc']}")
        else:
            # Sende eine Fehlermeldung bei ungültiger Eingabe
            await message.channel.send(
                "Das Eingabeformat ist ungültig. Eine korrekte Eingabe einer Deckliste ist z.B.:\n\n"
                "!analyze\n"
                "4 Lightning Bolt\n"
                "2 Llanowar Elves\n"
                "1 Black Lotus\n"
                "..."
            )

    elif message.content.startswith('!card'):
        card_name = message.content[len('!card'):].strip()
        card_data = get_card_data(card_name)

        if card_data:
            embed = discord.Embed(
                title=card_data['name'],
                description=f"Type: {card_data['type_line']}\nText: {card_data['oracle_text']}\nSet: {card_data['set_name']}",
                color=discord.Color.blue()
            )
            embed.set_image(url=card_data['image_uris']["normal"])
            
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Card not found or there was an error fetching the data.")
        

def run_bot():
    client.run(token=TOKEN)