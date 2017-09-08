
#Replaces all letters in a crossword with ?
def unsolveCrossword(crossword):
    ret = ""
    for char in crossword:
        if char.isalpha():
            ret += "?"
        else:
            ret += char
    return ret