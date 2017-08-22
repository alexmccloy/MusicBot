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

def generatePuzzle(letterCount):
    pass
    #import list of words and group into arrays by word length
    wordList = importWordList

    #choose a word with letterCount letters from list

    #check every word in list with <=letterCount letters and see if that word can be made with letterGroup

    #generate a score against each word based on lettercount and word frequency

    #put 10? of the words into a crossword (if there are less than 10 reroll?)

    #format and write to text file

#Returns a 2d array, an array for each word length containing all those words
def importWordList():
    wordArray = createWordArray(50)
    with open("wordList.txt", 'r') as f:
        text = f.readlines()

def createWordArray(maxLevel):
    ret = []
    for i in range(0,maxLevel-1):
        ret.append([])
    return ret




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--createPuzzle", "-c", nargs=2, type=int, help="Create a puzzle with X letters, Y times")
    parser.add_argument("-g", "--getPuzzle", action="store_true", help="rotates a new puzzle")
    parser.add_argument("-d", "--debug", action="store_true", help="extra debugging text")
    global args = parser.parse_args()

    if args.debug:
        print("debug mode on")

    if args.getPuzzle:
        print("Rotating puzzle")
        rotate_puzzle()

    if args.createPuzzle:
        for i in range(0,args.createPuzzle[1]):
            print("Creating puzzle number " + i + " with " + args.createPuzzle[0] + " letters.")
            generatePuzzle(args.createPuzzle[0])
