import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from glob import glob

blacklist_tags = [
    '[document]','noscript','header',
    'html','meta','head', 'input','script',
    # there may be more elements you don't want, such as "style", etc.
    ]
    
whitelist_tags = [
    'p', 'strong', 'div', 'span'
    # there may be more elements you such as "style", etc.
    ]


def parserssentry(entry):
    '''
    Returns and title and link from rss entry
    Parameters
    ----------
    entry : TYPE
        DESCRIPTION.
    Returns
    -------
    title : TYPE
        DESCRIPTION.
    link : TYPE
        DESCRIPTION.
    '''
    
    
    title = entry.title
    link = entry.link
    return title, link

def gethtml(link):
    '''
    Retutns the htmnl content from a link
    Parameters
    ----------
    link : TYPE
        DESCRIPTION.
    Returns
    -------
    html_page : TYPE
        DESCRIPTION.
    '''
    res = requests.get(link)
    html_page = res.content
    return html_page

def writefile(filename, content):
    '''
    Write a file with given contents
    Parameters
    ----------
    filename : TYPE
        DESCRIPTION.
    content : TYPE
        DESCRIPTION.
    Returns
    -------
    None.
    '''
    f = open(filename, "w",  encoding="utf-8")
    f.write(str(content))
    print('written -->'+  filename)
    f.close()
    
def parsehtml(html_page):
    '''
    Custom fn to extarct data from html page: WIP
    Parameters
    ----------
    html_page : TYPE
        DESCRIPTION.
    Returns
    -------
    None.
    '''
    soup = BeautifulSoup(html_page, 'html.parser')
    
    div_container = soup.find('div', class_ = 'article-page-body-content')
    
    #print(div_container)
    try:
        content=div_container.find('span', class_='paywall_content')
        #print(content)
        text = content.find_all(text=True)
    except:
        print ('paywall_content not found')
        content=div_container
        #print(content)
        text = content.find_all(text=True)

    #print (text)
    #set([t.parent.name for t in text])
    
    rawtext = ''
    for t in text: rawtext += '{} '.format(t)
            
    
    #print(rawtext)
    output = ''
    for t in text:
        #print(t.parent.name)
        #print(t)
        if t.parent.name in whitelist_tags:
            output += '{} '.format(t)
            #print ('add...' + t.parent.name + '    text-->', t)
        #else:
            #print ('skip...' + t.parent.name + '    text-->', t)
    return output


def main():
    '''
    Main function
    Returns
    -------
    None.
    '''
    NewsFeed = feedparser.parse("https://www.risk.net/feeds/rss/category/people")
    i=0
    for entry in NewsFeed.entries:
        i+=1
        print ("Processing " + str(i) + "  :----------------------------------")
        title,link = parserssentry(entry)
        print (title)
        print (link)
        html_page = gethtml(link)
        #print(html_page)
        
        writefile(f"{i:02d}news-html.txt", html_page)
        
        output = parsehtml(html_page) 
        #print(output)
        writefile(f"{i:02d}news.txt", output)
        print ('---------------------Done-------------------------')

if __name__ == "__main__":
    main()   
    
    
#%%
import re
import numpy as np
from pprint import pprint

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel


import spacy
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

NewsFeed = feedparser.parse("https://www.risk.net/feeds/rss/category/people")
news_titles = []
for entry in NewsFeed.entries:
    title,link = parserssentry(entry)
    news_titles.append(title)
        
filepaths = glob('*.txt')
news_desc = filepaths[1::2]

column_names =["Title", "Description"]

df = pd.DataFrame(columns=column_names)

for path,title in zip(news_desc, news_titles):
    with open(path, 'r', encoding="utf8") as file:
       data = file.read() 
    df.loc[len(df.index) ] = [title, data]
#%%
import re
import numpy as np
from pprint import pprint

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel


import spacy
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt



from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

data = df.Description.values.tolist()

data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

# Remove new line characters
data = [re.sub('\s+', ' ', sent) for sent in data]

# Remove distracting single quotes
data = [re.sub("\'", "", sent) for sent in data]

pprint(data[:1])
#%%
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(data))

print(data_words[:1])

#%%
# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# See trigram example
print(trigram_mod[bigram_mod[data_words[0]]])
#%%

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out
#%%
# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

print(data_lemmatized[:1])
#%%

# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# View
print(corpus[:1])

#%%
# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
#%%
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]
#%%
# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)
#%%
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
vis
pyLDAvis.save_html(vis, "Vis.html")
