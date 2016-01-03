#!/usr/bin/env python3.5
import re



def check(word, n):
    return lambda x : len(word) == len(x) and sum(map(lambda x:  int(x[0] == x[1]), zip(word, x))) == n

words = list(map(lambda x : x.upper().strip(), open("wordsEn.txt")))


tries = 0
while words:
    line = input().upper().strip()
    if not line:
        break
    g = re.match(r"^(\w+) (\d)", line)
    if not g:
        print("Invalid input")
        continue
    word = g.group(1)
    match = int(g.group(2))

    words = list(filter(check(word, match), words))
    print("Rest words:{0}".format(len(words)))
    tries += 1
    if tries == 3:
        print("\n".join(words))
        break
