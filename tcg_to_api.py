import json

with open('Sets/all_pokemon.json') as file:
    card_set_list = json.load(file)
    card_set_list = card_set_list['data']
    output = "{"

    with open('tcgsets.csv') as sets:
        sets = [x.strip("\r\n") for x in sets]

        for card_set in card_set_list:
            print(card_set['id'], card_set['name'])
            foundMatch = False
            for row in sets:
                if card_set['name'] == row:
                    foundMatch = True
            
            if not foundMatch:
                name = input()
                while name not in sets and name != "STOP":
                    name = input()
            else:
                name = card_set['name']

            if name == "STOP":
                break
            output += '"' + name + '":{"id":"' + card_set['id'] + '"},'
    output += "}"

    with open("pokemon_tcg_ids.json", "w") as file2:
        file2.write(output)