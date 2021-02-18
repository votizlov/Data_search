import nltk  
import numpy as np  
import random  
import string
import operator

import bs4 as bs  
import urllib.request  
import re
from matplotlib import pyplot as plt

raw_html = urllib.request.urlopen('https://habr.com/ru/post/122700/')
raw_html = raw_html.read()

article_html = bs.BeautifulSoup(raw_html, 'lxml')

article_paragraphs = article_html.find_all('p')

article_text = ''

for para in article_paragraphs:  
    article_text += para.text

corpus = nltk.sent_tokenize(article_text)

for i in range(len(corpus )):
    corpus [i] = corpus [i].lower()
    corpus [i] = re.sub(r'\W',' ',corpus [i])
    corpus [i] = re.sub(r'\s+',' ',corpus [i])

print(len(corpus))
#print(corpus[5])

wordfreq = {}
for sentence in corpus:
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        if token not in wordfreq.keys():
            wordfreq[token] = 1
        else:
            wordfreq[token] += 1

import heapq
most_freq = heapq.nlargest(200, wordfreq, key=wordfreq.get)

print(most_freq)
sentence_vectors = []
for sentence in corpus:
    sentence_tokens = nltk.word_tokenize(sentence)
    sent_vec = []
    for token in most_freq:
        if token in sentence_tokens:
            sent_vec.append(1)
        else:
            sent_vec.append(0)
    sentence_vectors.append(sent_vec)
sentence_vectors = np.asarray(sentence_vectors)

sorted_x = sorted(wordfreq.items(), key=operator.itemgetter(1))
print(sorted_x)
#x, y = zip(wordfreq)
#plt.plot(sorted_x)
#plt.imshow(sentence_vectors, interpolation='nearest')
plt.scatter(*zip(*sorted_x))
plt.show()