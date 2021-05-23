import tkinter as tk
from playsound import playsound
import random
from dataclasses import dataclass
import time


WORD_COUNT = int(input("How many words do you want to try?"))
root = tk.Tk()
# root.geometry('1000x1000')
keyPressPath = r'E:\Mimisbrunnr\Valhalla\Python Projects\TouchTyping\keyPress.wav'
errSoundPath = r'E:\Mimisbrunnr\Valhalla\Python Projects\TouchTyping\error-2.wav'
wordsPath = r'E:\Mimisbrunnr\Valhalla\Python Projects\TouchTyping\words.csv'


@dataclass
class Word:
    index: float
    word: str
    frequency: str
    correct: float
    incorrect: float


words = []
with open(wordsPath, 'r') as f:
    for ind, line in enumerate(f):
        if ind == 0:
            continue
        if ind == 1:
            wordsTyped, timeTaken = list(map(float, line.strip().split(',')))
            continue
        w, f, c, i = line.strip().split(',')
        words.append(Word(ind, w, float(f), float(c), float(i)))
n = len(words)
wt = []
for element in words:
    if element.correct == element.incorrect == 0:
        wt.append(element.frequency)
    elif element.correct > 0 and element.incorrect == 0:
        wt.append(element.frequency / element.correct)
    elif element.correct == 0 and element.incorrect > 0:
        wt.append(element.frequency * element.incorrect)
    else:
        wt.append(element.frequency * element.incorrect / element.correct)

delim_list = [',', ' ', '.', ';', '?']
delim_weight = [2, 20, 1, 0.1, 0.1]


def press(event):
    global textStr, root, ind, w, mistakes
    if ind < len(textStr) and event.char == textStr[ind]:
        playsound(keyPressPath)

        ind += 1
        w.tag_delete('curr')
        w.tag_delete('after')
        w.tag_add("curr", '1.' + str(ind - 1), '1.' + str(ind))
        w.tag_add('after', '1.' + str(ind), '1.' + str(ind + 1))
        w.tag_config('curr', background='green')
        ind -= 1

        if event.char in delim_list:
            c = textStr[ind - 1]
            j = ind - 2
            while c not in delim_list and j >= 0:
                c = textStr[j]
                j -= 1
            if j != -1:
                curr_word = textStr[j + 2: ind]
            else:
                curr_word = textStr[j + 1: ind]
            for element in words:
                if element.word == curr_word:
                    if mistakes == 0:
                        element.correct += 1
                    else:
                        element.incorrect += mistakes / len(curr_word)
                    break
            mistakes = 0
        ind += 1
    else:
        w.tag_config('curr', background='white')
        w.tag_config('after', background='red')
        playsound(errSoundPath)
        mistakes += 1
        if event.char in delim_list:
            c = textStr[ind - 1]
            j = ind - 2
            while c not in delim_list and j >= 0:
                c = textStr[j]
                j -= 1
            if j != -1:
                curr_word = textStr[j + 2: ind]
            else:
                curr_word = textStr[j + 1: ind]
            for element in words:
                if element.word == curr_word:
                    if mistakes == 0:
                        element.correct += 1
                    else:
                        element.incorrect += mistakes / len(curr_word)
                    break
            mistakes = 0


root.bind('<Key>', press)

chosenWords = random.choices([element.word for element in words], weights=wt, k=WORD_COUNT)
textStr = ''
for i, word in enumerate(chosenWords):
    delimiter = random.choices(delim_list, weights=delim_weight, k=1)[0]
    if i != len(chosenWords) - 1:
        textStr += word + delimiter
    else:
        textStr += word + '.'
w = tk.Text(root, height=5, width=800, font=('Times New Roman', 30))
w.tag_add("curr", "1.0", "1.0")
w.tag_add('after', "1.0", "1.0")
w.pack()
w.insert(tk.INSERT, textStr)
ind = 0
mistakes = 0

startTime = time.time()
root.mainloop()
timeTaken += time.time() - startTime - 1
wordsTyped += WORD_COUNT

with open(wordsPath, 'w') as f:
    f.write('word,frequency,correct,incorrect\n')
    f.write(str(wordsTyped) + ',' + str(timeTaken) + '\n')
    for element in words:
        f.write(element.word + ',' + str(element.frequency) + ',' + str(element.correct) + ',' + str(element.incorrect) + '\n')

print('current typing speed =', wordsTyped * 60 / timeTaken, 'words per minute')
