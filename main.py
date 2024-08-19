from mtg_analyzer.deck_analyzer import parse_decklist, analyze_deck

def main():
    decklist =[
    "4 Mountain",
    "4 Lightning Bolt",
    "2 Sol Ring",
    "4 Mable, Heir to Cragflame",
    "4 Llanowar Elves",
    "1 Black Lotus"
    ]
    
    deck = parse_decklist(decklist)
    analysis = analyze_deck(deck)
    print("Mana Curve:", analysis['mana_curve'])
    print("Color Distribution:", analysis['color_distribution'])

if __name__ == "__main__":
    main()