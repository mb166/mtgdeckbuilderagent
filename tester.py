from database import Database

database = Database()

results = database.searchByRulesText("creature gets")

counter = 0
for result in results:
    counter += 1
    print(result['name']," ",  counter)

