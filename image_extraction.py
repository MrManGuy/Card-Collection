import requests, json, os
import time

offset = 0
missed = ["swsh10.json", "swsh11.json", "swshp.json", "xy12.json"]
card_type = "Pokemon"
def main():
    running_path = os.getcwd() + "\\Card-Collection"  #Folder with all things related to that game
    game_path = os.path.dirname(running_path) + '\\' + card_type
    card_sets_path = os.path.dirname(running_path) + '\\' + card_type + "\\sets" #Folder with all sets

    files = os.listdir(card_sets_path)
    for i, set_file in enumerate(files[offset:]):
        image_folder_path = game_path + "\\imgs\\" + set_file[:-4] #Folder with all imgs
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        current_imgs = os.listdir(game_path + "\\imgs\\" + set_file[:-4])
        print("Starting file:", i + 1 + offset, " File name:", set_file)
        try:
            with open(card_sets_path + "\\" + set_file, 'r') as file:
                cardList = json.load(file)
                for card in cardList:
                    img_data = requests.get(card["images"]["small"]).content
                    card_id = card["id"]
                    card_id = card_id.replace("?", "question")
                    if card_id + ".png" not in current_imgs:
                        with open(image_folder_path + "\\" + card_id + ".png", 'wb') as handler:
                            handler.write(img_data)
        except:
            print("Error in file:", i + 1 + offset, " File name:", set_file)
            missed.append(i + 1 + offset)

if __name__ == "__main__":
    startTime = time.time()
    main()
    print(time.time() - startTime)
    print("List of missed sets:" + ", ".join(missed))