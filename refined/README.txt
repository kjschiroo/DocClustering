Structure of dataBundle.json

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
    