# coding=utf-8
 # 模拟网络通信路由表建立的Daoijkstra算法实现
 # Author bnkR.
import random
def d_gen(d_max, thr, INF):
 # 此函数用来生成一条随机长度的边，thr是无穷大的阈值
 d = random.randint(1, d_max)
 if d < thr:
     return d
 else:
     return INF

# 通过LSP表返回邻居
def neighbor(lsp, INF):
 return [ix for ix in range(len(lsp)) if lsp[ix] != INF and lsp[ix] != 0]

# Dijkstra算法
def dijkstra(gram, vs, INF):
 vNum = len(gram[0])
 cfmTable = [vs] #证实表
 cfmInfo = [(INF, INF) for ix in range(vNum)] #证实表信息(距离,下一跳)
 cfmInfo[vs] = (0, vs)
 testTable = neighbor(gram[vs], INF) #试探表
 testInfo= [(gram[vs][ix], ix) for ix in range(vNum)] #试探表信息(距离,下一跳)
 v_next = vs
 while True:
     lsp = gram[v_next]
     #获取v_next的LSP包，现实中可以调用其他函数
     for v in neighbor(lsp, INF):
         #遍历v_next的所有邻居
         if v not in cfmTable and v not in testTable:
             #如果此邻居不在证实表和试探表中，则加入试探表
             testTable.append(v)
         if lsp[v] + cfmInfo[v_next][0] < testInfo[v][0]:
             #如果在试探表中，则比较它到源的距离是否比试探表中之前存的更小，是则替换
             testInfo[v] = (lsp[v] + cfmInfo[v_next][0], cfmInfo[v_next][1])
     if not len(testTable):    #检查试探表是否非空
         break
     #找到试探表中的最小节点，将其加入证实表，并指定为下一个v_next
     minCostNode = testInfo[testTable[0]]
     vmin = testTable[0]
     for v in testTable:
         if testInfo[v][0] < minCostNode[0]:
             minCostNode = testInfo[v]
             vmin = v
     cfmTable.append(vmin)
     cfmInfo[vmin] = minCostNode
     v_next = vmin
     testTable = [v for v in testTable if v != v_next]
 return (cfmTable, cfmInfo)

# 主函数，图的生成，通过调整阈值来随机确定一些无法达到的边。
def main():
 INF = 1000
# vNum = 10
# gram = [[d_gen(100, 10, INF) for col in range(vNum)] for row in range(vNum)]
# # 对称化矩阵
# for row in range(vNum):
#     gram[row][row] = 0
#     for col in range(row):
#         gram[row][col] = gram[col][row]
# for row in range(vNum):
#     print gram[row]
 gram = [[0, 0.1, 0.3, 1000, 1000, 1000], [0.1, 0, 1000, 0.2, 0.4, 1000], [0.3, 1000, 0, 1000, 0.7, 1000], [1000, 0.2, 1000, 0, 1000, 0.5], [1000, 0.4, 0.7, 1000, 0, 0.4], [1000, 1000, 1000, 0.5, 0.4, 0]]
 print dijkstra(gram, 0, INF)
 
if __name__ == "__main__":
 main()
