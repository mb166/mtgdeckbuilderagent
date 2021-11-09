import json

class DeckBuilder:
    deck = []
    possibleCards = []
    cmcList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    manaCurve = [ 6, 8, 8, 5, 4, 2, 2]
    costList = [0, 0, 0, 0, 0, 0, 0]
    color = []

    def __init__(self, possibles, colors):
        self.possibleCards = possibles
        self.buildCMCList()
        self.color = colors
        

#build a list of cards organized by cmc
    def buildCMCList(self):
        for card in self.possibleCards:
            self.cmcList[int(card['cmc'])].append(card)

    def build(self):
        counter = 0
        for manaCost in self.manaCurve:            
            for card in self.cmcList[counter+1]:
                if self.costList[counter] < self.manaCurve[counter]:
                    self.deck.append(card)
                    self.costList[counter] += 1
            counter += 1

    def printDeck(self):
        counter = 0
        for card in self.deck:
            counter +=1
            card = '{0: <50}'.format(str(counter) + '. ' + card['name'] + " " +  " " + card['mana_cost'])
            print(card)

        lands = '{0: <50}'.format('36-60' + '. ' + self.getLandType())
        print(lands)
        
    def getLandType(self):
        switch = {
            'G': 'Forest',
            'U': 'Island',
            'B': 'Swamp',
            'W': 'Plains',
            'R': 'Mountain'
        }
        return switch.get(self.color)