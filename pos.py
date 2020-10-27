import re
from decimal import *       #this module will help us deal with the very small numbers.
getcontext().prec = 6       # for now I am rounding to ~6 spaces, I think
                            # When the numbers start getting very tiny, we can use the log method from this module
                            #but I didn't want to waste time figuring that part out quite yet!

dict = {}
firstword = []
splitsentence = []
pairlist = []
TAGLIST = ['N', 'J', 'V', 'A', 'I', 'Z', 'C', 'D', 'W', 'H', 'B', 'T', 'R']
highestprob = []
unique_words = {}
almost_zero_prob = 1/5000000


# this function reads in a txt file that is tagged like this /N /V /D ... etc
# it outputs a string of the entire corpus minus all the new line characters.
def get_corpus(file_name):
    line = "xxx"
    entire_corpus = ""
    with open(file_name, "r", encoding="UTF-8-sig", errors="ignore") as file:
        line = file.readline()
        while line:
            line.strip()
            entire_corpus += line + " "
            line = file.readline()
    #entire_corpus = entire_corpus.replace("\n", "")
    return entire_corpus

# This is a function which calculates the probability that a word is any given tag.
# It takes a giant string of all the words (and punctuation) in the corpus
# It puts the string in lowercase, then searches for instances of unique words
# These words are stored in a dictionary called unique_words = { raw_word : {"total" : x, "tag" : y} }
# The probability that a word is a certain tag is the number of times it appears as a tag, divided by the total occurrences
# These values are stored in a dictionary called word_tag_prob = { raw_word : {"tag" : z/unique_words[raw_word]["total"], etc. repeated for each tag } }
# The output of this function is the dictionary of all the probabilities of the words given their tags
def calculate_word_tag_prob(entire_corpus):
    global TAGLIST
    entire_corpus = entire_corpus.replace("\n", "")
    entire_corpus = re.sub(r'``', r'"', entire_corpus)
    entire_corpus = re.sub(r"''", r'"', entire_corpus)
    # entire_corpus = re.sub(r'\/[A-Z]\s', " ", entire_corpus)
    #entire_corpus = entire_corpus.lower()
    words_in_corpus = entire_corpus.split()
    # return words_in_corpus
    for word in words_in_corpus:
        word_pair = word.split(r'/')
        raw_word = word_pair[0]
        tag = word_pair[1]
        if raw_word not in unique_words:
            unique_words[raw_word] = {"total": 1, tag: 1}
        else:
            unique_words[raw_word]["total"] += 1 #calculates the number of times a unique word appears in the corpus
            if tag not in unique_words[raw_word]:
                unique_words[raw_word][tag] = 1
            else:
                unique_words[raw_word][tag] += 1
    #TAGLIST = [tag.lower() for tag in TAGLIST]
    word_tag_prob = {}
    for raw_word in unique_words.keys():
        word_tag_prob[raw_word] = {}
        total_word_count = unique_words[raw_word]["total"]
        for tag in TAGLIST:
            if tag in unique_words[raw_word]:
                word_with_tag_count = unique_words[raw_word][tag]
            else:
                word_with_tag_count = almost_zero_prob
            word_tag_prob[raw_word][tag.upper()] = (word_with_tag_count/total_word_count)
    return word_tag_prob
    #word_tag_prob[raw_word][tag]


# This function takes the first word in every sentence in the corpus and returns the probability that
# the first word starts with a tag
# The output of this function is a initial probs {
def calculate_initial_prob(entire_corpus):
    ssdict = {}
    initial_probs = {}
    sentence = entire_corpus.split("\n")
    return_string = ""
    for x in range(len(sentence)):
        firststring = sentence[x].split('/')
        if len(firststring) == 2:
            firstword.append(firststring[1])
    for word in firstword:
        if word not in ssdict:
            ssdict[word] = 1
        else:
            ssdict[word] += 1
    for item in ssdict:
        probfirst = ssdict[item] / len(firstword)
        initial_probs[item] = probfirst
    return initial_probs
    # initial_probs[tag]

#rint(calculate_initial_prob(get_corpus("corpus-brown-simple.txt")))

