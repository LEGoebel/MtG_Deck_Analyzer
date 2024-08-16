Magic: The Gathering Deck Analyzer Projekt

Ziel:
- Ein Magic: The Gathering Deck Analyzer, welcher einem erlaubt einzelne Karten in ein Deck hinzuzufügen,
  Decklisten zu laden und diese dann auf z.B. Manakosten, Farbbalance, Verteilung von Kartentypen analysiert.


MVP:
Input:
- Einzelkartensuche
- Deckliste hinzufügen (.txt Datei mit # Karte in jeder einzelnen Zeile)

Daten:
- Karten Abfrage per API von scryfall.com
- Caching der Daten, um unnötige Abfragen zu vermeiden

Analyzer:
- Berechnen der Mana-Kurve (noch ohne Visualisierung, entsprechend Liste mit Index -> Anzahl Karten mit diesen Kosten)
- Farbverteilung in %
- Durchschnittliche Manakosten des Decks
- Verteilung von Kartentypen

Ausgabe:
- in Konsole
- in .txt Datei



Zusätzliche Optionen:
- Visualisierung der Daten (Manakurve, Pie-Chart etc.)
- Genauere Analyse der Farbverteilung (z.B. "Auf CMC 3 kosten alle deine Karten 2 Rote Mana")
- Deck Vergleich (Grafiken übereinanderlegen)