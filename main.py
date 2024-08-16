from mtg_analyzer.scryfall_api import get_card_data

def main():
    input_card = input("Geben Sie einen Kartennamen ein, um die Daten von scryfall.com zu erhalten.\n")
    print(get_card_data(input_card))
    
main()