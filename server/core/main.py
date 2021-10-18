from itertools import permutations
import operator
import pandas as pd
import numpy as np
import numpy.matlib
import math

counts = 3757 # 样本总数
cols = [] # 存放每一列的名称 index为编号 即i
cols.append(0)
lists = {} # 存放每一列的list index为每一列的名称 即cols[i]
nodes = {} # 存放节点名称 index为两列编号的元祖 即(i, j)
nodes_scores = {} # 存放节点分数 index为两列编号的元祖 即(i, j)
route_scores = {} # 存放路径分数 index为两个节点index的元祖 即((a, b), (c, d))
nodes_index = {} # 存放节点序号 index为两列编号的元祖 即(i, j)
index_nodes = [] # 存放节点元祖 index为节点序号 即nodes_index的反转
tree = [] # 存放Tree的结构
Importance = {} # 存放节点重要性排序 index为两列编号的元祖 即(i, j)
usable_index_nodes = [] # 存放选中节点元祖 index为节点序号 即Important的反转
L_list = [] # 存放节点的排列顺序
layout = ['5A', '5B', '5C', '5D', '5E', '5F', '5G', '5H', '5I', '5J', '5K', '5L',
          '5M', '5N', '5O', '5P'] # 存放节点名称


class Node:
    def __init__(self, nodeNo, nodeSize, nodeConnected):
        self.nodeNo = nodeNo
        self.nodeSize = nodeSize
        self.nodeConnected = nodeConnected

    def display(self):
        print("节点序号", self.nodeNo)
        print("节点大小", self.nodeSize)
        print("相连的节点", self.nodeConnected)


class Layout:
    def __init__(self, nodeCounts, nodes):
        self.nodeCounts = nodeCounts
        self.nodes = nodes
        self.matrix = np.matlib.identity(nodeCounts, dtype=int)
        self.list = set()
        for i in range(nodeCounts):
            for j in range(nodeCounts):
                if i == j:
                    continue
                elif i in self.nodes[j].nodeConnected:
                    self.matrix[i, j] = 1

    def displayCounts(self):
        print(self.nodeCounts)

    def displayNodes(self):
        for i in range(len(self.nodes)):
            self.nodes[i].display()

    def displayMatrix(self):
        print(self.matrix)

    def findMinDist(self, start, end):
        self.list.add(start)
        self.list.add(end)
        if self.matrix[start, end] == 1:
            return 1
        elif start == end:
            return 0
        else:
            minDist = 99
            for i in range(len(self.nodes[start].nodeConnected)):
                if self.nodes[start].nodeConnected[i] in self.list:
                    continue
                minDist = min(self.findMinDist(self.nodes[start].nodeConnected[i], end) + 1, minDist)
            return minDist

def get_data(counts, file_name): # get cols & lists
    for i in range(1, counts+1):
        csv_data = pd.read_csv(file_name, usecols=[i])
        cols.append(csv_data.columns[0])
        corpus = csv_data.values.tolist()
        for j in range(0, len(corpus)):
            if lists.get(cols[i]):
                lists[cols[i]].append(corpus[j][0])
            else:
                lists[cols[i]] = []
                lists[cols[i]].append(corpus[j][0])

def get_nodes_index(count):
    index = 0
    for i in range(1, count+1):
        for j in range(i + 1, count+1):
            nodes_index[(i, j)] = index
            index_nodes.append((i, j))
            tree.append([-1, -1])
            index += 1

def get_nodes_scores(count): # get nodes name & nodes scores
    for i in range(1, count+1):
        for j in range(i + 1, count+1):
            nodes[(i, j)] = cols[i] + '_' + cols[j]
            nodes_scores[(i, j)] = get_H2(lists[cols[i]], lists[cols[j]])

def get_route_scores(): # get route scores
    for key1 in nodes.keys():
        for key2 in nodes.keys():
            if key1 == key2:
                continue
            else:
                route_scores[(key1, key2)] = get_H4(lists[cols[key1[0]]], lists[cols[key1[1]]], lists[cols[key2[0]]], lists[cols[key2[1]]])

def get_dic(item): # get a dic of a col
    ans = {}
    for i in range(0, len(item)):
        if ans.get(item[i]):
            ans[item[i]] += 1
        else:
            ans[item[i]] = 1
    return ans

def get_P_dic(X, Y): #得到两列的概率
    ans = {}
    for i in range(0, counts):
        if ans.get((X[i], Y[i])):
            ans[(X[i], Y[i])] += 1
        elif not ans.get((X[i], Y[i])):
            ans[(X[i], Y[i])] = 1
    for item in ans.keys():
        ans[item] /= counts
    return ans

def get_H2(X, Y): #计算联合信息熵 两个list
    P_dic = get_P_dic(X, Y)
    ans = 0
    for item in P_dic:
        ans += math.log(P_dic[item], 2) * P_dic[item]
    ans = -ans
    return ans

