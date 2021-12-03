import json

class DeckBuilder:
    deck = []
    possibleCards = []
    cmcList = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    #aggro nonland cards - 38 land - 22
    #midrange nonland cards - 36 land - 24
    #control nonland cards - 34 land - 26
    creatureCount = 0
    nonCreatureCount = 0
    manaCurveContainer = {
        "aggro": [ 0, 12, 16, 10],
        "midrange": [ 0, 6, 8, 14, 4, 2, 2],
        "control": [ 0, 0, 7, 12, 5, 5, 3, 2]
    }
    creatureAmountContainer = {
        "aggro": 24,
        "midrange": 18,
        "control": 6
    }
    nonCreatureAmountContainer = {
        "aggro": 14,
        "midrange": 18,
        "control": 28
    }
    landAmountContainer = {
        "aggro": 22,
        "midrange": 24,
        "control": 26
    }
    manaCurve = []
    costList = [0, 0, 0, 0, 0, 0, 0, 0]
    color = []
    archetype = ""

    def __init__(self, possibles, colors, archetype):
        self.possibleCards = possibles
        self.buildCMCList()
        self.color = colors
        self.archetype = archetype
        self.manaCurve = self.manaCurveContainer[archetype]
        

#build a list of cards organized by cmc
    def buildCMCList(self):
        for card in self.possibleCards:
            self.cmcList[int(card["cmc"])].append(card)

    def build(self):
        counter = 0
        for manaCost in self.manaCurve:            
            for card in self.cmcList[counter+1]:
                #evaluate card
                cardScore = self.evaluateCard(card)

                #test for manacurve
                if self.costList[counter] < self.manaCurve[counter]:
                    #creature
                    if "creature" in card["type_line"].lower():
                        if self.creatureCount < self.creatureAmountContainer[self.archetype]:
                            cardTuple = (cardScore, card)
                            self.deck.append(cardTuple)
                            self.costList[counter] += 1
                            self.creatureCount += 1
                        else:
                            #need to test card against all other creatures currently in deck and see if it can be swapped
                            self.trimDeck(card, cardScore, "creature")

                    #noncreature
                    else:
                        if self.nonCreatureCount < self.nonCreatureAmountContainer[self.archetype]:                 
                            cardTuple = (cardScore, card)
                            self.deck.append(cardTuple)
                            self.costList[counter] += 1
                            self.nonCreatureCount += 1
                        else:
                            #need to test card against all other nonCreatures currently in deck
                            self.trimDeck(card, cardScore, "nonCreature")
                else:
                    self.trimDeck(card, cardScore, "cmc")
            counter += 1

#used to keep deck numbers in check
    def trimDeck(self, card, cardScore, trimReason):
        #if reason for trimming was mana cost then determine if the card is creature or not and recursively call this function with correct reason     
        if(trimReason == "cmc"):
            if card["type_line"].lower() == "creature":
                self.trimDeck(card, cardScore, "creature")
            else:
                self.trimDeck(card, cardScore, "nonCreature")
            return

        for cardTuple in self.deck:
            score = cardTuple[0]
            deckCard = cardTuple[1]
            if(score < cardScore):
                if(trimReason == "creature"):
                    if(deckCard["type_line"].lower() == "creature" and deckCard["cmc"] == card["cmc"]):
                        self.deck.remove(deckCard)
                        self.deck.append((cardScore, card))
                        return
                if(trimReason == "nonCreature"):
                    if(deckCard["type_line"].lower() != "creature" and deckCard["cmc"] == card["cmc"]):
                        self.deck.remove((score, deckCard))
                        self.deck.append((cardScore, card))
                        return

    #evaluates cards based on keywords
    def evaluateCard(self, card):
        
        rulesText = card.get("oracle_text")
        if rulesText == None:
            return 0
        cardType = card.get("type_line")
        if cardType == None:
            return 0
        score = 0
        rulesText = rulesText.lower()

        #checking if card type is permanent
        #case for nonpermanent
        if(cardType == "sorcery") or (cardType == "instant"):
            if "destroy" in rulesText:
                score += 2
                if "all" in rulesText:
                    score += 3
                    if "nonland" in rulesText:
                        score -= 1
            if("draw" in rulesText):
                score += 2
            if("discard" in rulesText):
                score -= 1            
            if("damage to target" in rulesText):
                score += 1
            if("exile target" in rulesText):
                score += 3
            if("target creature gets +" in rulesText):
                score += 1
                if "and" in rulesText:
                    score += 1

            #giving more weight to instants
            if (cardType == "instant"):
                score += 1


        #card is permanent
        else:
            if(cardType == "creature"):
                #power
                if card["power"] < card["cmc"] and card["power" != "*"]:
                    score -= 1
                if card["power"] == card["cmc"] and card["power" != "*"]:
                    score += 1
                if card["power"] > card["cmc"] and card["power" != "*"]:
                    score += 2

                #toughness
                if card["toughness"] < card["cmc"] and card["toughness" != "*"]:
                    score -= 1
                if card["toughness"] == card["cmc"] and card["toughness" != "*"]:
                    score += 1
                if card["toughness"] > card["cmc"] and card["toughness" != "*"]:
                    score += 2

                #scores for keyword abilities
                if "Defender" in card["keywords"]:
                    score -= 1
                if "Deathtouch" in card["keywords"] or "Regenerate" in card["keywords"] or "Reach" in card["keywords"]:
                    score += 1
                if "Flying" in card["keywords"] or "Trample" in card["keywords"] or "Menace" in card["keywords"] or "Horsemanship" in card["keywords"] or "Haste" in card["keywords"] or "First strike" in card["keywords"] or \
                    "Haste" in card["keywords"] or "Intimidate" in card["keywords"] or "Protection" in card["keywords"]:
                    score += 2      
                if "Double strike" in card["keywords"] or "Lifelink" in card["keywords"] or "Hexproof" in card["keywords"]:
                    score += 3          
                if "Indestructible" in card["keywords"]:
                    score += 4

                
            if("draw" in rulesText):
                score += 2
            if("discard" in rulesText):
                score -= 1


        return score


    def printDeck(self):
        counter = 0
        for cardTuple in self.deck:
            counter +=1
            card = cardTuple[1]
            cardPrint = '{0: <50}'.format(str(counter) + '. ' + card['name'] + " " +  " " + card['mana_cost'])
            print(cardPrint)

        landNum = 61 - self.landAmountContainer[self.archetype]
        lands = '{0: <50}'.format(str(landNum) + '-60' + '. ' + self.getLandType())
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