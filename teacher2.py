import tkinter as tk
import random
from dataclasses import dataclass
from itertools import product


@dataclass
class Data:
    frequency: float
    correct: float
    incorrect: float
    weight: float


class TextHandler:
    WORD_COUNT = 10
    delimeters = [',', ' ', '.', ';', '?', ':']
    delimeterWeights = [2, 20, 1, 0.1, 0.1, 0.1]

    def __init__(self):
        self.words = dict()
        self.letters = dict()
        self.wordsTyped = 0
        self.timeTaken = 0

    def setData(self,
                wordFilePath: str = 'words.csv',
                letterFilePath: str = 'n-grams.csv',
                weightTechnique: str = 'Words') -> None:
        with open(wordFilePath, 'r') as f:
            for line_n, line in enumerate(f):
                if line_n == 0:
                    continue
                if line_n == 1:
                    self.wordsTyped, self.timeTaken = line.strip().split(',')
                    continue
                w, f, c, i = line.strip().split(',')
                self.words[w] = Data(float(f), float(c), float(i), 0.0)

        with open(letterFilePath, 'r') as f:
            for line_n, line in enumerate(f):
                if line_n == 0:
                    continue
                ch, f, c, i = line.strip().split(',')
                self.letters[ch] = Data(float(f), float(c), float(i), 0.0)

        if weightTechnique == 'Words':
            for data in self.words.values():
                if data.correct == data.incorrect == 0.0:
                    data.weight = data.frequency
                elif data.correct > 0 and data.incorrect == 0:
                    data.weight = data.frequency / data.correct
                elif data.correct == 0 and data.incorrect > 0:
                    data.weight = data.frequency * data.incorrect
                else:
                    data.weight = data.frequency * data.incorrect / data.correct
        else:
            for data in self.letters.values():
                if data.correct == data.incorrect == 0.0:
                    data.weight = data.frequency
                elif data.correct > 0 and data.incorrect == 0:
                    data.weight = data.frequency / data.correct
                elif data.correct == 0 and data.incorrect > 0:
                    data.weight = data.frequency * data.incorrect
                else:
                    data.weight = data.frequency * data.incorrect / data.correct

            for word, data in self.words.items():
                keys = list(word) + [''.join(t) for t in product(word, word)]
                weight = 0.0
                countSum = 0
                for key in keys:
                    count = word.count(key)
                    weight += count * self.letters[key].weight
                    countSum += count
                data.weight = weight / countSum

    def text(self) -> str:
        chosenWords = random.choices(self.words.keys(),
                                     weights=[data.weight for data in self.words.values()],
                                     k=TextHandler.WORD_COUNT)
        textStr = ''
        for i, word in enumerate(chosenWords):
            delimiter = random.choices(
                TextHandler.delimeters, weights=TextHandler.delimeterWeights, k=1)[0]
            if i != len(chosenWords) - 1:
                textStr += word + delimiter
            else:
                textStr += word + '.'
        return textStr

    def writeData(self,
                  wordFilePath: str = 'words.csv',
                  letterFilePath: str = 'n-grams.csv') -> None:
        sortedWords = sorted(self.words.keys())
        with open(wordFilePath, 'r') as f:
            f.write('word,frequency,correct,incorrect\n')
            f.write(self.wordsTyped + ',' + self.timeTaken + '\n')
            for word in sortedWords:
                data = self.words[word]
                f = str(data.frequency)
                c = str(data.correct)
                i = str(data.incorrect)
                f.write(word + ',' + f + ',' + c + ',' + i + '\n')
        sortedLetters = sorted(self.letters.keys())
        with open(letterFilePath, mode='r') as f:
            f.write('letter,frequency,correct,incorrect\n')
            for letter in sortedLetters:
                data = self.letters[letter]
                f = str(data.frequency)
                c = str(data.correct)
                i = str(data.incorrect)
                f.write(word + ',' + f + ',' + c + ',' + i + '\n')


class GUI:
    def __init__(self):
        self.root = tk.Tk()
