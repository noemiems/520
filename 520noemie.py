import re
IN = open("input.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []
finallist = []

def changingdots( str ):
    return str.replace('.', '|')
def changingpipes( str ):
    return str.replace('|', '.')

while line:
    line = IN.readline()
    line.strip()
    line = re.sub('<[^>]*>', "\n", line)
    text.append(line)

for x in range(len(text)):
    grouptext = text[x]
    grouptext = re.sub(r"(?:[A-Z]\.)+", lambda m: changingdots(m.group()), grouptext)
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
        sentence = re.sub(r"(?:[A-Z]\|)+", lambda m: changingpipes(m.group()), sentence)
        OUT.write(sentence)
        OUT.write('\n')


OUT.close()
IN.close()
