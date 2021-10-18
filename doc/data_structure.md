## Data Structure

Four json file:

```json
// vertex:

[
    {
        col: (x, x),
        name: "astring",
        score: 80,
        id: 0
    },
    {
    col: (x, x),
    name: "astring",
    score: 80,
    id: 1
    } ....
]


// edges:

edges[x][x] = score


// tree:

{
    0 : {   // 和 id 对应
        child: [1, 3],
        score: -1 // 叶子结点值不为 -1
    }
}


// layout:

[
    {
        layout_name: "5J",
        order: [23,32,12,2,1],             // order[x] 指布局的第 x 个放 id 节点
        score: 29232
    }
]
```