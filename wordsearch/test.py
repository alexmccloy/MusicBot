import json
import os

#modifies self.crossword to add in the found word
#wtf why did i decide to write this
def revealWord(word, solved, unsolved):
    print("LEN IS " + str(len(solved)))
    #check each square for first letter of word
    for y in range(0,len(solved)):
        print("Y:"+str(y))
        for x in range(0,len(solved[y])):
            print("X:"+str(x))
            if word[0] == solved[y][x]:
                #Horizontal
                tempcrossword = unsolved
                for i in range(1, len(word)):
                    print("i:" +str(i)+",x:"+str(x))
                    print(solved[2])
                    if word[i] != solved[y][x+(i*2)]:
                        break
                    tempcrossword[y] = replaceStringChar(tempcrossword[y], x+(i*2), word[i])
                    if i == len(word)-1: #last char of word - word found
                        unsolved = tempcrossword
                        print("h - CROSSWORD IS " + l2s(unsolved))
                        return unsolved
                #Vertical
                tempcrossword = unsolved
                for i in range(1, len(word)):
                    if word[i] != solved[y+i][x]:
                        break
                    tempcrossword[y+i] = replaceStringChar(tempcrossword[y+i], x, word[i])
                    if i == len(word)-1: #last char of word - word found
                        unsolved = tempcrossword
                        print("v - CROSSWORD IS " + l2s(unsolved))
                        return unsolved
    print("Word not in crossword, should not be here")

#assume word is in crossword
def revealWord2(word, solved, unsolved):
    #check horizontal
    temp = []
    found = False
    for i in range(0,len(solved)):
        line =  wordInLine(word, getRow(i, solved), getRow(i, unsolved), True)
        if line == None:
            temp.append(getRow(i, unsolved))
        else:
            temp.append(line)
            found = True
    if found:
        return temp

    #check vertical
    temp = None
    for i in range(0,len(solved[0])):
        line =  wordInLine(word, getCol(i, solved), getCol(i, unsolved), False)
        if line == None:
            temp = addCol(getCol(i, unsolved), temp)
        else:
            temp = addCol(line, temp)
            found = True
    if found:
        return temp
    print("Should not have got here")

#returns row x of crossword
def getRow(row, crossword):
    return crossword[row]

def getCol(col, crossword):
    ret = ""
    for row in crossword:
        ret += row[col]
    return ret

#adds a column to the right hand side of a 2d array
#if crossowrd is None transposes col
#TODO: currently assumes sizes are correct
def addCol(col, crossword):
    if crossword == None:
        ret = []
        for x in col:
            ret.append(x)
        return ret

    for i in range(0,len(crossword)):
        crossword[i] = crossword[i] + col[i]
    return crossword

#returns the updated line with word in it if matching, None otherwise.
#Assumed 1D arrays only
def wordInLine(word, solved, unsolved, horizontal):
    for i in range(0,len(solved)):
        temp = unsolved
        found = True
        if horizontal:
            factor = 2
        else:
            factor = 1
        #check if word too long to fit on rest of line
        if len(solved)+1 < i+len(word)*factor:
            continue
        for j in range(0,len(word)):
            if solved[i+j*factor] == word[j]:
                temp = replaceStringChar(temp, i+j*factor, word[j])
            else:
                found = False
                break
        #check that either at end of line or next char is -
        if found:
            if i+len(word)*factor >= len(solved) or solved[i+len(word)*factor] == '-':
                return temp
    return None

#Replaces all letters in a crossword with ?
def unsolveCrossword(crossword):
    ret = []
    for line in crossword:
        l = ""
        for char in line:
            if char.isalpha():
                l += "?"
            else:
                l += char
        ret.append(l)
    return ret


#replace char in string s at index with char c
def replaceStringChar(s, index, c):
    return s[:index] + c + s[index+1:]

def l2s(l):
    s = ""
    for x in l:
        s += str(x)
        s += '\n'
    return s
    


if __name__ == '__main__':
    print(os.getcwd())
    f = open("test.json", 'r')
    puzzleJson = json.loads(f.readlines()[0])
    crosswordSolved = puzzleJson["crossword"].split('\n')
    crosswordSolved.remove('')
    crossword = unsolveCrossword(crosswordSolved)

    print("Crossword solved: \n" + l2s(crosswordSolved))
    print("Crossword current:\n" + l2s(crossword))
    crossword = revealWord2("buying", crosswordSolved, crossword)
    crossword = revealWord2("big", crosswordSolved, crossword)
    crossword = revealWord2("bung", crosswordSolved, crossword)
    print("Crossword current:\n" + l2s(crossword))

    '''a='? ? ? ? - ? ? ?'
    b='b u n g - b u y'
    print(wordInLine('buy',b,a))'''