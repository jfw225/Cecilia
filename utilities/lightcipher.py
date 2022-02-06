import pandas as pd
from os import getcwd

# Define command dictionary.
CIPHER_PATH= f"{'' if not 'Cecilia' in getcwd() else 'utilities/'}lightcipher.xlsx"
df= pd.read_excel(CIPHER_PATH)
LIGHT_DICT= df.set_index('role')['num'].to_dict()
SPECIAL_DICT= df.set_index('special')['command'].to_dict()

# Define list of words to remove.
REMOVE_LIST= ['to', 'cc']

def get_command(audio):
    seperate_level_words= list()
    temp= list()
    for word in audio.split(): # checks for special words, removes words that cause issues, and seperates the words for two different commands
        if command:= SPECIAL_DICT.get(word): return command
        elif word not in REMOVE_LIST:
            if word == 'and':
                seperate_level_words.append([word for word in temp])
                temp.clear()
            else: temp.append(word)

    if temp: seperate_level_words.append(temp)

    print(seperate_level_words)

    seperate_level= list()
    for words in seperate_level_words: # analyzes words to try and seperate commands for different sections of the lights
        command= ''
        if 'bottom' in words or 'lower' in words: command+= 'r1 '
        elif 'top' in words or 'upper' in words: command+= 'r2 '
        elif len(seperate_level_words) == 1: command= 'r3 '
        #else: raise AssertionError

        word_count= dict() # keys are words in audio and in cipher, value is how many times it appears
        for role in LIGHT_DICT:
            for word in words:
                if word in role and all([role_word in words for role_word in role.split()]):
                    word_count[role]= word_count.get(role) + 1 if role in word_count else 1
        print(word_count)

        likely_role= str()
        highest_count= 0
        for role, count in word_count.items(): # determines the correct command based on count
            if count > highest_count:
                highest_count= count
                likely_role= role
        
        print(likely_role)
        if highest_count: seperate_level.append(command + str(LIGHT_DICT.get(likely_role)))
    print(seperate_level)

    if not all(['r' in command for command in seperate_level]):
        for i in range(len(seperate_level)):
            seperate_level[i]= f'r{i + 1} ' + seperate_level[i]
    print(seperate_level)
    return ','.join(seperate_level) + ','


if __name__ == '__main__':
    audio= 'cc turn the brightness down'
    #audio= 'cc turn the top lights brightness up'
    #audio= 'cc change top lights to red and bottom lights to yellow'
    #audio= 'cc change the top lights to light pink and bottom lights to reddish orange'
    #audio= 'switch the lights to baby blue and flash'
    #audio= 'turn the lights to large jump'

    command= get_command(audio)
    print(command)