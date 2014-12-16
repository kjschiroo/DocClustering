import json
import random

high = 500
low = 3

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

def findClosest(v, centroids):
    match = -1
    sim = -1
    for i in range(len(centroids)):
        temp = cosine(v, centroids[i], low, high, totalsVector)
        if temp > sim:
            match = i
            sim = temp
    return match

def evalGroup(g):
    catCount = {}
    for v in g:
        for c in v['categories']:
            if not c in catCount:
                catCount[c] = 0
            catCount[c] += 1
    total = len(g)
    output = ""
    cats = catCount.keys()
    cats.sort()
    for c in cats:
        output += str(c) + ":" + str(catCount[c]/float(total)) + " "
    output = output.strip()
    return output

with open("refined/dataBundle.json", 'r') as f:
    dataBundle = json.load(f)

totalsVector = dataBundle['totalsVector']
dataset = dataBundle['dataset']

fDataset = []
for v in dataset:
    fDataset.append(toFreqVec(v))

centroids = []
numCategories = 16
for i in range(numCategories):
    centroids.append(dict(random.choice(fDataset)))

r = 1
groups = {}
outputs = {}
for i in range(numCategories):
    outputs[i] = ""

with open("kmeans.out", 'w') as f:
    stop = False
    while not stop:
        print "Round " + str(r)
        f.write("Round " + str(r) + "\n")
        for i in range(numCategories):
            groups[i] = []
    
        i = 0
        for v in fDataset:
    #print str(i) + "/" + str(len(fDataset))
            close = findClosest(v,centroids)
            groups[close].append(v)
            i += 1
    
        stop = True
        for i in range(len(groups)):
            output = evalGroup(groups[i])
            if output != outputs[i]:
                stop = False
                print "*",

            outputs[i] = output
            print "Group " + str(i) + ": " + output
            f.write("Group " + str(i) + ": " + output + "\n")
            temp = {}
            for v in groups[i]:
                for k in v:
                    if k == 'categories':
                        continue
                    if not k in temp:
                        temp[k] = 0
    
                    temp[k] += v[k]
            centroids[i] = {}
            for k in temp:
                centroids[i][k] = temp[k]/len(groups[i])
        r += 1

with open("kmeans.json", 'w') as f:
    results = {'centroids':centroids, 'groups':groups, 'outputs':outputs}
    f.write(json.dumps(results))
