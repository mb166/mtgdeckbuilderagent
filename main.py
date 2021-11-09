from database import Database
from deckbuilder import DeckBuilder

color = input("Enter desired deck color:")

database = Database()
results = database.searchBySingleColor(color)
deckBuilder = DeckBuilder(results, color)
deckBuilder.build()
deckBuilder.printDeck()
