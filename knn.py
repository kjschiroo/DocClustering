import json
import random

high = 500
low = 3
K = 9

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
            if not c in counts:
                counts[c] = 0
            counts[c] += 1

    highest = max(counts.values())
    cls = []
    for c in counts:
        if counts[c] == highest:
            cls.append(c)

    return cls

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
    confusionMatrix[key1] = {}
    for key2 in allCategories.values():
        confusionMatrix[key1][key2] = 0

random.shuffle(fDataset)
train = fDataset[0:len(fDataset)/2]
test = fDataset[len(fDataset)/2:len(fDataset)-1]

p = 0
for v in test:
    print str(p) + "/" + str(len(test))
    cls = classify(v, train)
    for ca in v['categories']:
        if not ca in confusionMatrix:
            confusionMatrix[ca] = {}
        for cl in cls:
            if not cl in confusionMatrix[ca]:
                confusionMatrix[ca][cl] = 0
            confusionMatrix[ca][cl] += 1/float(len(v['categories'])*len(cls))
    p += 1
with open("knn.out", 'w') as f:
    output = ""
    output += "".ljust(5)
    for key2 in allCategories.values():
        output += str(key2).rjust(5)
    f.write(output + '\n')
    print output

    for key1 in allCategories.values():
        output = str(key1).rjust(5)
        for key2 in allCategories.values():
            output += str(confusionMatrix[key1][key2]).rjust(5)
        f.write(output + '\n')
        print output
