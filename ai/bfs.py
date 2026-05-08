from collections import deque
from constants import GRID_SIZE, EMPTY, FOREST

def bfs(grid_matrix, start, goal):
    """
    Standard BFS to find the shortest path from start to goal.
    Treats EMPTY (0) and FOREST (4) as passable (cost 1).
    Returns a list of (x, y) tuples representing the path.
    """
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            return path[::-1] # Reverse to get start -> goal
            
        x, y = current
        # 4 cardinal directions
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                # Passable check: 0 (EMPTY) or 4 (FOREST) or 5 (EAGLE - if goal)
                tile = grid_matrix[ny][nx]
                if (tile in [EMPTY, FOREST, 5]) and (nx, ny) not in visited:
                    visited[(nx, ny)] = current
                    queue.append((nx, ny))
                    
    return None # No path found
