import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from sklearn import metrics as mr
import networkx as nx

counts = 3757 # 样本总数
cols = [] # 存放每一列的名称 index为编号 即i
cols.append(0)
lists = {} # 存放每一列的list index为每一列的名称 即cols[i]
nodes = {} # 存放节点名称 index为两列编号的元祖 即(i, j)
nodes_scores = {} # 存放节点分数 index为两列编号的元祖 即(i, j)
route_scores = {} # 存放路径分数 index为两个节点index的元祖 即((a, b), (c, d))
nodes_index = {} # 存放节点序号 index为两列编号的元祖 即(i, j)
tree = [] #存放Tree的结构


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


# test
get_data(5, 'FlightDelayStatistics2015.csv') #读取数据
#print(cols)
get_nodes_scores(5) #得到节点名称 并计算分数
#print(nodes)
#print(nodes_scores)
get_route_scores()
#print(route_scores)
get_nodes_index(5)
print(nodes_index)

# 作图 to do

'''
def find_neighbor(node, counts): # 得到邻居节点
    ans = []
    for i in range(1, counts+1):
        if i < node[0]:
            ans.append((i, node[0]))
        elif i > node[0]:
            ans.append((node[0], i))
        if i < node[1]:
            ans.append((i, node[1]))
        elif i > node[1]:
            ans.append((node[1], i))
    ans = set(ans)
    ans.remove(node)
    return ans
    
neighbors = find_neighbor((1, 2), 5)
print(neighbors)    
'''


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

    print(max_node, max_node_route)
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
# colors
'''
def colors(G):
    for edge in list(G.edges):
        if G.edges[edge]['property'] == 'max':
            return 'black'
        elif G.edges[edge]['property'] == 'max_node':
            return 'blue'
        elif G.edges[edge]['property'] == 'max_node_route':
            return 'red'
'''

get_tree(max(nodes_scores, key=nodes_scores.get), nodes.copy(), nodes_scores.copy(), route_scores, nodes_index)
print(nodes_index[max(nodes_scores, key=nodes_scores.get)]) #树的最高节点
print(tree)