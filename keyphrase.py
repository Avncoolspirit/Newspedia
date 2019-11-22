def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pke
import string
from nltk.corpus import stopwords

from googlesearch import search
import requests

'''
Extract top-5 keyphrases and search for relevant content
'''

# 1. create a TopicRank extractor.
extractor = pke.unsupervised.TopicRank()

# 2. load the content of the document.
# TODO: Process closed-caption stream and extract keywords for every 5 sentences
extractor.load_document(input='federal.txt')

# 3. select the longest sequences of nouns and adjectives, that do
#    not contain punctuation marks or stopwords as candidates.
pos = {'NOUN', 'PROPN', 'ADJ'}
stoplist = list(string.punctuation)
stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
stoplist += stopwords.words('english')
extractor.candidate_selection(pos=pos, stoplist=stoplist)

# 4. build topics by grouping candidates with HAC (average linkage,
#    threshold of 1/4 of shared stems). Weight the topics using random
#    walk, and select the first occuring candidate from each topic.
extractor.candidate_weighting(threshold=0.74, method='average')

# 5. get the 10-highest scored candidates as keyphrases
keyphrases = extractor.get_n_best(n=5, redundancy_removal=True)
keyphrases = [keyphrase for (keyphrase, weight) in keyphrases]
print("Keyphrases:")
print(keyphrases)

keyphrases = ' '.join(keyphrases)

wiki_query = keyphrases + ' wikipedia'

for result in search(wiki_query, tld='com', lang='en', num=10, stop=10, pause=2):
	if 'wikipedia.org' in result:
		title = result.split('/')[-1]
		wiki_request = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=' + title + '&limit=1&namespace=0&format=json'
		wiki = requests.get(wiki_request, timeout=(5, 20))
		wiki_card = wiki.json()
		break

if wiki_card:
	print("Wiki card:")
	print(wiki_card)
else:
	print("Wikipedia Not Available")

news_query = keyphrases.replace(' ', '%20')
news_request = 'https://newsapi.org/v2/everything?q=' + news_query + '&sortBy=popularity&pageSize=10&apiKey=f086208033f04214bd283cc403681fc1'
news = requests.get(news_request, timeout=(5, 20))
news_list = news.json()['articles']
relevant_articles = []
print("Relevant news stories:")
for article in news_list:
	relevant_article = ((article['title'], article['url']))
	relevant_articles.append(relevant_article)
	print(relevant_article)