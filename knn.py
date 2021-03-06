import json
import random

high = 500
low = 3
K = 20

def toFreqVec(v):
    f = {}
    for i in v['countVector']:
        f[i] = v['countVector'][i]/float(v['wordCount'])
    f['categories'] = v['categories']
    return f

def cosine(vA, vB, low, high, totalsVector):
    c = 0
    for i in totalsVector:
        if totalsVector[i] >= low and totalsVector[i] <= high:
            if i in vA and i in vB:
                c += vA[i] * vB[i]
    return c

def findKClosest(v, trainingSet):
    buddies = []
    closeness = []
    for i in range(len(trainingSet)):
        temp = cosine(v, trainingSet[i], low, high, totalsVector)
        if len(buddies) < K:
            buddies.append(trainingSet[i])
            closeness.append(temp)
        else:
            m = min(closeness)
            if m < temp:
                j = closeness.index(m)
                buddies[j] = trainingSet[i]
                closeness[j] = temp

    return buddies

def classify(v, trainingSet):
    buddies = findKClosest(v, trainingSet)
    counts = {}
    for t in buddies:
        for c in t['categories']:
            cMod = c/10
            if not cMod in counts:
                counts[cMod] = 0
            counts[cMod] += 1

    highest = max(counts.values())
    cls = []
    for c in counts:
        if counts[c] == highest:
            cls.append(c)

    return cls

def printConfusion(m):
    output = ""
    output += "".ljust(7)
    for key in m.keys():
        output += str(key).rjust(7)
    print output

    for key1 in m.keys():
        output = str(key1).rjust(7)
        for key2 in m.keys():
            boxCount = int(m[key1][key2]*100)/100.0
            output += str(boxCount).rjust(7)
        print output

with open("refined/dataBundle.json", 'r') as f:
    dataBundle = json.load(f)

totalsVector = dataBundle['totalsVector']
dataset = dataBundle['dataset']
allCategories = dataBundle['categoryKey']

fDataset = []
for v in dataset:
    fDataset.append(toFreqVec(v))

confusionMatrix = {}
for key1 in allCategories.values():
    key1Mod = key1/10
    confusionMatrix[key1Mod] = {}
    for key2 in allCategories.values():
        key2Mod = key2/10
        confusionMatrix[key1Mod][key2Mod] = 0

random.shuffle(fDataset)
mark = len(fDataset)*9/10
mark = len(fDataset)*5/10
train = fDataset[0:mark]
test = fDataset[mark:len(fDataset)-1]

p = 0
for v in test:
    print str(p) + "/" + str(len(test))
    cls = classify(v, train)
    for ca in v['categories']:
        caMod = ca/10
        if not caMod in confusionMatrix:
            confusionMatrix[caMod] = {}
        for cl in cls:
            if not cl in confusionMatrix[caMod]:
                confusionMatrix[caMod][cl] = 0
            confusionMatrix[caMod][cl] += 1/float(len(v['categories'])*len(cls))
    p += 1
    if p % 5 == 0:
        printConfusion(confusionMatrix)

with open("knnCond.out", 'w') as f:
    output = ""
    output += "".ljust(7)
    for key2 in allCategories.values():
        output += str(key2).rjust(7)
    f.write(output + '\n')
    print output

    for key1 in allCategories.values():
        output = str(key1).rjust(7)
        for key2 in allCategories.values():
            boxCount = int(confusionMatrix[key1][key2]*100)/100.0
            output += str(boxCount).rjust(7)
        f.write(output + '\n')
        print output