def get_H4(A, B, C, D): # 4 lists
    H1 = 0
    H2 = 0
    P_dic1 = get_P_dic(A, B)
    for item in P_dic1:
        H1 += math.log(P_dic1[item], 2) * P_dic1[item]
    P_dic2 = get_P_dic(C, D)
    for item in P_dic2:
        H2 += math.log(P_dic2[item], 2) * P_dic2[item]
    H1 = -H1
    H2 = -H2
    used = {}
    ans = 0
    for i in range(0, counts):
        if not (A[i], B[i], C[i], D[i]) in used.keys():
            P = P_dic1[(A[i], B[i])] * P_dic2[(C[i], D[i])]
            ans += math.log(P, 2) * P
            used[(A[i], B[i], C[i], D[i])] = 1
    ans += H1 + H2
    return ans

def get_tree(node, usable_nodes, usable_nodes_scores, route_scores, node_indexes, k = 5):
    if usable_nodes == {} or k == 0:
        return
    # copy
    usable_route_scores = route_scores.copy()
    if node in usable_nodes:
        usable_nodes.pop(node)
    if node in usable_nodes_scores:
        usable_nodes_scores.pop(node)

    # get max
    route_max = -1
    max_node_route = node
    max_node = max(usable_nodes_scores, key = usable_nodes_scores.get) # max node score
    max_node_name = nodes[max_node]
    max_node_score = nodes_scores[max_node]

    for (item1, item2) in usable_route_scores.keys():
        if item1 == node and item2 in usable_nodes and usable_route_scores[(item1, item2)] > route_max:
            route_max = usable_route_scores[(item1, item2)]
            max_node_route = item2
        if item2 == node and item1 in usable_nodes and usable_route_scores[(item1, item2)] > route_max:
            route_max = usable_route_scores[(item1, item2)]
            max_node_route = item1

    #print(max_node, max_node_route)
    if max_node == max_node_route:
        tree[node_indexes[node]][0] = node_indexes[max_node]
        tree[node_indexes[node]][1] = node_indexes[max_node]
        usable_nodes.pop(max_node)
        usable_nodes_scores.pop(max_node)
        get_tree(max_node, usable_nodes, usable_nodes_scores, usable_route_scores, node_indexes, k - 1)
    else:
        tree[node_indexes[node]][0] = node_indexes[max_node]
        usable_nodes.pop(max_node)
        usable_nodes_scores.pop(max_node)
        get_tree(max_node, usable_nodes, usable_nodes_scores, usable_route_scores, node_indexes, k - 1)

        tree[node_indexes[node]][1] = node_indexes[max_node_route]
        usable_nodes[max_node] = max_node_name
        usable_nodes_scores[max_node] = max_node_score
        usable_nodes.pop(max_node_route)
        usable_nodes_scores.pop(max_node_route)
        get_tree(max_node_route, usable_nodes, usable_nodes_scores, usable_route_scores, node_indexes, k - 1)

def get_importance(count, choice): # 得到重要性排序
    farther = max(nodes_scores, key=nodes_scores.get)
    #print(farther)
    for i in range(1, count+1):
        Importance[farther] = i
        usable_index_nodes.append(farther)
        if choice[i-1] == 0:
            farther = index_nodes[tree[nodes_index[farther]][0]]
        elif choice[i-1] == 1:
            farther = index_nodes[tree[nodes_index[farther]][1]]

def get_permutation(count): # 得到全排列
    List = []
    for i in range(count):
        List.append(i)
    for i in list(permutations(List)):
        L_list.append(list(i))

def computeScore(Layout_list, index_nodes, node_score_list, Importance_list, route_score_list, L_list, k=1):
    dic = {}
    maxValue = -1
    index_1 = -1
    index_2 = -1
    for item in Layout_list:
        Rim = 0
        Rre = 0
        for item_1 in L_list:
            for i in range(item.nodeCounts):
                p = -k * abs(Importance_list[index_nodes[item_1[i]]] - item.nodes[item_1[i]].nodeSize)
                Rim += node_score_list[index_nodes[item_1[i]]] * math.exp(p)
            for i in range(item.nodeCounts):
                for j in range(item.nodeCounts):
                    if i == j:
                        continue
                    tmp = (index_nodes[item_1[i]], index_nodes[item_1[j]])
                    p = -k * (item.findMinDist(item_1[i], item_1[j]) - 1)
                    Rre += route_score_list[tmp] * math.exp(p)
            ans = Rim + Rre
            #print(Layout_list.index(item))
            dic[layout[Layout_list.index(item)] +" "+"".join('%s' %id for id in item_1)] = ans
            if ans > maxValue:
                maxValue = ans
                index_1 = Layout_list.index(item)
                index_2 = L_list.index(item_1)
    sorted(dic.items(), key=lambda item: item[1], reverse=True)
    return index_1, index_2, dic



get_data(5, 'FlightDelayStatistics2015.csv') #读取数据
get_nodes_scores(5) #得到节点名称 并计算分数
print(nodes)
print(nodes_scores)
get_route_scores()
print(route_scores)
get_nodes_index(5)
print(nodes_index)
print(index_nodes)
get_tree(max(nodes_scores, key=nodes_scores.get), nodes.copy(), nodes_scores.copy(), route_scores, nodes_index)
#print(nodes_index[max(nodes_scores, key=nodes_scores.get)]) #树的最高节点
print(tree)
get_importance(5, [0,0,0,0,0])
#print(Importance)
#print(usable_index_nodes)
get_permutation(5)

