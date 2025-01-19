from pathlib import Path

import argparse
import os
import random
import string

letters = string.ascii_letters
numbers = string.octdigits
symbols = "-_"

DEFAULT_SAVELOCATION = os.path.join(Path(__file__).parent, "saved_usernames.txt")
WORKING_DIRECTORY = Path(DEFAULT_SAVELOCATION).parent

def start(        
        source = "None",
        max_username_length = 32,
        save_location = DEFAULT_SAVELOCATION
):
    
    first_run = True
    while True:
        mode = ""
        if first_run == False:
            mode = input("Want another name? Y/n\n> ")
        if mode == "Y" or mode == "y" or mode == "\n" or  mode == "" or first_run == True:
            username = generate_username(source, max_username_length)
            print(f"\n{username}     Length of name: {len(username)}.")
            mode = input("Want to save name? y/N\n> ")
            if mode == "Y" or mode == "y":
                save(save_location, username)
            try: # By typing 'username' -s when prompted it saves name typed. Example: > OXRAVEBUGBLOOD -s    <-- saves OXRAVEBUGBLOOD to file
                if len(mode.split(" ")) == 2 and mode.split(" ")[1] == "-s":
                    save(save_location, mode.split(" ")[0])
                    print("\n** Saved username\n")
            except:
                pass

        elif mode == "n" or mode == "N":
            break
        first_run = False

def generate_username(
        source = "None",
        max_username_length = 32,
        save_location = DEFAULT_SAVELOCATION
    ):

    list_of_names = [
        "neck",
        "crack",
        "driver",
        "dopamine",
    ]

    username = ""
    
    if source != "None": # Loading user defined list
        list_of_names = load_from_source(source)
        for i, e in enumerate(list_of_names): # Filtering out breakline char, and grabbing actual word/name
            list_of_names[i] = e.split(f"\n")[0]

    smallest_word_in_length = find_smallest_length_of_name(list_of_names)

    while True:
        if len(username) == max_username_length:
            break
        elif len(username) + smallest_word_in_length > max_username_length:
            break

        rolled_name = list_of_names[random.randint(0, len(list_of_names) - 1)]
        if len(username) + len(rolled_name) > max_username_length:
            continue
        if rolled_name in username: # Is a quick but not accurate fix might expand on this in the future
            continue

        if random.randint(0, 100) > 92: # Rolling for characters front
            username = roll_random_chars(username, max_username_length)

        if len(rolled_name) + len(username) <= max_username_length:
            username = username + rolled_name

        if random.randint(0, 100) > 92: # Rolling for characters back
            username = roll_random_chars(username, max_username_length)
        if random.randint(0, 100) > 92: # Rolling for random stop
            break

    # Post processing
    if random.randint(0, 100) > 50: # Rolling for uppercase name
        username = username.upper()
    if random.randint(0, 100) > 80: # Rolling for is a,e,i,o, to be replaced with numbers instead
        username_list = list(username)
        all_letters_to_numbers_lucky_roll = True if random.randint(0, 100) > 93 else False
        for i, c in enumerate(username):
            roll = random.randint(0, 100)
            #print(roll, c)
            if roll > 80 or all_letters_to_numbers_lucky_roll:
                if c == "a" or c == "A":
                    username_list[i] = "4"
                elif c == "o" or c == "O":
                    username_list[i] = "0"
                elif c == "i" or c == "i":
                    username_list[i] = "1"
                elif c == "e" or c == "E":
                    username_list[i] = "3"

        username = ""
        for e in username_list:
            username += e
    return username

def roll_random_chars(username, max_username_length):
    min_length = 1
    max_length = 4
    length = None
    if len(username) <= max_username_length - min_length:
        while True: # Rolling for amount of random chars
            length = random.randint(min_length, max_length)
            if length + len(username) <= max_username_length:
                break # Is valid length
        for i in range(length):
            choice = random.randrange(0, 3)
            if choice == 0: # Chooses letters
                n = random.randrange(0, len(letters))
                username = username + letters[n]
            elif choice == 1: # Chooses a digit
                n = random.randrange(0, len(numbers))
                username = username + numbers[n]
            elif choice == 2: # Chooses a symbol
                n = random.randrange(0, len(symbols))
                username = username + symbols[n]
    return username

def save(save_location, username):
    if os.path.isdir(save_location): # If save location is a directory it creates a new file and appends text to it
        save_file = os.path.join(save_location, "saved_usernames.txt")
        with open(f"{save_file}", "w") as f:
            f.write(f"{username}\n")
    else: # Save location specified is an already existing file. Appends text to file.
        with open(f"{save_location}", "a") as f:
            f.write(f"{username}\n")
        
def load_from_source(source):
    if "/" not in source or "\\" not in source:
        source = os.path.join(WORKING_DIRECTORY, source)
    with open(source) as file:
        file_lines = file.readlines()
    return file_lines

def find_smallest_length_of_name(lst):
    smallest = len(lst[0])
    for e in lst:
        if len(e) < smallest:
            smallest = len(e)
    return smallest
        
def parse_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type = str, default = "None", help = "user can specify a txt file with user saved names to generate from.")
    parser.add_argument('--save-location', type = str, default = DEFAULT_SAVELOCATION, help = "sets the save location for processed names, please specify using absolute path. Can also use relative path.")
    parser.add_argument('--max-username-length', type = int, default = 16, help = "sets the max length a generated username can have.")

    return parser.parse_args()

if __name__ == "__main__":
    kwargs = parse_kwargs()
    start(**vars(kwargs))