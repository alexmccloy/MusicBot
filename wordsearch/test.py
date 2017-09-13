#modifies self.crossword to add in the found word
#wtf why did i decide to write this
def revealWord(self, word):
    print("LEN IS " + len(self.crosswordSolution), flush=True)
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


if __name__ == '__main__':
    f = open("current.json", 'r')
    puzzleJson = json.loads(f.readlines()[0])
    crossword = puzzleJson["crossword"]