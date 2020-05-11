#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

import re
import pickle
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

from pprint import pprint

with open('data/okt_token.pkl', 'rb') as f:
    tokens = pickle.load(f)
print(tokens)

# create dictionary
id2word = corpora.Dictionary(tokens)
# 
corpus = [id2word.doc2bow(token) for token in tokens]
print(corpus[0])

num_topics = 5
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics,
                                      random_state=100, update_every=1, chunksize=100,
                                      passes=10, alpha='auto', per_word_topics=True)

# print the keyword in the 10 topics
pprint(lda.print_topics())
doc_lda = lda[corpus]
# compute perplexity
print("\nPerplexity: ", lda.log_perplexity(corpus))
# compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda, texts=tokens, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

# visualize the topics
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda, corpus, id2word)

pyLDAvis.save_html(vis, "data/lda_topic5_checked_stopwords_review_data.html")

