#possible arguments -
#   generatePuzzle -  x y --generates y new puzzles each using x letters
#       will place each puzzle in its own text file
#
#   --getPuzzle ---gets the next puzzle in the new puzzle folder and puts it in the wordsearch directory with the name
#       current.txt. Moves the current puzzle into the used folder. If there are no puzzles left will generate a new one

import argparse
import glob
from random import randint
import os
from datetime import datetime

DEFAULT_LETTERS = 6
CURRENT_PUZZLE_NAME = "current.txt"

def rotate_puzzle():
    files = getFilesInNewDir()
    if len(files) == 0:
        generatePuzzle(DEFAULT_LETTERS)
        files = getFilesInNewDir()

    #move current to used
    os.rename(CURRENT_PUZZLE_NAME, "new/"+str(datetime.now()))

    #pick random new and move to current
    os.rename(files[randint(0,len(files-1))], CURRENT_PUZZLE_NAME)

def getFilesInNewDir():
    files = []
    for file in glob.glob("new/*.txt"):
        if args.debug: #may have problems if this needs to be declared global
            print(file)
        files.append(file)
    return files

def generatePuzzle(letterCount):
    #import list of words and group into arrays by word length
    wordList = importWordList()
    matchingWords = []

    #choose a word with letterCount letters from list
    print("lettercount is " + str(letterCount))
    print(wordList[letterCount])
    chosenWord = wordList[letterCount][randint(0,len(wordList[letterCount]))]

    #check every word in list with <=letterCount letters and see if that word can be made with letterGroup
    while letterCount >= 3:
        for word in wordList[letterCount]:
            if checkLettersInWord(chosenWord, word):
                matchingWords.append(word)

        letterCount = letterCount - 1
        

    #generate a score against each word based on lettercount and word frequency
    scoredWords = assignWordScores(matchingWords)

    #put 10? of the words into a crossword (TODO: if there are less than 10 reroll?)
    #pick 9 words + chosenWord, square random number to bias higher scored words
    crosswordWords = [chosenWord]
    for i in range(0, randint(5,9)):
        continue

    for w in scoredWords:
        print(w)

    #format and write to text file

#returns true if word can be made by letters
def checkLettersInWord(letters, word):
    for l in word:
        if l not in letters:
            return False
    return True


#Returns a 2d array, an array for each word length containing all those words
def importWordList():
    wordArray = createWordArray(50)
    with open("wordList.txt", 'r') as f:
        for line in f:
            #append to correct level of array
            l = line.strip()
            wordArray[len(l)].append(l)
    return sorted(wordArray)

#returns a list of pairs (score, word)
#score is from 1-20 based on how common word is (20=best=less common. also factor in word length)
#15 points for rarity, 5 for word length (7 letter word = maximum points)
def assignWordScores(matchingWords):
    scoredWordsAll = []
    scoredWordsMatching = []
    with open("wordFreq.txt") as f:
        for line in f:
            l = line.split(" ") #format WORD1 WORD2 TYPE FREQ
            #need to do both words in each row
            scoredWordsAll.append((calculateWordScore(l[0],l[3]), l[0]))
            scoredWordsAll.append((calculateWordScore(l[1],l[3]), l[0]))

    #check against matchingWords
    for i in matchingWords: #string
        for j in scoredWordsAll: # (score, word)
            if i == j[1]:
                scoredWordsMatching.append(j)

    return scoredWordsMatching

#max word freq =~ 1100000
#score = 15-freq/78571 + max(7,len(word))-2
def calculateWordScore(word, freq):
    score = 0
    score += 15 - (freq / 78571)
    if len(word) > 7:
        score += 5
    else:
        score += len(word) - 2
    return score



def createWordArray(maxLevel):
    ret = []
    for i in range(0,maxLevel-1):
        ret.append([])
    return ret



if str(__name__) == "__main__":
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--createPuzzle", "-c", nargs=2, type=int, help="Create a puzzle with X letters, Y times")
    parser.add_argument("-g", "--getPuzzle", action="store_true", help="rotates a new puzzle")
    parser.add_argument("-d", "--debug", action="store_true", help="extra debugging text")
    args = parser.parse_args()

    if args.debug:
        print("debug mode on")

    if args.getPuzzle:
        print("Rotating puzzle")
        rotate_puzzle()

    if args.createPuzzle:
        for i in range(0,args.createPuzzle[1]): #number of puzzles to make
            print("Creating puzzle number " + str(i) + " with " + str(args.createPuzzle[0]) + " letters.")
            generatePuzzle(args.createPuzzle[0]) #number of letters in puzzles
