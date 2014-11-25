import os
import json

RAW_DATA_DIR = "./raw/"
PROCESS_DATA_DIR = "./refined/"
gWordKeys = {}
gTotalVector = {}

gCategoryKeys = {'Arts':10,
                 'Aesthetics':11,
                 'Performing arts':12,
                 'History':20,
                 'Theories of history':21,
                 'Science':30,
                 'Philosophy of science':31,
                 'Science education':32,
                 'Biography':40,
                 'Autobiographies':41,
                 'Biographical novels':42,
                 'Sports':50,
                 'Sports trophies and awards':51,
                 'Wars involving the states and peoples of Africa':61,
                 'Wars involving the United Kingdom':62,
                 'Wars involving the Soviet Union':63}

selectedCategories = ['Arts', 'Aesthetics', 'Performing arts', 'History', 'Theories of history', 'Science', 'Philosophy of science', 'Science education', 'Biography','Autobiographies', 'Biographical novels', 'Sports', 'Sports trophies and awards','Wars involving the states and peoples of Africa', 'Wars involving the United Kingdom','Wars involving the Soviet Union']
def processGatheredArticles():
    if not os.path.exists(PROCESS_DATA_DIR):
        os.makedirs(PROCESS_DATA_DIR)

    dataset = []
    if os.path.exists(RAW_DATA_DIR):
        filenames = os.listdir(RAW_DATA_DIR)
        for filename in filenames:
            if ".json" in filename and "Article" in filename:
                with open (RAW_DATA_DIR + filename) as f:
                    d = json.load(f)
                    
                    article = {}
                    article['title'] = d['title']
                    article['categories'] = categoriesList(d['categories'])
                    content = stripSpecialChars(d['content']).lower()
                    article['countVector'] = vectorizeContent(content)
                    article['wordCount'] = len(content.split())
                    dataset.append(article)

    dataBundle = {}
    dataBundle['dataset'] = dataset
    dataBundle['categoryKey'] = gCategoryKeys
    dataBundle['wordKey'] = gWordKeys
    dataBundle['totalsVector'] = gTotalVector
    with open(PROCESS_DATA_DIR + "dataBundle.json", 'w') as f:
        f.write(json.dumps(dataBundle))

    overviewData(dataset)

    dbExplained = '''Structure of dataBundle.json

    'categoryKey' -> Dictonary mapping category strings to numerical keys.
                     Keys are defined such that X0 is the main category and
                     X1,...,X9 would be subcategories

    'wordKey' -> Dictionary mapping words to a numerical key. These keys are
                 then used as the index for an article's countVector corresponding
                 to the given word.

    'dataset' -> List of articles
        article = {'title':<title>,
                   'categories':<list of numerical keys for categories>,
                   'countVector': <dictionary mapping numerical word keys to counts of word for article>,
                   'wordCount': <total number of words in the article>}

    'totalsVector' -> A dictionary mapping numerical word keys to the total number of
                      times the corresponding word is used thoughout all of the articles.
    '''

    with open(PROCESS_DATA_DIR + "README.txt", 'w') as f:
        f.write(dbExplained)

def stripSpecialChars(content):
    # Check that it is ascii and alpha-numeric or whitespace
    return "".join(c for c in content if ord(c) < 128 and (c.isalnum() or c.isspace()))

def vectorizeContent(content):
    contentVector = {}
    wordBag = content.split()
    for word in wordBag:
        key  = getWordKey(word)
        if not key in contentVector:
            contentVector[key] = 0
        contentVector[key] += 1
        gTotalVector[key] += 1
    return contentVector

def categoriesList(categories):
    catList = []
    l = list(set(categories).intersection(selectedCategories))
    for category in l:
        catList.append(gCategoryKeys[category])
    return catList

def getWordKey(word):
    if not word in gWordKeys:
        gWordKeys[word] = len(gWordKeys)
        gTotalVector[gWordKeys[word]] = 0
    return gWordKeys[word]

def overviewData(dataset):
    categoryCountOver = {}
    categoryCountUnder = {}
    noCatOver = 0
    noCatUnder = 0
    for a in dataset:
        if a['wordCount'] >= 500:
            categoryCount = categoryCountOver
            if len(a['categories']) == 0:
                noCatOver += 1
        else:
            categoryCount = categoryCountUnder
            if len(a['categories']) == 0:
                noCatUnder += 1

        for c in a['categories']:
            if not c in categoryCount:
                categoryCount[c] = 0
            categoryCount[c] += 1

    with open(PROCESS_DATA_DIR + "Overview.txt", 'w') as f:
        f.write("Category Count Breakdown\n")
        f.write("    Category      Under 500      Over 500\n")
        for key in gCategoryKeys:
            numKey = gCategoryKeys[key]
            if not numKey in categoryCountOver:
                categoryCountOver[numKey] = 0
            if not numKey in categoryCountUnder:
                categoryCountUnder[numKey] = 0
            f.write("    " + key + ": " + str(categoryCountUnder[numKey]) + "    " + str(categoryCountOver[numKey]) + "\n")
        f.write("    No Category: " + str(noCatUnder) + "    " + str(noCatOver) + "\n")
        f.write("\n")
        f.write("Total articles: " + str(len(dataset)) + "\n")

processGatheredArticles()