#Layout
Five_1 = Layout(5, [Node(0, 1, [1]), Node(1, 1, [0, 2]), Node(2, 1, [1, 3]),
                    Node(3, 1, [2, 4]), Node(4, 1, [3])])
Five_2 = Layout(5, [Node(0, 3, [1, 3]), Node(1, 2, [0, 2, 3, 4]), Node(2, 3, [1, 4]),
                    Node(3, 1, [0, 1, 4]), Node(4, 1, [1, 2, 3])])
Five_3 = Layout(5, [Node(0, 1, [1, 4]), Node(1, 3, [0, 2, 4]), Node(2, 3, [1, 3, 4]),
                    Node(3, 3, [2, 4]), Node(4, 2, [0, 1, 2, 3])])
Five_4 = Layout(5, [Node(0, 2, [1, 3]), Node(1, 2, [0, 2, 4]), Node(2, 1, [1, 4]),
                    Node(3, 2, [0, 4]), Node(4, 2, [1, 2, 3])])
Five_5 = Layout(5, [Node(0, 2, [1, 4]), Node(1, 2, [0, 2, 4]), Node(2, 2, [1, 3, 4]),
                    Node(3, 2, [2, 4]), Node(4, 1, [0, 1, 2, 3])])
Five_6 = Layout(5, [Node(0, 2, [1, 2]), Node(1, 2, [0, 2]), Node(2, 1, [0, 1, 3, 4]),
                    Node(3, 2, [2, 4]), Node(4, 2, [2, 3])])
Five_7 = Layout(5, [Node(0, 1, [1, 4]), Node(1, 2, [0, 2, 4]), Node(2, 1, [1, 3, 4]),
                    Node(3, 1, [2]), Node(4, 2, [0, 1, 2])])
Five_8 = Layout(5, [Node(0, 3, [1, 3, 4]), Node(1, 4, [0, 2, 3]), Node(2, 1, [1, 3, 4]),
                    Node(3, 4, [0, 1, 2, 4]), Node(4, 2, [0, 2, 3])])
Five_9 = Layout(5, [Node(0, 1, [1, 3, 4]), Node(1, 3, [0, 2, 3]), Node(2, 3, [1, 3]),
                    Node(3, 2, [0, 1, 2, 4]), Node(4, 2, [0, 3])])
Five_10 = Layout(5, [Node(0, 1, [1, 2, 4]), Node(1, 2, [0, 2, 3]), Node(2, 3, [0, 1, 3, 4]),
                    Node(3, 3, [1, 2, 4]), Node(4, 2, [0, 2, 3])])
Five_11 = Layout(5, [Node(0, 1, [1, 3, 4]), Node(1, 2, [0, 2, 3]), Node(2, 1, [1, 3, 4]),
                    Node(3, 2, [0, 1, 2, 4]), Node(4, 2, [0, 2, 3])])
Five_12 = Layout(5, [Node(0, 2, [1]), Node(1, 2, [0, 2, 3, 4]), Node(2, 1, [1, 3]),
                    Node(3, 1, [1, 2, 4]), Node(4, 1, [1, 3])])
Five_13 = Layout(5, [Node(0, 1, [1, 4]), Node(1, 3, [0, 2, 4]), Node(2, 3, [1, 3, 4]),
                    Node(3, 1, [2, 4]), Node(4, 2, [0, 1, 2, 3])])
Five_14 = Layout(5, [Node(0, 2, [1, 3, 4]), Node(1, 3, [0, 2, 3]), Node(2, 2, [1, 3, 4]),
                    Node(3, 3, [0, 1, 2, 4]), Node(4, 1, [0, 2, 3])])
Five_15 = Layout(5, [Node(0, 2, [1, 3, 4]), Node(1, 4, [0, 2, 3]), Node(2, 4, [1, 3]),
                    Node(3, 3, [0, 1, 2, 4]), Node(4, 1, [0, 3])])
Five_16 = Layout(5, [Node(0, 1, [1]), Node(1, 1, [0, 2]), Node(2, 1, [1, 3, 4]),
                    Node(3, 2, [2, 4]), Node(4, 2, [2, 3])])


Layout_List = [Five_1, Five_2, Five_3, Five_4, Five_5,
               Five_6, Five_7, Five_8, Five_9, Five_10,
               Five_11, Five_12, Five_13, Five_14, Five_15, Five_16]

index_1, index_2, res = computeScore(Layout_List, usable_index_nodes, nodes_scores, Importance, route_scores, L_list)

#Layout_List[index_1].displayNodes()
print(layout[index_1])
print(L_list[index_2])
point = []
for i in range(len(L_list[index_2])):
    point.append(usable_index_nodes[L_list[index_2][i]])
print(point)

f = zip(res.keys(), res.values())
c = sorted(f, key = lambda x: x[1])
index = len(c)-1
for i in range(20):
    print(c[index])
    index -= 1



