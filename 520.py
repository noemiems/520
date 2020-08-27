import re
IN = open("text.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []
exceptions = ['Mr.', 'Mrs.', 'e.g', 'i.e', '.com', 'Dr.', 'Fig.', 'Ms.']

while line:
    line = IN.readline()
    line.strip()
    text.append(line)

for x in range(len(text)):
    grouptext = text[x]
    sentences = re.split('((?<=[.!?]\s)|(?<=[.!?]\")) +(?=[A-Z+])', grouptext)
    sentencelist.append(sentences)

for paragraph in range(len(sentencelist)):
    for sentence in sentencelist[paragraph]:
        OUT.write(sentence)
        OUT.write('\n')
        OUT.write('\n')

OUT.close()
IN.close()
