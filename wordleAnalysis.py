import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_table('WordleSolver2.csv', sep=',')

plt.figure()
plt.hist(data['Guesses'], bins=[2,3,4,5,6,7], range=[2,7], align='left', color='pink', edgecolor='black')
plt.xticks(range(2,7))
plt.xlabel('Number of Guesses')
plt.ylabel('Occurences')
plt.title('Guesses For All Wordle Solutions')

solved = data[data['Matching'] == True]
print(len(data) - len(solved))
plt.figure()
plt.hist(solved['Guesses'], bins=[2,3,4,5,6,7], range=[2,7], align='left', color='purple', edgecolor='black')
plt.xticks(range(2,7))
plt.xlabel('Number of Guesses')
plt.ylabel('Occurences')
plt.title('Guesses For Solved Wordle Solutions')

plt.figure()
plt.hist(data['Matching'], bins=[0,1,2], range=[0,1,2], align='left', color='blue', edgecolor='black')
plt.xticks(range(0,2), ['False', 'True'])
plt.xlabel('Guessed the Correct Word')
plt.ylabel('Occurences')
plt.title('Guesses Matching Solution')

time = data['Time']
time.drop(time.tail(1).index, inplace=True)
totalTimeGuessing = sum(time)
print('Total Time Guessing: ', totalTimeGuessing)
totalTime = data['TotalTime'].iloc[-1]
print('Total Time Running Program: ', totalTime)
averageTimePerSolve = totalTime/len(data)
print('Average Time per Solve: ', averageTimePerSolve)

sixGuesses = data[data['Guesses'] == 6]
fiveGuesses = data[data['Guesses'] == 5]
fourGuesses = data[data['Guesses'] == 4]
threeGuesses = data[data['Guesses'] == 3]
twoGuesses = data[data['Guesses'] == 2]

sixGuessesAvarageTime = sum(sixGuesses['Time'])/len(sixGuesses)
fiveGuessesAvarageTime = sum(fiveGuesses['Time'])/len(fiveGuesses)
fourGuessesAvarageTime = sum(fourGuesses['Time'])/len(fourGuesses)
threeGuessesAvarageTime = sum(threeGuesses['Time'])/len(threeGuesses)
twoGuessesAvarageTime = sum(twoGuesses['Time'])/len(twoGuesses)

x = [twoGuessesAvarageTime, threeGuessesAvarageTime, fourGuessesAvarageTime, fiveGuessesAvarageTime, sixGuessesAvarageTime]
y = range(2,7)

plt.figure()
plt.scatter(data['Time'], data['Guesses'])
plt.scatter(x, y, marker='*', s=150, label='Average Time for Number Guesses')
plt.legend()
plt.grid(color='lightgray', linestyle=':')
plt.yticks(range(2,7))
plt.xlabel('Time [sec]')
plt.ylabel('Number of Guesses')
plt.title('Number of Guesses vs. Time')
plt.show()

