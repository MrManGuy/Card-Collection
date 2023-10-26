import json, requests

api_url = 'https://api.pokemontcg.io/v2/cards?q=set.id:'

with open("pokemon_tcg_ids.json") as pokemon_ids:
    pokemon_ids = json.load(pokemon_ids)

    for key in pokemon_ids:
        if 'ids' not in pokemon_ids[key]:
            acutal_data = []
            with open('Sets/' + pokemon_ids[key]['id'] + '.json', 'w') as current_set:
                print('Now doing: ' + pokemon_ids[key]['id'])
                r = requests.get(url = api_url + pokemon_ids[key]['id'] + "&orderBy=number")
                data = r.json()
                actual_data = data['data']
                if ((int(data['page']) - 1) * 250) + int(data['count']) < int(data['totalCount']):
                    r = requests.get(url = api_url + pokemon_ids[key]['id'] + "&page=2")
                    for card in r.json()['data']:
                        actual_data.append(card)

                current_set.write(json.dumps(actual_data))
        #We have no trainer kits so skip them for now
        else:
            continue
        