Magic: The Gathering Deck Analyzer Projekt

Ziel:
- Ein Magic: The Gathering Deck Analyzer, welcher einem erlaubt einzelne Karten zu analysieren (Daten von Scryfall erhalten),
  Decklisten zu laden und diese dann auf z.B. Manakosten, Farbbalance, Verteilung von Kartentypen analysiert.


Ziel erreicht. Vorerst fertiggestelltes Projekt. Plane dieses Projekt zwar nochmals zu besuchen, dann aber vielleicht neu
aufzulegen, da ich hoffe, dass meine Arbeitsweise sich entsprechend weiterentwickelt.
Gelernte Dinge: 
- Implementierung von API-Calls ("offene" Scryfall API)
- Einfache Analyse eines Decks implementiert
- Discord Bot implementiert und entsprechend eingebunden
- Unit - Tests helfen beim sicherstellen des Fortschrittes.



MVP:
Input:
- Einzelkartensuche  Done
- Deckliste hinzufügen (.txt Datei mit # Karte in jeder einzelnen Zeile) Done

Daten:
- Karten Abfrage per API von scryfall.com - Done
- Caching der Daten, um unnötige Abfragen zu vermeiden - Done

Analyzer:
- Berechnen der Mana-Kurve -Done
- Visualisierung Mana- Kurve - Done
- Farbverteilung in % - Done
- Visualisierung der Farbverteilung - Done
- Durchschnittliche Manakosten des Decks - Done
- Verteilung von Kartentypen - Verworfen

Ausgabe:
- in Konsole bzw. als Antwort in Discord Server - Done
- in .txt Datei - Verworfen



Zusätzliche Optionen:
- Visualisierung der Daten (Manakurve, Pie-Chart etc.) - Done
- Genauere Analyse der Farbverteilung (z.B. "Auf CMC 3 kosten alle deine Karten 2 Rote Mana") - Verworfen
- Deck Vergleich (Grafiken übereinanderlegen) - Verworfen



Anleitung/Manual:

Um den Bot zu benutzen musst du selbst einen Account im Discord Developer Portal haben und dort einen Bot erstellen.
Den Token, welchen du erhältst musst du in eine Datei, welche exakt .env heißt einfügen.

Eine Vorlage ist:


APPLICATION_ID = "123456789101112131415"
PUBLIC_KEY = "a1b2c3d4e5f6g7h8i9j10k11l12"
SECRET_KEY = "abcdefghijklmnopqrstuvwxyz123456789"

Dann lädst du den Bot korrekt ein und lässt das Programm in VS Code o.Ä. laufen.