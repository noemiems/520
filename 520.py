import re

#testString = "\"You are a nice - \" \"So are you!\"\nI love him. I? Love him? Truly! O! 'Tis grand!" #This is a silly test string with some weird examples.
IN = open("Test.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []
current_sent = ""

while line:
    line = IN.readline()
    line.strip()
    text.append(str(line))
    for x in range(len(text)):
        for token in re.finditer('"*\'*[A-Z]*[a-z]*\!*\.*\?*\-*"*\s*\r*\n*', text[x]):
            token = token.group(0) #this has something to do with regex groups and parenthesis;
            current_sent = current_sent + token
            if re.search('[.!?\-\"](\s|\n|\Z)', token):
                sentencelist.append(current_sent)
                current_sent = ""

#for x in range(len(sentencelist)):
#    print(sentencelist[x])
#    print('\n')

for x in range(len(sentencelist)):
        OUT.write(sentencelist[x])
        OUT.write('\n')
        OUT.write('\n')

#OUT.close()
#IN.close()

