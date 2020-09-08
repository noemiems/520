import re
IN = open("input.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []
finallist = []

while line:
    line = IN.readline()
    line.strip()
    text.append(line)

for x in range(len(text)):
    grouptext = text[x]
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.\s)(?<!p\.)((?<=[.?!])|(?<=\.")|(?<=]\.))(\s+|[A-Z].*)', grouptext)
    sentencelist.append(sentences)

for x in range(len(sentencelist)):
    for y in range(len(sentencelist[x])):
        text = sentencelist[x][y]
        final = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.\s)(?<!p\.)((?<=[.?!])|(?<=\.")|(?<=]\.))(\s+|[A-Z].*)', text)
        finallist.append(final)
        
for paragraph in range(len(finallist)):
    for sentence in finallist[paragraph]:
        OUT.write(sentence)
        OUT.write('\n')


OUT.close()
