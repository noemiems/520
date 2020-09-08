import re
IN = open("abstracts.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []
finallist = []

while line:
    line = IN.readline()
    line.strip()
    line = re.sub('<[^>]*>', "\n", line)
    text.append(line)

for x in range(len(text)):
    grouptext = text[x]
    sentences = re.split('(?<=[A-Z]\.[A-Z]\.)(\s)', grouptext)
    for y in range(len(sentences)):
        sentencesb = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.\s)(?<!p\.)((?<=[.?!])|(?<=\.")|(?<=]\.))(\s+|[A-Z].*)', sentences[y])
        sentencelist.append(sentencesb)

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
IN.close()
