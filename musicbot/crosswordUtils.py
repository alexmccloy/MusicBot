import threading


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

#converts list to printable string
def l2s(l):
    s = ""
    for x in l:
        s += str(x)
        s += '\n'
    return s

#create a formatted output that can be easily read in discord chat
#also forces crossword to code format for uniform text width
#TODO may need to add extra data to output later
def formatCrosswordOutput(crossword, letters):
    return "Letters: " + letters + "\n" + l2s(crossword) + "\n"

#runs a crossword game and manages everything except for stepping through the game
class crosswordGameManager:
    def __init__(self, jsonCrossword):
        self.letters = jsonCrossword["letters"] #available letters
        self.crosswordSolution = jsonCrossword["crossword"].split('\n') #fully solved crossword
        self.crosswordSolution.remove('')
        self.crossword = unsolveCrossword(self.crosswordSolution) #current players solution
        self.scoredWords = jsonCrossword["scores"] #all available words and scores
        self.foundWords = [] #words that have been found so far
        self.crosswordWords = jsonCrossword["crosswordWords"] #words that are in the crossword
        self.players = [] #list of tuples with (score, player) that can be sorted

        print(self.crossword)
        print(self.crosswordSolution)

    #returns -1 if guess is wrong, 0 if word found, and 1 if crossword complete
    #internally updates variables and checks a players guess / adds scores
    #TODO may want to add extra return val for crosswordWord found to reprint crossword immediately
    def checkGuess(self, guess, player):
        print(guess)
        print(player)
        print("------------------")
        print("crossword words " + str(self.crosswordWords))
        print("scored words " + str(self.scoredWords))
        print("found words " + str(self.foundWords))
        if (guess in (item[1] for item in self.scoredWords)) and (guess not in self.foundWords):
            print("GOT HERE")
            self.updateScores((self.getWordScore(guess), player))
            self.foundWords.append(guess)
            if guess in self.crosswordWords:
                print("GUESS IS" + guess)
                crossword = rasdsaevealWord(guess, crosswordSolution, crossword)
                print(l2s(crossword))
                self.crosswordWords.remove(guess)
            #check if crossword is complete
            if len(self.crosswordWords) == 0:
                return 1
            return 0
        return -1

    #returns modified unsolved crossword with the given word revealed
    def revealWord(word, solved, unsolved):
        print("REVEALWORD: " + word + " " + solved + " " + unsolved)
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
    #if crossword is None transposes col
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

    #replace char in string s at index with char c
    def replaceStringChar(self, s, index, c):
        return s[:index] + c + s[index+1:]

    def updateScores(self, newScore): #(score,playerName)
        for i in range(0,len(self.players)):
            if self.players[i][1] == newScore[1]: #player already in list
                self.players[i] = (self.players[i][0] + newScore[0], self.players[i][1])
            else:
                self.players.append(newScore)

    def getWordScore(self, word):
        for w in self.scoredWords:
            if word == w[1]:
                return w[0]
        return 0

#crosswordGame should be instance of crosswordGameManager
class crosswordChecker (threading.Thread):
    def __init__(self, threadID, name, messageQueue, crosswordGame, keepAlive):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.messageQueue = messageQueue
        self.crosswordGame = crosswordGame
        self._return = None
        self.keepAlive = keepAlive
        
    def run(self):
        while True:
            if self.keepAlive.value:
                #take a message off the queue and check it, only exit if it scored points
                try:
                    guess = self.messageQueue.get(True, 1) #(player, message)
                    complete = self.crosswordGame.checkGuess(guess[1], guess[0])
                    if complete == 1:
                        self._return = self.crosswordGame.players
                        break
                except:
                    pass
            else:
                print("gonna try to kill myself now")
                break

    def join(self, timeout):
        #return tuple (name, score) if someone guessed right
        threading.Thread.join(self, timeout)
        return self._return