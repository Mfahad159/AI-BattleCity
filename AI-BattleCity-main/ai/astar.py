import heapq
from constants import GRID_SIZE, ASTAR_COST, INF

def astar(grid_matrix, start, goal):
    """
    A* Search Algorithm.
    g(n): Path cost (Empty=1, Forest=1, Brick=3, Steel=inf, Water=inf)
    h(n): Manhattan distance to goal
    """
    # priority queue: (f_score, (x, y))
    pq = []
    gx, gy = goal
    
    # h(start)
    h_start = abs(start[0] - gx) + abs(start[1] - gy)
    heapq.heappush(pq, (h_start, start))
    
    came_from = {start: None}
    g_score = {start: 0}
    
    while pq:
        f, current = heapq.heappop(pq)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]
            
        x, y = current
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                tile = grid_matrix[ny][nx]
                cost = ASTAR_COST.get(tile, INF)
                
                if cost == INF:
                    continue
                
                tentative_g = g_score[current] + cost
                
                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g
                    h = abs(nx - gx) + abs(ny - gy)
                    came_from[(nx, ny)] = current
                    heapq.heappush(pq, (tentative_g + h, (nx, ny)))
                    
    return None # No path
