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

DEFAULT_LETTERS = 6

def rotate_puzzle():
    files = []
    for file in glob.glob("new/*.txt"):
        if debug:
            print(file)
        files.append(file)

    if len(files) == 0:
        generatePuzzle(DEFAULT_LETTERS)
        rotate_puzzle()
        return

    #move current to used

    #pick random new and move to current

def generatePuzzle(letterCount):
    pass
    #import list of words and group into arrays by word length

    #choose a word with letterCount letters from list

    #check every word in list with <=letterCount letters and see if that word can be made with letterGroup

    #generate a score against each word based on lettercount and word frequency

    #put 10? of the words into a crossword (if there are less than 10 reroll?)

    #format and write to text file



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("letterCount", type=int, help="How many letters each puzzle should have")
    parser.add_argument("puzzleCount", type=int, help="How many puzzles to generate")
    parser.add_argument("--getPuzzle", "-g", action="store_true", help="rotates a new puzzle")
    parser.add_argument("--debug", "-d", action="store_true", help="extra debugging text")
    args = parser.parse_args()

    if args.getPuzzle:
        print("Rotating puzzle")
        rotate_puzzle()
        break

    for (i in range(0,puzzleCount)):
        continue
