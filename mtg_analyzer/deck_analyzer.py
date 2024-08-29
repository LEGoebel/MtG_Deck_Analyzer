from mtg_analyzer.scryfall_api import get_card_data
import matplotlib.pyplot as plt
from PIL import Image
import os

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
    # Initialisiere Mana Kurve von 0 bis 10+. Heißt es geht von 0 bis 10 und danach gibt es nurnoch die Kategorie 10+
    mana_curve = {i: 0 for i in range(11)}
    mana_curve['10+'] = 0
    total_cmc = 0
    total_cards = 0
    
    # Farbverteilung initialisieren
    color_distribution = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0, 'M': 0}    #WUBRG + Colorless + Multicolor
    
    for card in deck:
        cmc = card.get('cmc', 0)
        count = card.get('count', 1)
        total_cmc += cmc * count
        total_cards += count
        colors = card.get('colors', [])
        
        # Mana-Kurve aktualisieren
        if cmc >= 10:
            mana_curve['10+'] += card['count']
        else:
            mana_curve[cmc] += card['count']
            
        # Farbverteilung aktualisieren
        if not colors:
            color_distribution['C'] += card['count']
        elif len(colors) > 1:
            color_distribution['M'] += card['count']
        else:
            for color in colors:
                color_distribution[color] += card['count']
              
    average_cmc = round(total_cmc / total_cards, 2) if total_cards > 0 else 0
        
    # Erstelle das Balkendiagramm für die Mana-Kurve
    create_combined_chart(mana_curve, color_distribution)

    return {
        'mana_curve': mana_curve,
        'color_distribution': color_distribution,
        'average_cmc': average_cmc
    }
        

    
def create_mana_curve_chart(mana_curve, filename = "Mana_Kurve.png"):
    cmc_values = []
    counts = []

    for cmc, count in mana_curve.items():
        if cmc == '10+':
            cmc_values.append(11)  # Du kannst 11 oder einen anderen höheren Wert verwenden
        else:
            cmc_values.append(int(cmc))
        counts.append(count)

    plt.bar(cmc_values, counts, color='lightblue')
    plt.xlabel('Mana-Kosten (CMC)')
    plt.ylabel('Anzahl Karten')
    plt.title('Manakurve')

    plt.savefig(filename)
    plt.close()


def create_color_distribution_pie_chart(color_distribution: dict, filename="Farbverteilung.png"):
    # Definiere die Farben für die Farbverteilung
    color_map = {
        'W': 'white',     # Weiß für White
        'U': 'blue',      # Blau für Blue
        'B': 'black',     # Schwarz für Black
        'R': 'red',       # Rot für Red
        'G': 'green',     # Grün für Green
        'C': 'gray',      # Grau für Colorless
        'M': 'gold'       # Gold für Multicolor
    }
    
    # Filtere Farben aus, die nicht im Deck vorhanden sind
    filtered_labels = [color for color in color_map.keys() if color_distribution.get(color, 0) > 0]
    filtered_sizes = [color_distribution[color] for color in filtered_labels]
    filtered_colors = [color_map[color] for color in filtered_labels]


    plt.figure(figsize=(8, 6))
    plt.pie(filtered_sizes, labels=filtered_labels, colors=filtered_colors, autopct='%1.1f%%', startangle=140, textprops={'color': 'black'})


    plt.axis('equal')  # Gleichmäßige Darstellung des Kuchendiagramms
    plt.title("Color Distribution")
    plt.savefig(filename)
    plt.close()
    
def create_combined_chart(mana_curve: dict, color_distribution: dict, filename="deck_analysis.png"):
    # Temporäre Dateinamen für die einzelnen Diagramme
    mana_curve_filename = "temp_mana_curve.png"
    color_distribution_filename = "temp_color_distribution.png"

    # Erstelle die einzelnen Diagramme und speichere sie als temporäre Dateien
    create_mana_curve_chart(mana_curve, filename=mana_curve_filename)
    create_color_distribution_pie_chart(color_distribution, filename=color_distribution_filename)

    # Lade die gespeicherten Bilder
    mana_curve_img = Image.open(mana_curve_filename)
    color_distribution_img = Image.open(color_distribution_filename)

    # Erstelle ein neues Bild mit ausreichend Platz für beide Diagramme
    total_width = mana_curve_img.width + color_distribution_img.width
    max_height = max(mana_curve_img.height, color_distribution_img.height)
    combined_img = Image.new('RGB', (total_width, max_height))

    # Füge die beiden Bilder nebeneinander in das neue Bild ein
    combined_img.paste(mana_curve_img, (0, 0))
    combined_img.paste(color_distribution_img, (mana_curve_img.width, 0))

    # Speichere das kombinierte Bild
    combined_img.save(filename)

    # Schließe die Bilder und entferne die temporären Dateien
    mana_curve_img.close()
    color_distribution_img.close()

    # Optional: Lösche die temporären Dateien nach dem Gebrauch
    os.remove(mana_curve_filename)
    os.remove(color_distribution_filename)