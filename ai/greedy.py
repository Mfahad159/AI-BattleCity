from constants import GRID_SIZE, EAGLE_POS

def greedy_step(grid_matrix, current, goal):
    """
    Greedy Best-First Search: returns the single best next step towards goal.
    Uses Manhattan distance as heuristic h(n).
    """
    x, y = current
    gx, gy = goal
    
    best_move = None
    min_h = float('inf')
    
    # 4 cardinal directions
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            # Greedy doesn't care about passable in pathfinding, 
            # but we'll check it to avoid wall-bumping if possible.
            # However, Fast Tank Spec says: "If next tile is Brick THEN shoot it".
            # So we just pick the neighbor that is closest to goal.
            
            h = abs(nx - gx) + abs(ny - gy)
            if h < min_h:
                min_h = h
                best_move = (dx, dy)
                
    return best_move
