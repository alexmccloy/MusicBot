#possible arguments -
#   generatePuzzle -  x y --generates y new puzzles each using x letters
#       will place each puzzle in its own text file
#
#   --getPuzzle ---gets the next puzzle in the new puzzle folder and puts it in the wordsearch directory with the name
#       current.txt. Moves the current puzzle into the used folder. If there are no puzzles left will generate a new one

import argparse

def rotate_puzzle():



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("letterCount", type=int, help="How many letters each puzzle should have")
    parser.add_argument("puzzleCount", type=int, help="How many puzzles to generate")
    parser.add_argument("--getPuzzle", "-g", action="store_true", help="rotates a new puzzle")
    
