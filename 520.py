import re

testString = "\"You are a nice - \" \"So are you!\"\nI love him. I? Love him? Truly! O! 'Tis grand!" #This is a silly test string with some weird examples.

# Can you please fix the code so it can read a .txt file?
#IN = open("text.txt")
OUT = open("output.txt", "w")
line = "XXX"
text = []
sentencelist = []
current_sent = ""

# I commented these out but we can add them back later
#while line:
#    line = IN.readline()
#    line.strip()
#    text.append(line)

for token in re.finditer('"*\'*[A-Z]*[a-z]*\!*\.*\?*\-*"*\s*\r*\n*', testString):
    token = token.group(0) #this has something to do with regex groups and parenthesis;
    current_sent = current_sent + token
    if re.search('[.!?\-\"](\s|\n|\Z)', token):
        sentencelist.append(current_sent)
        current_sent = ""

print(sentencelist) #This line is to show that the code is putting what we have decided are sentences into a list.

# Can you please fix the code here so that the output is the content of sentencelist?
for paragraph in range(len(sentencelist)):
    for sentence in sentencelist[paragraph]:
        OUT.write(sentence)
        OUT.write('\n')
        OUT.write('\n')
        OUT.write('\n')

OUT.close()
#IN.close()
