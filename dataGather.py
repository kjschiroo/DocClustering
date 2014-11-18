import os
import json
from time import sleep
import wikipedia    # github.com/goldsmith/Wikipedia

from wikitools import wiki
from wikitools import category

RAW_DATA_DIR = "./raw/"
gGatheredArticleTitles = {}

selectedCategories = ['Arts', 'Aesthetics', 'Performing arts', 'History', 'Theories of history', 'Science', 'Philosophy of science', 'Science education', 'Biography','Autobiographies', 'Biographical novels', 'Sports', 'Sports trophies and awards','Wars involving the states and peoples of Africa', 'Wars involving the United Kingdom','Wars involving the Soviet Union']

def getPageAndWriteJSON(page, fileName):
    dataToSave = {}
    dataToSave['title'] = page.title
    dataToSave['categories'] = page.categories
    dataToSave['content'] = page.content

    print "Writing " + RAW_DATA_DIR + fileName
    with open(RAW_DATA_DIR + fileName,'w') as f:
        f.write(json.dumps(dataToSave))

def tryToSavePageWithTitle(title, theCategory, fileName):
    page = None
    if title in gGatheredArticleTitles:
        print "    Already have it, " + gGatheredArticleTitles[title]['filename']
        if not theCategory in gGatheredArticleTitles[title]['category']:
            gGatheredArticleTitles[title]['category'].append(theCategory)
        return False
    try:
        sleep(20)
        page = wikipedia.WikipediaPage(title)
        getPageAndWriteJSON(page, fileName)
        gGatheredArticleTitles[title] = {'filename':fileName, 'title':title, 'category':[theCategory]}
        print "    That's new, " + gGatheredArticleTitles[title]['filename']
        return True
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

    with open (RAW_DATA_DIR + "THIS_ROUND_DATA_GUIDE.txt", 'w') as f:
        f.write("Categories Searched:\n")
        site = wiki.Wiki("http://en.wikipedia.org/w/api.php")
        i = len(gGatheredArticleTitles) + 1
        for theCategory in selectedCategories:
            f.write("   " + theCategory + ": " + str(i) + "-")
            cat  = category.Category(site, theCategory)
            sleep(20)
            for article in cat.getAllMembersGen(namespaces=[0]):
                print theCategory + ": " + article.title
                fileName = "Article" + str(i).zfill(4) + ".json"
                if tryToSavePageWithTitle(article.title, theCategory, fileName):
                    i += 1
            f.write(str(i-1) + "\n")
    with open (RAW_DATA_DIR + "DATA_GUIDE.json", 'w') as f:
        f.write(json.dumps(gGatheredArticleTitles))

def getAlreadyGatheredMapFromArticleFiles():
    if os.path.exists(RAW_DATA_DIR):
        filenames = os.listdir(RAW_DATA_DIR)
        for filename in filenames:
            if ".json" in filename and "Article" in filename:
                with open (RAW_DATA_DIR + filename) as f:
                    d = json.load(f)
                    gGatheredArticleTitles[d['title']] = {'filename':filename, 'title':d['title'], 'category':[]}

getAlreadyGatheredMapFromArticleFiles()
gatherEntries()
