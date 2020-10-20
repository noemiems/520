IN = open("shortcorpus.txt")
import re
line = 'XXX'
text = []
ssdict = {}
dict = {}
firstword = []
sentence = []
tagslist = []
splitsentence = []

while line:
    line = IN.readline()
    line.strip()
    text.append(line)
for x in range(len(text)):
    pattern = re.split('\s', text[x])
    sentence.append(pattern)
for x in range(len(sentence)):
    firststring = sentence[x][0].split('/')
    if len(firststring) == 2:
        firstword.append(firststring[1])
for word in firstword:
    if word not in ssdict:
        ssdict[word] = 1
    else:
        ssdict[word] += 1
for item in ssdict:
    probfirst = ssdict[item]/len(firstword)
    print('Probability that', item, 'starts a sentence:', probfirst)
for x in range(len(sentence)):
    for item in sentence[x]:
        splititem = item.split('/')
        splitsentence.append(splititem)
for lists in range(len(splitsentence)):
    if len(splitsentence[lists]) == 2:
        tagslist.append(splitsentence[lists][1])

for tag in range(1,len(tagslist)):
    pair = tagslist[tag-1] + tagslist[tag]
    if pair not in dict:
        dict[pair] = 1
    else:
        dict[pair] += 1

print(dict)
