import re

in_file_name = "AaronHuey_2010X.txt"
file = open(in_file_name)
myText = file.read().replace("\n", " ")
file.close()
file2 = open("sentences_in__" + in_file_name, "w") # This double underscore is to say that this is a prefix that was programmatically added


#myText = "\"You are a nice - \" \"So are you!\"\nI love him. I? Love him? Truly! O! 'Tis grand!"

# sent_list = []
current_sent = ""

for token in re.finditer('"*\'*[A-Z]*[a-z]*\!*\.*\?*\-*"*\s*\r*\n*', myText):
    token = token.group(0)
    current_sent = current_sent + token
    if re.search('[.!?\-\"](\s|\n|\Z)', token):
        #sent_list.append(current_sent)
        file2.write(current_sent + "\n\n")
        current_sent = ""

# print(sent_list)


