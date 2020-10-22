# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:39:08 2020

@author: Redlinl
"""


import stanfordnlp  
import numpy as np
import matplotlib.pyplot as plt
nlp = stanfordnlp.Pipeline() 

# File used to 
f = open("PBS.txt", "r", encoding = "utf-8")

# Reads the text from the file and obtains nlp dependencies
sentence = f.read();
doc = nlp(sentence)

# Variables to store data about words and dependencies between them
toinf = 0;
bareinf = 0;
imp = 0;
ind = 0;
pvoice = 0

# Variables to denote count of different verb times
s = ""
prevword = None;
i = 0

# 12 different verb tense and aspect combinations in English:
# Simple present, past , future
# Present, past, future perfect
# Present, past, future progressive
# Present, past, future, perfect progressive
# count is organized as [present, past, future]
# With each sublist being [simple, perfect, progressive, perfect progressive]
types = ['present','past','future' ]
count = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Iterates through the sentences from the text
for sent in doc.sentences:
    print("\n")
    i = 0
    
    # Iterates through the words
    for word in sent.words:
        
        # Looks for the auxiliary verb "will" to find future tenses
        if (word.upos == 'AUX' and word.text == 'will'):
            
            # Finds next words to determine verb placement
            if (i < (len(sent.words)-1)):
                nextword = sent.words[i+1]
            
            if (i < (len(sent.words)-2)):
                nextnextword = sent.words[i+2]
                
            if (i < (len(sent.words)-3)):
                
                nextnextnextword = sent.words[i+3]
            
            # Looks for "have" to find perfect tenses
            if ((i < (len(sent.words)-1)) and nextword.text == 'have'):
                if ((i < (len(sent.words)-2)) and nextnextword.text == 'been'):
                    if ((i < (len(sent.words)-3)) and (('Tense=Pres' in nextnextnextword.feats and 'VerbForm=Part' in nextnextnextword.feats) or 'Ger' in nextnextnextword.feats)):
                        count[2][3]+= 1
                    else:
                        count[2][2] += 1
                else:
                    count[2][2]+= 1
            else:
                if ((i < (len(sent.words)-1)) and nextword.text == 'be'):
                    count[2][1] += 1
                else:
          
                    count[2][0] += 1
                    
        # Simple present tense is easily found using the tense attribute
        elif((word.upos == 'VERB' or word.lemma == 'be') and 'Tense=Pres' in  word.feats and 'Mood=Ind' in word.feats):
            if (i < len(sent.words)-1):
                nextword = sent.words[i+1]
            if ((i < len(sent.words)-1) and ('Tense=Pres|VerbForm=Part' in nextword.feats or 'Ger' in nextword.feats) ):
                count[0][1] +=1
            else:
                count[0][0] +=1
        # Simple past tense is easily found using the tense attribute
        elif((word.upos == 'VERB' or word.lemma == 'be') and 'Tense=Past' in  word.feats and 'Mood=Ind' in word.feats):
            if (i < len(sent.words)-1):
                nextword = sent.words[i+1]
            if ((i < len(sent.words)-1) and ('Tense=Pres|VerbForm=Part' in nextword.feats or 'Ger' in nextword.feats)):
                count[1][1] +=1
            else:
                count[1][0] +=1
        
        # looks for perfect and progressive present tenses
        elif('NOUN' in word.upos or 'PRON' in word.upos):
            
            if (i < len(sent.words)-1):
                nextword = sent.words[i+1]
            if (i < (len(sent.words)-2)):
                nextnextword = sent.words[i+2]
                if (nextnextword.text == 'added'):
                    print('here')
            if (i < (len(sent.words)-3)):
                nextnextnextword = sent.words[i+3]
            if ((i < len(sent.words)-1) and nextword.text == 'have'):
                print('here')
                if ((i < (len(sent.words)-2)) and nextnextword.text == 'been'):
                    if ((i < (len(sent.words)-3)) and ('Tense=Pres|VerbForm=Part' in nextnextnextword.feats or 'Ger' in nextnextnextword.feats)):
                        count[0][3]+= 1
                    else:
                        count[0][2] += 1
                else:
                    count[0][2]+= 1
            if ((i < len(sent.words)-1) and nextword.text == 'had'):
                print('here')
                if ((i < (len(sent.words)-2)) and nextnextword.text == 'been'):
                    
                    if ((i < (len(sent.words)-3)) and ('Tense=Pres|VerbForm=Part' in nextnextnextword.feats or 'Ger' in nextnextnextword.feats)):
                        count[1][3]+= 1
                    else:
                        count[1][2] += 1
                else:
                    count[1][2]+= 1
        prevword = word
        i+=1
print(count)

# Plots data from sentence
fig, ax1 = plt.subplots()
labels = ['simple', 'progressive', 'perfect', 'perfect\n progressive']
x = np.arange(len(labels))
ax1.set_ylabel('Count')
ax1.set_title('Past Tenses')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()
ax1.bar(x, count[1], color = ['red', 'blue','orange','green'])
fig.tight_layout()


        

