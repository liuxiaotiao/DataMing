class FPtreeNode:
    def __init__(self, idValue, parentNode):
        self.id = idValue
        self.time = 1
        self.Link = None
        self.parent = parentNode
        self.childNode = {}

    def inc(self, Occur):
        self.time += Occur

    def isRootNode(self):
        if self.parent != None:
            return True
        else:
            return False

    def settime(self, count):
        self.time = count

    def gettime(self):
        return self.time

    def linkNextNode(self, name, newtreeNode):
        self.childNode[name] = newtreeNode

    def getchildNode(self,name):
        return self.childNode[name]

    def getparentNode(self):
        return self.parent

    def getLink(self):
        return self.Link

    def setLink(self,Link):
        self.Link=Link


def createTree(dataSet, minSup):
    headerTable = {}
    headerTb = {}
    for trans in dataSet:
        for item in trans:
            headerTb[item] = headerTb.get(item, 0) + dataSet[trans]
    for key in headerTb:
        if headerTb.get(key, 0) > minSup - 1:
            headerTable[key] = headerTb.get(key, 0)
    freqelement = set(headerTable.keys())

    headerTab = {}
    for k in headerTable:
        headerTab[k] = [headerTable[k], None]

    FPTree = FPtreeNode('Root', None)
    for tranS, num in dataSet.items():
        local = {}
        for item in tranS:
            if item in freqelement:
                local[item] = headerTab[item][0]
        if len(local) > 0:
            orItems = [v[0] for v in sorted(local.items(), key=lambda p: p[1], reverse=True)]
            changeTree(orItems, FPTree, headerTab, num)
    return FPTree, headerTab


def changeTree(items, FPTree, hTable, count):
    if items[0] in FPTree.childNode:
        FPTree.getchildNode(items[0]).inc(count)
    else:
        FPnextNode = FPtreeNode(items[0], FPTree)
        FPnextNode.settime(count)
        FPTree.linkNextNode(items[0], FPnextNode)
        if hTable[items[0]][1] == None:
            hTable[items[0]][1] = FPTree.getchildNode(items[0])
        else:
            a = hTable[items[0]][1]
            b = FPTree.getchildNode(items[0])
            while a.getLink() != None:
                a = a.getLink()
            a.setLink(b)
    if len(items) > 1:
        changeTree(items[1::], FPTree.getchildNode(items[0]), hTable, count)


def indexTree(leaf, findprePath):
    if leaf.isRootNode():
        findprePath.append(leaf.id)
        indexTree(leaf.getparentNode(), findprePath)


def findPath(FPtreeNode):
    condPats = {}
    while FPtreeNode != None:
        prePath = []
        indexTree(FPtreeNode, prePath)
        if len(prePath) > 1:
            condPats[frozenset(prePath[1:])] = FPtreeNode.gettime()
        FPtreeNode = FPtreeNode.getLink()
    return condPats


def mining(HTable, minSup, preFix, fIList):
    itemlist = [v[0] for v in sorted(HTable.items(), key=lambda p: p[1][0])]

    for basePat in itemlist:
        newFSet = preFix.copy()
        newFSet.add(basePat)
        fIList.append(newFSet)
        condPatt = findPath(HTable[basePat][1])
        myCondTree, currentHead = createTree(condPatt, minSup)
        if currentHead != None:
            mining(currentHead, minSup, newFSet, fIList)


def getRules(itemsets, frequencysets, mincof):
    iSet = {}
    for i in frequencysets:
        iSet[frozenset(i)] = 0

    for i in itemsets:
        for j in frequencysets:
            if j.issubset(i):
                iSet[frozenset(j)] = iSet.get(frozenset(j), 0) + 1

    d_order = sorted(iSet.items(), key=lambda n: n[1], reverse=False)

    for i in range(len(d_order)):
        for j in range(len(d_order)):
            if ((d_order[j][0] - d_order[i][0]) != frozenset()) & (d_order[i][0].issubset(d_order[j][0])):
                conf = d_order[j][1] / d_order[i][1]
                if conf >= mincof:
                    print(d_order[i][0], d_order[j][0] - d_order[i][0], conf)


if __name__ == "__main__":
    minSup = 2
    mincof = 0.6
    Dat = [
        ['Bread', 'Milk'],
        ['Bread', 'Diaper', 'Beer', 'Eggs'],
        ['Milk', 'Diaper', 'Beer', 'Coke'],
        ['Bread', 'Milk', 'Diaper', 'Beer'],
        ['Bread', 'Milk', 'Diaper', 'Coke']
    ]
    initSet = {}
    for i in Dat:
        initSet[frozenset(i)] = 1
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    myFreqList = []
    mining(myHeaderTab, minSup, set([]), myFreqList)

    c = []
    for y in Dat:
        d = set(y)
        c.append(d)
    print("Fset:", myFreqList)
    getRules(c, myFreqList, mincof)
