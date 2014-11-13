import os
import json
from time import sleep
import wikipedia    # github.com/goldsmith/Wikipedia

from wikitools import wiki
from wikitools import category

RAW_DATA_DIR = "./raw/"
gGatheredArticleTitles = {}

selectedCategories = ['Arts', 'History', 'Science', 'Biography', 'Sports']

def getPageAndWriteJSON(page, fileName):
    dataToSave = {}
    dataToSave['title'] = page.title
    dataToSave['categories'] = page.categories
    dataToSave['content'] = page.content

    with open(RAW_DATA_DIR + fileName,'w') as f:
        f.write(json.dumps(dataToSave))

def tryToSavePageWithTitle(title, fileName):
    page = None
    if title in gGatheredArticleTitles:
        return False
    try:
        page = wikipedia.WikipediaPage(title)
        if len(page.content.split()) > 500:
            getPageAndWriteJSON(page, fileName)
            gGatheredArticleTitles[title] = fileName
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
            if randomeTitle in gGatheredArticleTitles:
                # Find a different article
                continue
            print randomTitle
            fileName = "Random" + str(i).zfill(len(str(numberEntries))) + ".json"
            if(tryToSavePageWithTitle(randomTitle, fileName)):
                gGatheredArticleTitles[randomTitle] = fileName
                break


def gatherEntries():
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)

    site = wiki.Wiki("http://en.wikipedia.org/w/api.php")
    i = 0
    for theCategory in selectedCategories:
        cat  = category.Category(site, theCategory)
        for article in cat.getAllMembersGen(namespaces=[0]):
            print article.title
            fileName = "Article" + str(i).zfill(4) + ".json"
            if tryToSavePageWithTitle(article.title, fileName):
                i += 1
            sleep(20)
            if i % 500 == 0:
                break

gatherEntries()
