from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import word_tokenize
from nltk import pos_tag, pos_tag_sents
from nltk.corpus import wordnet as wn
import glob
from collections import defaultdict
from itertools import groupby
import pandas as pd
stop_words=['a', 'able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be',
            'because','been','by','did','else','ever','every','for','from','get','got','had','has','have','he','her','hers',
            'him','his','how','however','i','if','in','into','is','it','its','just','least','let','may','me','might','my','of',
            'off','on','or','other','our','own','rather','said','say','says','she','should','since','so','than','that','the',
            'their','them','then','there','these','they','this','tis','to','was','us','was','we','were','what','when','where',
            'while','who','whom','why','will','would','yet','you','your','They','Look','Good','A', 'Able','About','Across',
            'After','All','Almost','Also','Am','Among','An','And','Any','Are','As','At','Be','Because','Been','By','Did',
            'Else','Ever','Every','For','From','Get','Got','Had','Has','Have','He','Her','Hers','Him','His','How','However',
            'I','If','In','Into','Is','It','Its','Just','Least','Let','May','Me','Might','My','Of','Off','On','Or','Other',
            'Our','Own','Rather','Said','Say','Says','She','Should','Since','So','Than','That','The','Their','Them','Then',
            'There','These','They','This','Tis','To','Was','Us','Was','We','Were','What','When','Where','While','Who','Whom',
            'Why','Will','Would','Yet','You','Your','not']
stopwords = [a.lower() for a in stop_words]

def change_tag(tag):
    if tag in ['JJ','JJR','JJS']: return 'a'
    if tag in ['NN','NNS']: return 'n'
    if tag in ['RB','RBR','RBS']: return 'r'
    if tag in ['VB','VBD','VBG','VBN','VBZ','VBP','VD','VDD','VDG','VDN','VDZ','VDP','VH','VHD','VHG',
              'VHN','VHZ','VHP','VV','VVD','VVG','VVN','VVP','VVZ']: return 'v'
    
#preprocessing tge tagged document 
def tagant(text):
    token = word_tokenize(text)
    word_tag = [a.split('_') for a in token if '_' in a ]
    tags = []
    bad_tag = ['UH', 'NP', 'CC','CD','EX','FW','MD','NPS','PDT','POS','PP','PPS','RP','SENT','SYM',
               'TO','UH','WDT','WP','WPS','WRB']
    for i in word_tag:
        if i[0].lower() not in stopwords and i[0].isalpha() and i[1] not in bad_tag:
             tags.append(tuple((i[0].lower(),change_tag(i[1]))))
    return tags


def extract_path(path):
    with open(path,"r", encoding="utf8") as f:
        txt = f.read()
    return txt

#process each document
def calculate_neg(text):
    tags = tagant(text)
    pos = neg = 0
    neg_words = []
    #print (tags)
    for i in tags:
        word, tag = i[0],i[1]
        if len(list(swn.senti_synsets(word,tag))) > 0:
            a = list(swn.senti_synsets(word,tag))[0]
            a_neg = a.neg_score()
            a_pos = a.pos_score()
            pos += a_pos
            neg += a_neg
            print (word + ", " + tag+ ", Pos = " + str(a_pos) + ", Neg = " + str(a_neg))
            if (a_neg - a_pos > 0.3):
                neg_words.append(word)
    return [neg - pos, neg_words, neg, pos]

#process each case
def neg_for_group(path):
    group = process(path)
    score =  sum(calculate_neg(i)[0] for i in group)/len(group)
    pos =  sum(calculate_neg(i)[2] for i in group)/len(group)
    neg =  sum(calculate_neg(i)[3] for i in group)/len(group)
    words = []
    for i in group:
        words += calculate_neg(i)[1]
  
    words = dict_of_neg(words)
    return [score, words, pos, neg]

def dict_of_neg(words):
    dict_words = defaultdict(int)
    words.sort()
    for key, group in groupby(words):
        leng = len(list(group))
        if ( leng > 2):
            dict_words[key] = leng
    return dict_words 

# select the tagged document only
def process(path):
    group =[]
    files = glob.glob(path)
    for i in range(len(files)):
        file = files[i]
        with open(file,'r',encoding="utf8") as f:
            group.append(f.read())
    return group[1::2]

a1_score = neg_for_group("a1-paris/*")
a2_score = neg_for_group("a2-nigeria/*")
b1_score = neg_for_group("b1-belgium/*")
b2_score = neg_for_group("b2-pakistan/*")
c1_score = neg_for_group("c1-france/*")
c2_score = neg_for_group("c2-iraq/*")

items = [('Case',["Score","Pos","Neg"]),("a1",[a1_score[0], a1_score[2], a1_score[3]]),("a2",[a2_score[0], a2_score[2], a2_score[3]]),
         ("b1",[b1_score[0], b1_score[2],b1_score[3]]),("b2",[b2_score[0], b2_score[2], b2_score[3]]),
         ("c1",[c1_score[0], c1_score[2], c1_score[3]]),("c2",[c2_score[0], c2_score[2], c2_score[3]])]
df = pd.DataFrame.from_items(items)
