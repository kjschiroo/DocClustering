import json

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

def getClassForGroup(group):
    votes = {}
    for v in group:
        cats = v['categories']
        for c in cats:
            if not c in votes:
                votes[c] = 0
            votes[c] += 1/float(len(cats))
    topCount = max(votes.values())
    for c in votes:
        if topCount == votes[c]:
            return c

def scoreGroup(group, confusionMatrix):
    cls = getClassForGroup(group)/10
    for v in group:
        cats = v['categories']
        for c in cats:
            cMod = c/10
            confusionMatrix[cls][cMod] += 1/float(len(cats))

def printConfusion(m):
    output = ""
    output += "".ljust(7)
    theKeys = sorted(gCategoryKeys.values())
    theModKeys = []
    for key in theKeys:
        modKey = key/10
        if not modKey in theModKeys:
            theModKeys.append(modKey)

    for key in theModKeys:
        output += str(key).rjust(7)
    print output
    for key1 in theModKeys:
        output = str(key1).rjust(7)
        for key2 in theModKeys:
            boxCount = int(m[key1][key2]*100)/100.0
            output += str(boxCount).rjust(7)
        print output

with open("kmeans6.json", 'r') as f:
    results = json.load(f)

groups = results['groups']

confusionMatrix = {}
for key1 in gCategoryKeys.values():
    key1Mod = key1/10
    confusionMatrix[key1Mod] = {}
    for key2 in gCategoryKeys.values():
        key2Mod = key2/10
        confusionMatrix[key1Mod][key2Mod] = 0

for g in groups:
    scoreGroup(groups[g], confusionMatrix)

printConfusion(confusionMatrix)
