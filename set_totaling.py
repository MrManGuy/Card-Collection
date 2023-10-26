import json, copy, re

with open('pokemon_fixed_cards.csv', "r") as card_list:
    card_list = card_list.read().split('\n')
    current_set = ''
    current_open_set = ''
    not_counted = ''
    for row in card_list[1:]:
        row_list = row.split(",")
        if current_set != row_list[2]:
            if current_set != '':
                with open('Sets/' + current_set + '.json', 'w') as file:
                    file.write(json.dumps(current_open_set))
            current_set = row_list[2]
            with open('Sets/' + current_set + '.json') as file:
                current_open_set = json.load(file)
        
        found_row = False
        for card in current_open_set:
            #Check by number
            if row_list[1] != '':
                if card['number'] == row_list[1]:
                    found_row = True
            #Is a prime mon
            elif "(Prime)" in row_list[0]:
                if 'Prime' in card['subtypes']:
                    if row_list[0].replace(' (Prime)', '') == card['name']:
                        found_row = True
            #Is a team plasma mon
            elif "(Team Plasma)" in row_list[0]:
                if "Team Plasma" in card['subtypes']:
                    if row_list[0].replace(' (Team Plasma)', '') == card['name']:
                        found_row = True
            #Is an unown
            elif 'Unown' in row_list[0]:
                temp = ''
                if '[' in row_list[0]:
                    temp = row_list[0].split('[')
                else:
                    temp = row_list[0].split('(')
                
                unown_id = current_set + '-' + temp[1][0]
                if card['id'] == unown_id or card['name'] == row_list[0].replace('(','').replace(')','').replace('[','').replace(']',''):
                    found_row = True
            elif '(Secret)' in row_list[0]:
                if row_list[0].replace(' (Secret)', '') == card['name'] and int(card['number']) > int(card['set']['printedTotal']):
                    found_row = True
            #Check by name
            else:
                if card['name'].replace("\u00e9", "e").replace('\u2642', 'M').replace('\u2640', 'F').replace('\u03b4', '(Delta Species)') == row_list[0]:
                    found_row = True
                

            if found_row:
                card['owned'] = {
                    'normal': row_list[3],
                    'holo': row_list[4],
                    'reverse': row_list[5],
                    'have': 'true'
                }
                break

        if not found_row:
            not_counted += row + '\n'

    with open('pokemon_unable_to_find.csv', "w") as file:
        file.write(not_counted.strip('\n'))


with open("pokemon_tcg_ids.json") as pokemon_ids:
    pokemon_ids = json.load(pokemon_ids)
    output = '<html><head><link rel="stylesheet" href="card_styles.css"></head><body><div class="main-container">'
    for key in pokemon_ids:
        if 'ids' not in pokemon_ids[key]:
            with open('Sets/' + pokemon_ids[key]['id'] + '.json', 'r') as current_set:
                set_output = ''
                current_set = json.load(current_set)
                unique_cards = 0
                for card in current_set:
                    if 'owned' in card and 'have' in card['owned']:
                        if card['owned']['have'] == 'true':
                            unique_cards += 1
                            set_output += '<div class="pokemon-card have"><img class="pokemon-card-img" src="' + card['images']['small'].replace('https://images.pokemontcg.io', 'Imgs/Pokemon') +'"/><h3 class="pokemon-card-text">' + card['name'] + ' - ' + card['number'] + ' - ' + card['owned']['normal'] + ' - ' + card['owned']['holo'] + ' - ' + card['owned']['reverse'] + '</h3></div>'
                    else:
                        set_output += '<div class="pokemon-card"><img class="pokemon-card-img" src="' + card['images']['small'].replace('https://images.pokemontcg.io', 'Imgs/Pokemon') +'"/><h3 class="pokemon-card-text">' + card['name'] + ' - ' + card['number'] + '</h3></div>'
                percentage_complete = 100 * (unique_cards / card['set']['total'])
                output += '<details class="pokemon-set"><summary class="pokemon-set-title" style="background: linear-gradient(to right, rgb(140, 255, 140) ' + str(percentage_complete) + '%, white ' + str(percentage_complete) + '%);">' + key + ' - ' + str(unique_cards) + '/' + str(card['set']['printedTotal'])+ ' (' + str(card['set']['total']) +  ')</summary><div class="pokemon-card-container">'
                output += set_output
                output += '</div></details>'
    output += '</div></body></html>'
    with open('pokemon_tracker.html', 'w', encoding="utf-8") as file:
        file.write(output)