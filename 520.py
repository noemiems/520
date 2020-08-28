import re
IN = open("text.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []

while line:
    line = IN.readline()
    line.strip()
    text.append(line)

for x in range(len(text)):
    grouptext = text[x]
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)((?<=[.?!])|(?<=\."))(\s|[A-Z].*)', grouptext)
    sentencelist.append(sentences)

for paragraph in range(len(sentencelist)):
    for sentence in sentencelist[paragraph]:
        OUT.write(sentence)
        OUT.write('\n')
        OUT.write('\n')
        OUT.write('\n')

OUT.close()
IN.close()
