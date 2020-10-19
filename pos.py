IN = open("corpus-brown.txt")
import re
line = 'XXX'
text = []
sentence = []
wordlist = []
taglist = []

while line:
    line = IN.readline()
    line.strip()
    text.append(line)
for x in range(len(text)):
    pattern = re.findall('[A-Z]?[a-z]+/[A-Z]+', text[x])
    sentence.append(pattern)
    for y in range(len(sentence)):
        for z in range(len(sentence[y])):
            string = sentence[y][z].split('/')
            wordlist.append(string[0])
            taglist.append(string[1])
