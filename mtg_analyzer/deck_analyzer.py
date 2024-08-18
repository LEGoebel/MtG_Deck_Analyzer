from mtg_analyzer.scryfall_api import get_card_data

def parse_decklist(decklist):
    parsed_deck = []
    for line in decklist:  # Iteriere direkt über die Liste
        if line.strip():  # Ignoriere leere Zeilen
            parts = line.split(' ', 1)
            if len(parts) == 2 and parts[0].isdigit():  # Stelle sicher, dass 'count' eine Zahl ist
                count, card_name = parts
                card_data = get_card_data(card_name.strip())
                if card_data:
                    parsed_deck.append({
                        'count': int(count),
                        'name': card_name.strip(),
                        'cmc': card_data.get('cmc', 0),
                        'colors': card_data.get('colors', [])
                    })
            else:
                print(f"Warnung: Ungültige Zeile übersprungen: {line}")
    return parsed_deck

def analyze_deck(deck: list[dict]) -> dict:
    mana_curve = {}
    color_distribution = {}
    for card in deck:
        cmc = card['cmc']
        colors = card['colors'] or ['Colorless']
        for _ in range(card['count']):
            mana_curve[cmc] = mana_curve.get(cmc, 0) + 1
            for color in colors:
                color_distribution[color] = color_distribution.get(color, 0) + 1
    return {'mana_curve': mana_curve, 'color_distribution': color_distribution}