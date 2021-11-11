"""COMPLING2 final project by Kelsey E. Wanket 11/05/2021"""

import nltk
from nltk.parse.generate import generate, demo_grammar
#from nltk.corpus import treebank
from nltk import CFG

def rmduptuple(in_tuple_list):
    '''
    Function that removes duplicate items in the list
    '''
    return [j for j in (set(tuple(i) for i in in_tuple_list))]


def rmduplstentry(in_list):
    '''
    Function that removes duplicate 'sets' in the list
    '''
    out_list = []
    for i in in_list:
        if i not in out_list:
            out_list.append(i)
    return out_list


def grammar2bigram(in_sent_list):
    '''
    Function that generates bigrams from the possible list of sentences in the CFG
    '''

    # container for the bigram
    out_bigram = []

    # splitting the words in each sentences in the list of sentences

    for sent in in_sent_list:
       splitted = sent.split()
       splitted.insert(0," ")
       splitted.append(" ")
       sent_siz = len(splitted)

       # generating bigram from given sentences
       for i in range(sent_siz-1):
          out_bigram.append((splitted[i],splitted[i+1]))

    # removing duplicate entries in the bigrams
    out_bigram = rmduptuple(out_bigram)

    return out_bigram


def bigram2trans(in_bigram):
    '''
    Function that generates transitions from bigram transitions,
    in the form of python dictionary data type, that consist of
    strings (key for the python dictionary) and a set (values that
    are corresponding to the key) like the following
      transitions = {a : {b,c,d}, d : {f,g}}
    which expresses the transitions of
      a -> b
      a -> c
      a -> d
      d -> f
      d -> g
    '''

    words       =  []
    bi_siz  =   len(in_bigram)

    for i in range(bi_siz):
       words.append(in_bigram[i][0])

    # removing any duplicate elements in the list
    sep_words = rmduplstentry(words)

    #
    transitions =  {}
    sets        =  set()

    # building transitions
    for i in sep_words:
       for j in range(bi_siz):
           if (in_bigram[j][0] == i):
              sets.add(in_bigram[j][1])

           transitions[i] = sets
       sets     =  set()

    return transitions


def addblanks2sent(in_grammar_sent_siz,in_grammar_trans,in_sent):
    '''
    function that adds 'blank' to signal initials to the first word and the last word of
    the input sentence.
    blanks are only added to the words that are in the grammar
    '''
    splitted             =  in_sent.split()

    if (len(splitted) < min(in_grammar_sent_siz)):
       print("\nThe input sentence is unacceptable.\n")
       exit()

    grammar_trans_keys   =  in_grammar_trans.keys()

    init_words           =  in_grammar_trans[" "]
    final_words          =  set()

    # parsing final words from given grammar
    for key in grammar_trans_keys:
       if (" " in in_grammar_trans[key]):
          final_words.add(key)

    # adding initial to the first word of the input sentence
    for word in init_words:
       if (word == splitted[0]):
          splitted.insert(0," ")

    # adding initial to the last word of the input sentence
    # comparing the final words from the grammar and the input sentence
    for word in final_words:
       if (word == splitted[-1]):
          splitted.append(" ")

    return splitted


def sent2bigram(in_sent):
    '''
    Function that generates bigrams from an input sentence.
    input sentence has to be processed using addblanks2sent() function.
    '''

    sent_siz =  len(in_sent)

    # container for the bigram
    out_bigram = []

    # generating bigrams (each bigram is in 'set')
    for i in range(sent_siz - 1):
       out_bigram.append((in_sent[i],in_sent[i+1]))

    # removing duplicate tuples in the list
    out_bigram  =  rmduptuple(out_bigram)

    return out_bigram


def chk_sent(in_grammar_trans,in_sent):
    '''
    Function to check if the input sentence is acceptable to the
given grammar
    '''

    print("\nInput sentence : \"{0:s}\"".format(" ".join(in_sent)))

    sent_siz       =  len(in_sent)

    # extracting the 'keys' in the grammar (in the form of python dictionary)
    grammar_keys   =  list(in_grammar_trans.keys())

    # checking if the sentence has acceptable initial and final state
    if (in_sent[0] != " " or in_sent[-1] != " "):
       print("-> Wrong initial or final state. The input sentence is unacceptable.\n")
       exit()

    # comparing the transitions by iterating through the grammar's transitions
    # and the sentence's transitions
    for i in range(sent_siz-1):
        # current(i th) and next (i+1 th) word of the input sentence
        crnt_step_word    =  in_sent[i]
        next_step_word    =  in_sent[i+1]

        # transitions of the grammar with the i th word of the input sentence
        crnt_step_trans   =  in_grammar_trans[in_sent[i]]


        # if the input sentence has a word that are not in the grammar,
        # the input sentence is not acceptable
        if (next_step_word not in grammar_keys):
          print("-> The input sentence is unacceptable. The following word is not acceptable in the given grammar.")
          print("    unacceptable word =>\"{0:s}\"\n".format(next_step_word))
          exit()

       # if the sentence's transition exist in the grammar's transitions, move on to the next transition
        if (next_step_word in crnt_step_trans):
           continue

       # if the sentence's transition does not exist in the grammar's transitions,
       # the input sentence is not acceptable.
        else:
          print("-> Unacceptable transition found in the sentence. The input sentence is unacceptable.")
          #print("  transition => ","\"",next_step_word,"\"","to","\"",prev_step,"\"","does not exist in the given grammar.\n")
          print("    transition => \"{0:s}\" to \"{1:}\" does not exist in the given grammar.\n".format(crnt_step_word,next_step_word))
          exit()

    # if we cannot find any exceptions, then the input sentence is acceptable to the given grammar
    print("-> The input sentence is acceptable.\n")



'''
Main code
'''

# input sample sentences, and generate bigrams and transitions
#input_sent     =  input("type an input sentence : ") #"a dog in the man"
input_sent     =  "a dog saw a man a dog"

# calling the grammar and generating the sentences
grammar        = CFG.fromstring(demo_grammar)
gram_sent_list = []

gram_sent_size = []
for sents in generate(grammar):
    gram_sent_size.append(len(sents))
    gram_sent_list.append(' '.join(sents))

# generating bigrams and transitions of the given grammar
gram_bigram    =  grammar2bigram(gram_sent_list)
gram_trans     =  bigram2trans(gram_bigram)

# pre-processing sample sentence (adding the initial and final #)
sample_sent    =  addblanks2sent(gram_sent_size,gram_trans,input_sent)

# checking the sentence's validity
chk_sent(gram_trans,sample_sent)