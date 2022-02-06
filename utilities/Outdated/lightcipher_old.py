import pandas as pd

# Define command dictionary.
cipher_path= 'lightcipher.xlsx'
cipher_path= 'utilities/lightcipher.xlsx'
df= pd.read_excel(cipher_path)
LIGHT_DICT= df.set_index('role')['num'].to_dict()
SPECIAL_DICT= df.set_index('special')['command'].to_dict()

# Define list of words to remove.
removeList= ['to', 'cc']

def commandHelper(cipherList):
    exeList= list()
    for msg in cipherList:
        mlist= msg.split()
        com= ''
        if 'bottom' in mlist or 'lower' in mlist: com+= 'r1 '
        elif 'top' in mlist or 'upper' in mlist: com+= 'r2 '

        tempList= list()
        # Each match in the text file gets added to a seperate list. Also adds the specified relay to the command.
        for x in LIGHT_DICT:
            for y in mlist:
                if y in x: tempList.append(x)
        print(tempList)

        # The each word in the matches are checked to see if it appears at least once in the audio.
        for x in tempList:
            l= x.split()
            for y in l:
                if not y in mlist:
                    tempList.remove(x)
                    break
        print(tempList)

        # The matches are counted to see which one appears the most. The one that appears the most gets executed.
        tempCom= ''
        tempInt1= 0
        for x in tempList:
            tempInt2= tempList.count(x)
            if tempInt2 > tempInt1:
                tempInt1= tempInt2
                tempCom= x
        print(tempCom)

        # References command list for specific number.
        com+= str(LIGHT_DICT.get(tempCom))
        if com != 'None': exeList.append(com)
    return exeList


def cipher(cipher):
    executeList= list()

    # Splits up the statement by seperating by 'and'.
    cipherList= list()
    temp= cipher.split()
    print(SPECIAL_DICT.get('movie'))
    # First removes any unnecessary words. Also fixes 'cctop' issue.
    for x in temp:
        print(x)
        if com:= SPECIAL_DICT.get(x):
            print(com)
            return com

        if 'top' in x:
            temp.remove(x)
            temp.append('top')
        for y in removeList:
            if y == x: temp.remove(x)

    temps= ''
    for x in temp:
        temps+= x + ' '
        if x == 'and' or x == temp[len(temp) - 1]:
            cipherList.append(temps)
            temps= ''

    executeList= commandHelper(cipherList)



    # If a relay is not specified and there is only one command, the command is executed for both relays.
    # If a relay is not specified and there are two commands, the commands are executed for r1 and r2 respectively.
    try:
        if 'r1' not in executeList[0] and 'r2' not in executeList[0]:
            k= len(executeList)
            for i in range(k):
                com= executeList[i]
                if k == 1:
                    executeList[0]= 'r3 ' + com
                    break
                executeList[i]= 'r{} '.format(str(i + 1)) + com

    except Exception: pass
    finally:
        com= ''
        for x in executeList:
            com+= x + ','

        return com

if __name__ == '__main__':
    a= input('Command?: ')
    print(cipher(a))
