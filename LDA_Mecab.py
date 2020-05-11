#!/usr/bin/env python
# coding: utf-8

# In[168]:


from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
from konlpy.tag import Komoran
import jpype
# p = jpype.getDefaultJVMPath()
# jpype.startJVM(p, convertStrings=False)
f = open("checked_review_data_r.csv", "r", encoding = 'utf-8')
lines = f.readlines()

sentences = []
for line in lines:
    if ',0' in line: #제품 유형별 lda
        sentences.append(line)
    
f.close()

#형태소 분석한 단어들의 list를 get
# hannanum = Hannanum()
# han_mophs = hannanum.morphs(lines)
# print("hannanum: ", han_morphs)
# selected_han = []
# for sentence1 in han_morphs:
#     for word, tag in sentence1:
#         if tag in ['Noun','Adjective', 'Verb']:
#             selected_han.append(word)

            
# kkma = Kkma()
# kkma_mophs = kkma.morphs(lines)
# print("kkma: ", kkma_morphs)
# selected_kkma = []
# for sentence1 in kkma_morphs:
#     for word, tag in sentence1:
#         if tag in ['Noun','Adjective', 'Verb']:
#             selected_kkma.append(word)

            
# komoran = Komoran()
# kom_morphs = komoran.morphs(lines)
# print("komoran: ", kom_morphs)
# selected_kom = []
# for sentence1 in kom_morphs:
#     for word, tag in sentence1:
#         if tag in ['Noun','Adjective', 'Verb']:
#             selected_kom.append(word)

            
mecab = Mecab()
sentences_tag = []
for sentence in sentences:
    morph = mecab.pos(sentence)
    sentences_tag.append(morph)
# print("mec: ", mec_morphs)
selected_mec = []
n_sentence = 0

nouns_tag = []
for sentence in sentences:
    morph = mecab.nouns(sentence)
    nouns_tag.append(morph)
# print("mec: ", mec_morphs)

for sentence1 in sentences_tag:
    selected_mec.append([])
    for word, tag in sentence1:
        if tag in ['NNG', 'VV']:
            selected_mec[n_sentence].append(word)
    n_sentence += 1
    
        
            
# twitter = Twitter()
# twit_morphs = twitter.morphs(lines)
# print("twitter: ", twit_morphs)
# selected_twit = []
# for sentence1 in twit_morphs:
#     for word, tag in sentence1:
#         if tag in ['Noun','Adjective', 'Verb']:
#             selected_twit.append(word)


# f.close()

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel


# Create Dictionary
id2word = corpora.Dictionary(nouns_tag)
 
# Create Corpus
texts = selected_mec
 
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]
 
# View
print(corpus[:3])

num_topics = 5
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics,
                                      random_state=100, update_every=1, chunksize=100,
                                      passes=10, alpha='auto', per_word_topics=True)

from pprint import pprint

# Print the Keyword in the 10 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus)) # a measure of how good the model is. lower the better.

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim # don't skip this
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# Visualize the topics
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
vis

pyLDAvis.save_html(vis, 'rinnai_hybrid_lda_mecab.html')




