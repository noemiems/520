import re

in_file_name = "AaronHuey_2010X.txt" # <-------------- input file name here
file = open(in_file_name)
myText = file.read()
file.close()
myText = re.sub('<[^>]*>', "\n", myText)
out = open("sentences_in__" + in_file_name, "w") # This double underscore is to say that this is a prefix that was programatically added

abbrev_dict = ["Mr.", "Mrs.", "Ms.", "U.S.", "U.S.A.", "U.S.S.R", "A.L."]

for item in abbrev_dict:
    clean_item = re.sub(r'\.', 'THISISADOT', item)
    myText = re.sub(item, clean_item, myText)

split_regex = r'(\s*[.!?]"*\s*)|(\n\s*)|(\s*-"\s*)'
split_text = re.split(split_regex, myText) # The r at the beginning is some kind of flag to say, "hey, this is a regex."

for token in split_text:
    if token is None:
        continue
    is_sentence_boundary = re.search(split_regex, token) is not None
    if not is_sentence_boundary:
        token = re.sub(r'THISISADOT', '.', token)
        out.write(token)
    else:
        token = re.sub(r'\n', ' ', token)
        out.write(token + '\n\n')

# Wish list items: deal with rules for exceptions with abbreviations. Example: U.S. Stock Exchange vs He went to the U.S. Stock Exchanges there were doing great.
