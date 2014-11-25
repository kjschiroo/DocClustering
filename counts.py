import os
import json
import csv

PROCESS_DATA_DIR = "./refined/"
COUNTS_DIR = "./counts/"

def articlesInCategory(category, dataset):
    articleSet = []
    for article in dataset:
        for c in article['categories']:
            if (c - category < 10) and (c - category >= 0):
                articleSet.append(article)
                break
    return articleSet

def countWordsInArticleSet(articleSet):
    return sum([a['wordCount'] for a in articleSet])

def freqForCategory(keyList, category, data):
    articles = articlesInCategory(category, data['dataset'])
    totalWordsInCat = countWordsInArticleSet(articles)
    wordFreq = []
    for key in keyList:
        numKey = str(data['wordKey'][key])
        total = 0.1
        for a in articles:
            if numKey in a['countVector']:
                total += a['countVector'][numKey]
        wordFreq.append([key, float(total)/float(totalWordsInCat)])
    return wordFreq
    

if not os.path.exists(COUNTS_DIR):
    os.makedirs(COUNTS_DIR)

filename = "dataBundle.json"
with open (PROCESS_DATA_DIR + filename, 'r') as f:
    data = json.load(f)

wordsAndCounts = []
with open (COUNTS_DIR + "totalCount.csv", 'wb') as f:
    countWriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    totalWords = sum(data['totalsVector'].values())
    for word in data['wordKey']:
        numKey = str(data['wordKey'][word])
        count = data['totalsVector'][numKey]
        wordsAndCounts.append([word, float(count)/float(totalWords)])
    wordsAndCounts = sorted(wordsAndCounts, key=lambda wordCountPair: wordCountPair[1], reverse=True)
    for row in wordsAndCounts:
        countWriter.writerow(row)

categories = {10:'Arts', 20:'History', 30:'Science', 40:'Biography', 50:'Sports', 60:'War'}
# wordsAndCounts is now sorted
orderedWords = [entry[0] for entry in wordsAndCounts]
for key in categories:
    categoryWordsAndCounts = freqForCategory(orderedWords, key, data)
    with open (COUNTS_DIR + categories[key] + "Count.csv", 'wb') as f:
        countWriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in categoryWordsAndCounts:
            countWriter.writerow(row)
