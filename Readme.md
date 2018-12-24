# Link Analysis Report


## Report Information
名字：王康霖
學號：N26077124


## Implement

在 `algorithm.py` 中以三個 function 的方式來 implement 作業要求
### Hits
依以下步驟實做：

1. 取出 graph 中的所有 nodes, 並創兩個 dict 分別存每個 node 的 auth 和 hub (預設值為1)
2. 利用前次 iteration 計算出來的 auth 和 hub，更新本次的 auth 和 hub
3. Normalize，每個 node 的 hub 值除所有 hub 值之和，auth 值除所有auth值之和
4. 計算 diff，如果大於 min_diff，重複步驟2-4

### Pagerank
d = damping factor = 0.15

N = graph size = number of nodes

依以下步驟實做：

1. 取出graph中的所有nodes, 並創一個dict存每個node的pagerank(預設值為1/d)
2. 對每個node的rank，先給一個最小值((1-d)/N)
3. 對該node的每個parent，計算該parent給本node的rank值，並加總在rank上，即可得到該node的pagerank值
4. 計算diff，如果大於min_diff，重複步驟2-4

### Simrank
![](https://i.imgur.com/yUqn2id.png)
依照上圖公式計算每個pair(u->v)的sim值
I(a): a的所有parents


## Result Analysis and Discussion
![](https://i.imgur.com/AxxUouw.png)

執行 `python3 algorithm` 後會將結果分別存在 `result/` 對應的資料夾裡

### Hits
1. 如果 graph 是 cycle，所有 nodes 的 hub 和 auth 都是一樣的值 (graph_2)
2. 如果 graph 是對稱的話，對應的 node 的 hub 和 auth 會一樣 (graph_3)

### Pagerank
1. 如果 graph 是 cycle，所有 nodes 的 pagerank 都是一樣的值 (graph_2)
2. 如果 graph 是對稱的話，對應的 node 的 pagerank 一樣 (graph_3)
3. 所有 nodes 的 pagerank 值總合必為1

### Simrank
1. 如果每個 node 只有一個 parent，則 sim 仍是一個單位矩陣


## Computation Performance Analysis
執行 `python3 analysis.py`

```python
def c_time(graphs, method):
    time_list = list()
                                 
    if method == 1:
        compute_method = hits
    elif method == 2:
        compute_method = pagerank
    elif method == 3:
        compute_method = simrank
    ...
```       
```python    
for i, time in enumerate(c_time(graphs, method)):
    print('Graph {}:'.format(i+1))
    print('Nodes: {}, Edges: {}, Time: {} secs'.format(
        len(graphs[i].nodes()), len(graphs[i].edges()), time
    ))
```
由於一次輸出結果太長不方便截圖，因此分次執行
`method` 分別帶入 1，2，3；代表 hits，pagerank，simrank

### Hits
![](https://i.imgur.com/HoSl7ra.png)

### Pagerank
![](https://i.imgur.com/wbANOld.png)

### Simrank
![](https://i.imgur.com/ZDz3YoR.png)

根據以上結果發現，node 及 edge 的數量越多，花費的時間越久。此現象應該與 edge 有較大關係，因為每個演算法皆有 loop 過所有 edge。


## Increment of result
![](https://i.imgur.com/uQlgb6o.png)

加入一個 1 -> 1 的 edge 即可以讓 hub，auth，pagerank 都有小幅度的提升

hub 的計算方式是 children 的 auth 的加總
auth 的計算方式是 parents 的 hub 的加總
所以增加自己指到自己的edge，必能提高 hub 和 auth 值

如果一個 page 被 link，那麼 link 到這些 page 將增加其 pagerank。
如果沒有直接 link，link 到 page 路徑較短的 page 將會產生更強的效果。
發生這種情況是因為 rank 是由指向自己的 page 決定的。如果這個 page 貢獻更多的 page，可以貢獻更多（即 page 的路徑是較短的 page），那麼其 rank 會更高

## Question and Discussion

### Can link analysis algorithms really find the “important” pages from Web?

以上實做的三種分析演算法，都只考慮page之間的link，而不是他的content，content應該才是決定page是不是重要的關鍵之一。

### Disadvantage of PageRank

舊的 page rank 會比新的 page 高。因為即使是非常好的 new page 也不會有很多連結，除非它是某個站點的子站點。

### Disadvantage of HITS

HITS 演算法可以獲得比較高的 recall，算出具有較大Hub 值的 page 和具有較大 Auth 值的 page。但在實際應用中 HITS 演算法有以下幾個問題：

由 Root 生成 Base 的時間花費太高，由 Base 生成 digraph 也很耗時，計算量大
網頁中廣告等無關 link 影響 auth，hub 的計算，降低準確率

### Compare between HITS and PageRank

HITS 與使用者輸入的查詢有相關，而 PageRank 與查詢無關。
所以，HITS 可以單獨作為相似性計算標準，而PageRank 必須結合其他內容相似性計算才可以進行搜尋的比較。
HITS 因為與使用者查詢有關，所以必須在接收到使用者查詢後才能進行計算，計算效率較低；而 PageRank 則可以直接計算結果，計算效率較高。
HITS 的計算數量較少，只需特定 page 之間的 link；而 PageRank 則須對所有 page 進行計算。

### Conclusion

這三種方法都各自有優缺和要計算的考量。
在實務上，我們更應該依照需求去做改進，並在 time cost 上和準確率之間做最佳的平衡。