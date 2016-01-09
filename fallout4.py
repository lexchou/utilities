#!/usr/bin/env python3.5
import re



def similiarity(a, b):
    return sum(map(lambda x:  int(x[0] == x[1]), zip(a, b)))

def check(word, n):
    return lambda x : len(word) == len(x) and similiarity(word, x) == n

def read_candidates():
    ret = []
    print("Type fallout 4 terminal candidate passwords, empty line to end:");
#return ["PASS", "DOWN", "BARE", "SHOW", "RATE", "PROP", "THUS", "BODY", "GOES", "LOSE", "FORM", "SOME"]
    while True:
        line = input().upper().strip()
        if line:
            ret.append(line)
        else:
            break
    return ret



words = read_candidates()# list(map(lambda x : x.upper().strip(), open("wordsEn.txt")))

word_len = len(words[0])
candidates = []
for word in words:
    scores = list(map(lambda x:0 if x == word else similiarity(x, word), words))
    total_score = sum(scores)
    candidates.append((total_score, word))
words=(list(map(lambda x:x[1], sorted(candidates, key = lambda x:x[0], reverse = True))))
print("|" + "|".join(["*" * word_len] + words) + "|")
for word in words:
    scores = list(map(lambda x:0 if x == word else similiarity(x, word), words))
    scores = map(lambda x: str(x) if x else "", scores)
    scores = map(lambda x:" " * (word_len - len(x)) + x, scores)
    print("|{0}|".format("|".join([word] + list(scores))))









tries = 0
while words:
    line = input().upper().strip()
    if not line:
        break
    if tries < 3:
        g = re.match(r"^(\w+) (\d)", line)
        if not g:
            print("Invalid input")
            continue
        word = g.group(1)
        match = int(g.group(2))

        words = list(filter(check(word, match), words))
        print("{0} Rest words:{1}".format(len(words), "/".join(words)))
        tries += 1
        if tries == 3:
            print("\n".join(words))
    else:
         if line in words:
             print("Correct password!")
         else:
             print("Incorrect password!")
