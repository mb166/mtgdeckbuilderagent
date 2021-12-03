from database import Database
from deckbuilder import DeckBuilder

color = input("Enter desired deck color:")

archetype = input("Enter desired deck archetype:")

database = Database()
results = database.searchBySingleColor(color)
deckBuilder = DeckBuilder(results, color, archetype)
deckBuilder.build()
deckBuilder.printDeck()
