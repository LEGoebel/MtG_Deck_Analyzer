from typing import Final
import os
from dotenv import load_dotenv
import discord
from mtg_analyzer.deck_analyzer import parse_decklist, analyze_deck
from mtg_analyzer.scryfall_api import get_card_data

# .env Datei laden
load_dotenv()

# Discord Token aus der Umgebungsvariable laden
TOKEN: Final[str] =  os.getenv('SECRET_KEY')

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# async def send_message(message, user_message) -> None:
#     if not user_message:
#         print('(Message was empty probably because the intents are not enabled correctly!)')
#         return
    
#     if is_private := user_message[0] == '?':
#         user_message = user_message[1:]
        
#     try:
#         response = get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)

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
        decklist_input = message.content[len('!analyze'):].strip().splitlines()
        deck = parse_decklist(decklist_input)
        analysis = analyze_deck(deck)

        response = (
            f"Mana Curve: {analysis['mana_curve']}\n"
            f"Color Distribution: {analysis['color_distribution']}"
        )

        await message.channel.send(response)

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