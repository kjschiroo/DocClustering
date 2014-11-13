import os
import json
from time import sleep
import wikipedia    # github.com/goldsmith/Wikipedia

RAW_DATA_DIR = "./raw/"

def getPageAndWriteJSON(page, fileName):
    dataToSave = {}
    dataToSave['title'] = page.title
    dataToSave['categories'] = page.categories
    dataToSave['content'] = page.content

    with open(RAW_DATA_DIR + fileName,'w') as f:
        f.write(json.dumps(dataToSave))

def tryToSavePageWithTitle(title, fileName):
    page = None
    try:
        page = wikipedia.WikipediaPage(title)
        if len(page.content.split()) > 500:
            getPageAndWriteJSON(page, fileName)
            return True
        else:
            return False
    except wikipedia.exceptions.WikipediaException as e:
        print e
        return False

def gatherRandomEntries(numberEntries):
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)

    for i in range(numberEntries):
        while(True):
            sleep(15)
            page = None
            randomTitle = wikipedia.random()
            print randomTitle
            fileName = "Random" + str(i).zfill(len(str(numberEntries))) + ".json"
            if(tryToSavePageWithTitle(randomTitle, fileName)):
                break

def gatherArticlesFromArticle(article):

def gatherEntries(type):

gatherRandomEntries(10)
