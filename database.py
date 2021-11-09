import json

class Database:

    json_file = '.\Data\AllCards.json'
    #json data is in a list of dictionaries with each card being its own dictionary
    #so accesss like data[index]["value"]
    #json.dumps(card) will format nicely for printing
    data = []
    def __init__(self):
        with open(self.json_file, encoding="utf8") as json_data:
            self.data = json.load(json_data)


#Colors are in the data as follows: Green=G, Blue=U, Black=B, White=W, Red=R
    #Returns cards that have the given color in their cost(can return multicolor)
    def searchByColor(self, color):
        results = []
        for card in self.data:
            if 'colors' in card:
                for colors in card['colors']:
                    if(colors == color):
                        results.append(card)
                        break
        return results

    #Returns cards that only have a specified cost of the given color.(no multicolor cards)
    def searchBySingleColor(self, color):
        results = []
        for card in self.data:
            if 'colors' in card:
                if (color in card['colors'] and len(card['colors']) == 1):
                    results.append(card)
        return results

    #Returns cards of the given card type
    #Card type is capitalized: Creature, Sorcery, Instant, Artifact, Land...
    def searchByType(self, type):
        results = []
        for card in self.data:
            if 'type_line' in card:
                if (type in card['type_line']):
                    results.append(card)
        return results

    #Returns cards that have the specified keyword on their card text
    #Keywords are capitalized.
    def searchByKeyword(self, keyword):
        results = []
        for card in self.data:
            if 'keywords' in card:
                for keywords in card['keywords']:
                    if (keyword in card['keywords']):
                        results.append(card)
                        break
        return results

    #Returns cards that contain the given string in their name
    def searchByName(self, name):
        results = []
        for card in self.data:
            if 'name' in card:
                if (name in card['name']):
                    results.append(card)
        return results

    #Returns cards that have the exact given string as a name
    def searchByExactName(self, name):
        results = []
        for card in self.data:
            if 'name' in card:
                if (name == card['name']):
                    results.append(card)
        return results

    #Returns cards that are the given cost
    #cmc needs to be a number and not string
    def searchByCMC(self, cmc):
        results = []
        for card in self.data:
            if 'cmc' in card:
                if (cmc == card['cmc']):
                    results.append(card)
        return results

    #Returns cards that have the given string anywhere in their rules text
    #Used to find broad statements such as: creature gets, destroy all, ...
    def searchByRulesText(self, rules):
        results = []
        for card in self.data:
            if 'oracle_text' in card:
                if (rules in card['oracle_text']):
                    results.append(card)
        return results


