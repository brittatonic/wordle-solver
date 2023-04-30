import z3
import time
import pandas as pd
import pdb

# Ignoring the DataFrame append warning
import warnings
warnings.filterwarnings("ignore")

# Define Constants
WORD_LEN = 5
LETTER_TO_INDEX = {letter: index for index, letter in enumerate("abcdefghijklmnopqrstuvwxyz")}
INDEX_TO_LETTER = {index: letter for letter, index in LETTER_TO_INDEX.items()}
NUM_GUESSES = 6

# Read in dictionary file and wordle answers
def loadDictionary():
    with open('simpleDictionary.txt') as file:
        dictionary = set(word.strip() for word in file.readlines())
    words = removeInvalidWords(dictionary)
    words = list(words)
    words = removePluralWords(words)

    with open('WordleAnswers.txt') as file:
        solution = set(word.strip().lower() for word in file.readlines())
    wordle = list(solution)
    return words, wordle

# Construct the variables
def defineLetterVariables():
    return [z3.Int(f"letter_{index}") for index in range(WORD_LEN)]

# Contrain variables to be within the alphabet
def defineAlphabetConstraints(solver, vars):
    for var in vars:
        solver.add(var >= 0, var <= 25)
    return solver

# Remove any word ending with an s
def removePluralWords(words):
    fiveLetterWords = list(filter(lambda word: len(word) == 5, words))
    fourLetterWords = set(filter(lambda word: len(word) == 4, words))
    fiveLetterWordsWithS = set(filter(lambda word: word[4] == "s", fiveLetterWords))
    goodFiveLetterWords = list(filter(lambda word: not (word in fiveLetterWordsWithS and word[:4] in fourLetterWords), fiveLetterWords))
    return goodFiveLetterWords

# Make sure solver only picks legal words
def addWordConstraints(solver, words, vars):
    disjunction = []

    for word in words:
        conjuntion = z3.And([vars[index] == LETTER_TO_INDEX[letter] for index, letter in enumerate(word)])
        disjunction.append(conjuntion)
    solver.add(z3.Or(disjunction))
    return solver

# Remove words that are not valid (bad characters, etc.)
def removeInvalidWords(words):
    validChars = set(LETTER_TO_INDEX.keys())

    def validCharsInWord(word):
        return set(word).issubset(validChars)
    return filter(validCharsInWord, words)

# Greyed box in a guess
def letterNotInSolution(solver, vars, letter):
    for var in vars:
        solver.add(var != LETTER_TO_INDEX[letter])
    return solver

def letterInWrongSpot(solver, vars, letter, position):
    solver.add(vars[position] != LETTER_TO_INDEX[letter])
    solver.add(z3.Or([var == LETTER_TO_INDEX[letter] for var in vars]))
    return solver

# If solver guesses a word with same letter more than once
def letterAppearsOnce(solver, vars, letter):
    uniqueDisjunction = []

    for var in vars:
        letterConjuntion = [var == LETTER_TO_INDEX[letter]]
        for otherVar in vars:
            if var == otherVar:
                continue
            letterConjuntion.append(otherVar != LETTER_TO_INDEX[letter])
        uniqueDisjunction.append(z3.And(letterConjuntion))

    solver.add(z3.Or(uniqueDisjunction))
    return solver

# Green box in a guess
def letterInCorrectSpot(solver, vars, letter, position):
    solver.add(vars[position] == LETTER_TO_INDEX[letter])
    return solver

def findAllIndexes(word, letter):
    return [ii for ii, ltr in enumerate(word) if ltr == letter]

# Print Z3 guessed solution
def printSolution(model, vars):
    word = []
    for var in vars:
        word.append(INDEX_TO_LETTER[model[var].as_long()])
    print('Guess: ', ''.join(word))
    return word

if __name__ == "__main__":
    words, solutions = loadDictionary()

    df = pd.DataFrame(columns=['Guesses', 'Time', 'Wordle', 'FinalWord', 'Matching', 'TotalTime'])

    # Timer
    startTime = time.time()

    solver = z3.Solver()
    for ii in range(len(solutions)):
        solver.reset()
        vars = defineLetterVariables()
        solver = defineAlphabetConstraints(solver, vars)
        solver = addWordConstraints(solver, words, vars)

        wordle = list(solutions[ii])
        print('-----',solutions[ii],'-----')
        letterRemoved = ''

        startGuessTime = time.time()
        for jj in range(NUM_GUESSES):
            result = solver.check()

            model = solver.model()
            guess = printSolution(model, vars)

            guessLetters = list(guess)

            common_letters = set(guessLetters) & set(wordle)

            for letters in guessLetters:
                if (letters not in common_letters):
                    checkIfRemoved = set(letterRemoved) & set(letters)
                    if (len(checkIfRemoved) == 0):
                        letterRemoved += letters

            for removed in letterRemoved:
                solver = letterNotInSolution(solver, vars, removed)

            for idx, letter in enumerate(guessLetters):
                if (letter in wordle):
                    wordleIdx = wordle.index(letter)
                    wordleIdxs = findAllIndexes(wordle, letter)
                    guessIdxs = findAllIndexes(guess, letter)
                    if (len(wordleIdxs) > 1):
                        checkWhichIndexs = set(wordleIdxs) & set(guessIdxs)
                        # pdb.set_trace()
                        if (len(checkWhichIndexs) == 0):
                            solver = letterInWrongSpot(solver, vars, letter, idx)
                        elif (len(checkWhichIndexs) > 1): 
                            for value in checkWhichIndexs:
                                solver = letterInCorrectSpot(solver, vars, letter, value)
                        elif (len(checkWhichIndexs) == 1):
                            goodIdx = checkWhichIndexs.pop()
                            for badIdx in guessIdxs:
                                if (badIdx != goodIdx):
                                    continue
                            solver = letterInCorrectSpot(solver, vars, letter, goodIdx)
                    elif (idx == wordleIdx):
                        solver = letterAppearsOnce(solver, vars, letter)
                        solver = letterInCorrectSpot(solver, vars, letter, idx)
                        continue
                    else:
                        solver = letterInWrongSpot(solver, vars, letter, idx)

            if (guess == wordle):
                endGuessTime = time.time()
                df = df.append({'Guesses': jj+1, 'Time': endGuessTime - startGuessTime, 'Wordle': solutions[ii], 'FinalWord': ''.join(guess), 'Matching': True}, ignore_index=True)
                break
            elif ((jj == NUM_GUESSES-1) & (guess != wordle)):
                endGuessTime = time.time()
                df = df.append({'Guesses': jj+1, 'Time': endGuessTime - startGuessTime, 'Wordle': solutions[ii], 'FinalWord': ''.join(guess), 'Matching': False}, ignore_index=True)

    endTime = time.time()
    print('Total time to guess all wordles was: ', endTime - startTime)
    df = df.append({'TotalTime': endTime - startTime}, ignore_index=True)

    df.to_csv('WordleSolver2.csv', index=None, mode='w')
