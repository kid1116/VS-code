def numIslands(grid):
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # 边界检查和水域检查
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        # 标记为已访问（就地修改）
        grid[r][c] = '0'
        # 向四个方向深入探索
        dfs(r-1, c)   # 上
        dfs(r+1, c)   # 下
        dfs(r, c-1)   # 左
        dfs(r, c+1)   # 右

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)  # 淹没整个岛屿
    
    return count

grid=[
        ["0","1","0","1","0"],["1","0","1","0","1"],["0","1","0","1","0"],["1","0","1","0","1"],["0","1","0","1","0"]
    ]
print(numIslands(grid))