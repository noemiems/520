import re
IN = open("text.txt")
line = "XXX"
list = []
sentencelist = []
exceptions = ['Mr.', 'Mrs.', 'e.g', 'i.e', '.com']

while line:
    line = IN.readline()
    line.strip()
    list.append(line)

for x in range(len(list)):
    paragraph = list[x]
    sentence = re.split('\.|!|\?|;|(?<!\[\s])[,](?![\s])', paragraph)
    sentencelist.append(sentence)

for y in range(len(sentencelist)):
    for z in sentencelist[y]:
        print(z, '\n')
