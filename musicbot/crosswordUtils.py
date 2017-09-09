import threading


#Replaces all letters in a crossword with ?
def unsolveCrossword(crossword):
    ret = ""
    for char in crossword:
        if char.isalpha():
            ret += "?"
        else:
            ret += char
    return ret

#create a formatted output that can be easily read in discord chat
#also forces crossword to code format for uniform text width
#TODO may need to add extra data to output later
def formatCrosswordOutput(crossword, letters):
    return "Letters: " + letters + "\n`" + crossword + "`"

#runs a crossword game and manages everything except for stepping through the game
class crosswordGameManager:
    def __init__(self, jsonCrossword):
        self.letters = jsonCrossword["letters"] #available letters
        self.crosswordSolution = jsonCrossword["crossword"] #fully solved crossword
        self.crossword = unsolveCrossword(self.crosswordSolution) #current players solution
        self.scoredWords = jsonCrossword["scores"] #all available words and scores
        self.foundWords = [] #words that have been found so far
        self.crosswordWords = jsonCrossword["crosswordWords"] #words that are in the crossword
        self.players = [] #list of tuples with (score, player) that can be sorted

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
                print("AND HERE")
                self.revealWord(guess)
                self.crosswordWords.remove(guess)
            #check if crossword is complete
            if len(self.crosswordWords) == 0:
                return 1
            return 0
        return -1

    #modifies self.crossword to add in the found word
    #wtf why did i decide to write this
    def revealWord(self, word):
        print("Revealing word: " + word)
        #check each square for first letter of word
        for y in range(0,len(self.crosswordSolution)):
            print("Y:"+y)
            for x in range(0,len(self.crosswordSolution)[y]):
                print("X:"+x)
                if word[0] == self.crosswordSolution[y][x]:
                    #Horizontal
                    tempcrossword = self.crossword
                    for i in range(1, len(word)):
                        if word[i] != self.crosswordSolution[y][x+(i*2)]:
                            break
                        tempcrossword[y] = self.replaceStringChar(tempcrossword[y], x+(i*2), word[i])
                        if i == len(word)-1: #last char of word - word found
                            self.crossword = tempcrossword
                            print("CROSSWORD IS " + str(self.crossword))
                            return
                    #Vertical
                    tempcrossword = self.crossword
                    for i in range(1, len(word)):
                        if word[i] != self.crosswordSolution[y+i][x]:
                            break
                        tempcrossword[y+i] = self.replaceStringChar(tempcrossword[y+i], x, word[i])
                        if i == len(word)-1: #last char of word - word found
                            self.crossword = tempcrossword
                            print("CROSSWORD IS " + str(self.crossword))
                            return
        print("Word not in crossword, should not be here")

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