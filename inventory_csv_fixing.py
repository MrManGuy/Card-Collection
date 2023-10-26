import json, re, time

def main():
    #Open the csv file with all cards
    with open("tcginventory-7-18-23.csv", newline='') as inventory:
        inventory = [x.strip("\r\n").split(",") for x in inventory]
        
        with open("pokemon_tcg_ids.json") as pokemon_ids:
            output = "CardName,CardNum,SetID,Normal,Holo,Reverse\n"
            set_dictionary = json.load(pokemon_ids)

            for i in range(1, len(inventory)):
                if "Pokemon" in inventory[i][2]:
                    normal, holo, reverse = 0, 0, 0
                    #Detemine if the card is a holo, reverse, or normal
                    if "[Holofoil]" in inventory[i][1] or "[Unlimited Holofoil]" in inventory[i][1] or "[1st Edition Holofoil]" in inventory[i][1]:
                        holo += int(inventory[i][0])
                    elif "[Reverse Holofoil]" in inventory[i][1]:
                        reverse += int(inventory[i][0])
                    else:
                        normal += int(inventory[i][0])
                    
                    set_id = set_dictionary[inventory[i][3]]['id']

                    card_name = inventory[i][1].strip()
                    card_num = ""

                    #If a card has a dash isolate the name of the card
                    if " - " in card_name:
                        card_name_list = card_name.split(" - ")
                        card_name = card_name_list[0].strip()
                        if "/" in card_name_list[1]:
                            card_num = str(int(card_name_list[1].split("/")[0].strip()))

                    #If the card contains a set number in parathesis seperated that
                    if re.search("\([0-9]+\)", card_name) != None:
                        card_name_list = card_name.split("(")
                        card_num = str(int(card_name_list[1][:-1]))
                        card_name = card_name_list[0].strip()

                    #If the card has already been added with update the normal, holo, and reverse counts
                    if f"{card_name},{card_num},{set_id}," in output:
                        output = output.split("\n")
                        new_line = ""
                        line_pos = 0
                        for j, line in enumerate(output):
                            if f"{card_name},{card_num},{set_id}," in line:
                                 line_pos = j
                                 new_line = line.split(",")
                                 new_line[3] = str(int(new_line[3]) + normal)
                                 new_line[4] = str(int(new_line[4]) + holo)
                                 new_line[5] = str(int(new_line[5]) + reverse)
                                 new_line = ",".join(new_line)
                                 break
                            
                        output[line_pos] = new_line
                        output = "\n".join(output)
                    else:
                        output += f"{card_name},{card_num},{set_id},{normal},{holo},{reverse}\n"
            with open("pokemon_fixed_cards.csv", "w") as output_file:
                output_file.write(output.strip('\n'))

if __name__ == "__main__":
    startTime = time.time()
    main()
    print(time.time() - startTime)
