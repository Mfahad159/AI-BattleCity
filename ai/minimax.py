from constants import BOSS_HEURISTIC, GRID_SIZE

class MinimaxSolver:
    def __init__(self):
        self.nodes_evaluated = 0
        self.nodes_with_pruning = 0

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        self.nodes_evaluated += 1
        
        if depth == 0 or game_state['is_over']:
            return self.evaluate(game_state), None

        if maximizing_player:
            max_eval = float('-inf')
            best_action = None
            for action in self.get_actions(game_state, 'boss'):
                new_state = self.simulate_action(game_state, 'boss', action)
                eval_val, _ = self.minimax(new_state, depth - 1, alpha, beta, False)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_action = action
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break # Pruning
            return max_eval, best_action
        else:
            min_eval = float('inf')
            best_action = None
            for action in self.get_actions(game_state, 'player'):
                new_state = self.simulate_action(game_state, 'player', action)
                eval_val, _ = self.minimax(new_state, depth - 1, alpha, beta, True)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_action = action
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break # Pruning
            return min_eval, best_action

    def evaluate(self, state):
        # Heuristic implementation from constants.py
        score = 0
        boss_pos = state['boss_pos']
        player_pos = state['player_pos']
        
        dist = abs(boss_pos[0] - player_pos[0]) + abs(boss_pos[1] - player_pos[1])
        if dist <= 3:
            score += BOSS_HEURISTIC['player_within_3_tiles']
            
        if self._has_los(state['grid'], boss_pos, player_pos):
            score += BOSS_HEURISTIC['player_in_line_of_sight']
            
        # ... other factors
        score += (state['player_max_hp'] - state['player_hp']) * BOSS_HEURISTIC['player_hp_missing_per_hp']
        score += (state['boss_max_hp'] - state['boss_hp']) * BOSS_HEURISTIC['boss_hp_missing_per_hp']
        
        return score

    def _has_los(self, grid, pos1, pos2):
        # Simplified LOS check
        return pos1[0] == pos2[0] or pos1[1] == pos2[1]

    def get_actions(self, state, agent):
        # Cardinal moves + Shoot
        return [(0, 1), (0, -1), (1, 0), (-1, 0), "shoot"]

    def simulate_action(self, state, agent, action):
        # Deep copy state and update
        # This is a simplified simulation for the agent
        new_state = state.copy()
        if action == "shoot":
            pass # Handle shot impact
        else:
            if agent == 'boss':
                new_state['boss_pos'] = (state['boss_pos'][0] + action[0], state['boss_pos'][1] + action[1])
            else:
                new_state['player_pos'] = (state['player_pos'][0] + action[0], state['player_pos'][1] + action[1])
        return new_state