# This function takes a list of tagged words, removes the words, and calculates the probabilities that a single
# tag will come after another tag by dividing all instances of the second_tagcounting all instances of a tag
# It outputs the transition_prob { tag
def calculate_transition_prob(entire_corpus):
    transition_counts = {}
    tag_counts = {}
    sentences = entire_corpus.split('\n')
    for sentence in sentences:
        tagslist = "".join(re.findall(r'/[NJVAIZCDWHBTR] ', sentence))
        tagslist = re.sub(r'/', "", tagslist)
        tagslist = re.sub(r'\s', "", tagslist)
        #tagslist = re.sub(r'\n', "", tagslist)
        #entire_corpus = re.sub(r'\s', '', entire_corpus)
        for i in range(len(tagslist)):
            if i == 0:
                prev_tag = "start"
            else:
                prev_tag = tagslist[i-1]
            transition = (prev_tag, tagslist[i]) #sentence[i] is the current tag
            if transition not in transition_counts:
                transition_counts[transition] = 1
            else:
                transition_counts[transition] += 1
            if tagslist[i] not in tag_counts:
                tag_counts[tagslist[i]] = 1
            else:
                tag_counts[tagslist[i]] += 1
    transition_probs = {}
    for transition in transition_counts.keys():
        transition_probs[transition] = transition_counts[transition]/tag_counts[transition[1]] #we want the current tag; 0 is the previous tag
    return transition_probs
    # transition_probs[(prev_tag, current_tag)]

def train(tagged_corpus):
    model = {}
    model["transition_prob"] = calculate_transition_prob(tagged_corpus)
    model["word_tag_prob"] = calculate_word_tag_prob(tagged_corpus)
    model["initial_prob"] = calculate_initial_prob(tagged_corpus)
    return model

def tag_corpus(untagged_corpus, model, output_file_name):
    with open(output_file_name, "w", encoding="UTF-8-sig", errors="IGNORE") as writer:
        sentences = untagged_corpus.split("\n")     #prior to processing, the corpus should have been run through a sentence splitter that puts each sentence on a new line
        for sentence in sentences:      # Each iteration of this for-loop is independent; would be good for parallel processing
            sentence = sentence.lstrip()
            sentence = sentence.rstrip()
            if sentence == "":
                continue
            words = re.split("\s+", sentence)
            tag_probs = fill_viterbi_table(model, words)
            max_tag_prob = -10000
            tag_table = {}
            last_word = len(words)-1
            for tag in TAGLIST:
                tag_prob = tag_probs[last_word][tag][0]    #This is the current tag probability for the last word
                if tag_prob > max_tag_prob:
                    max_tag_prob = tag_prob
                    tag_table[last_word] = tag
            next_tag = tag_table[last_word]
            for word_i in reversed(range(len(words)-1)):
                tag_table[word_i] = tag_probs[word_i + 1][tag_table[word_i + 1]][1]    #This could be made easier to read
            for word_i in range(len(words)):
                writer.write(words[word_i] + "/" + tag_table[word_i] + " ")
            writer.write("\n")

def fill_viterbi_table(model, words):
    tag_probs = {}
    prev_word_i = -1
    for word_i in range(len(words)):  # Would be BAD for parallel processing because each iteration depends on the previous one!
        word = words[word_i]
        tag_probs[word_i] = {}  # for each word, we need a new dictionary inside the dictionary
        force_noun = (word not in model["word_tag_prob"])
        for tag in TAGLIST:  # always capitalize your global constants because it's easier to read!
            if prev_word_i < 0:
                if force_noun and tag != "N":
                    tag_probs[word_i][tag] = (almost_zero_prob, None)
                else:
                    trans_prob = model["initial_prob"].get(tag, almost_zero_prob)
                    word_tag_prob = model["word_tag_prob"][word][tag]
                    tag_probs[word_i][tag] = (trans_prob * word_tag_prob, None)  # Since the prev_prob is 1, we can just pretend it's not there
            else:
                best_prev_tag = None
                max_prev_tag_prob = -100000  # something less than 0
                for prev_tag in TAGLIST:
                    prev_prob = tag_probs[prev_word_i][prev_tag][0]
                    trans_prob = model["transition_prob"].get((prev_tag, tag), almost_zero_prob)
                    word_tag_prob = model["word_tag_prob"].get(word, {}).get(tag, almost_zero_prob)
                    tag_prob = prev_prob * trans_prob * word_tag_prob
                    if tag_prob > max_prev_tag_prob:
                        max_prev_tag_prob = tag_prob
                        best_prev_tag = prev_tag
                if force_noun and tag != "N":
                    tag_probs[word_i][tag] = (almost_zero_prob, best_prev_tag)
                else:
                    tag_probs[word_i][tag] = (max_prev_tag_prob, best_prev_tag)
        prev_word_i = word_i
    return tag_probs

def main(tagged_corpus_file, untagged_corpus_file, output_file_name):
    tagged_corpus = get_corpus(tagged_corpus_file)
    model = train(tagged_corpus) #all the pieces
    untagged_corpus = get_corpus(untagged_corpus_file)
    tag_corpus(untagged_corpus, model, output_file_name)

main("corpus-brown-simple.txt", "first_untagged_corpus.txt", "first_tagged_corpus.txt")
