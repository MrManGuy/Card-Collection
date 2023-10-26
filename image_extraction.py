import requests, json, os
import time

def main():
    running_path = os.getcwd() + "\\" #Folder with all things related to that game

    with open("pokemon_tcg_ids.json") as pokemon_ids:
        pokemon_ids = json.load(pokemon_ids)
        for key in pokemon_ids:
            if 'ids' not in pokemon_ids[key]:
                with open('Sets/' + pokemon_ids[key]['id'] + '.json', 'r') as current_set:
                    current_set = json.load(current_set)
                    print('Working on: ' + key)
                    for card in current_set:
                        img = card['images']['small']
                        new_file_name = img.replace('https://images.pokemontcg.io', 'Imgs/Pokemon')
                        
                        if not os.path.exists(running_path + new_file_name[:new_file_name.rfind('/')]):
                            os.makedirs(running_path + new_file_name[:new_file_name.rfind('/')])

                        img_data = requests.get(img).content
                        with open(new_file_name, 'wb') as handler:
                            handler.write(img_data)
                        

if __name__ == "__main__":
    startTime = time.time()
    main()
    print(time.time() - startTime)