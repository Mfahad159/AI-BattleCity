# AlphaBeta-Armor: Battle City AI Engine

An AI-intensive recreation of the classic **Battle City (Tank 1990)** developed in Python. This project serves as a comprehensive implementation of core AI concepts, ranging from Constraint Satisfaction Problems (CSP) for map generation to Adversarial Search for strategic boss battles.

---

## 🎮 Game Overview

The game is built on a strict **26×26 tile grid matrix** where every object — tanks, bullets, and walls — occupies a specific cell. The core objective is to defend the **Eagle (Base)** at tile `(12, 24)` while eliminating a pool of **20 enemy tanks** across three challenging levels.

---

## 🧠 AI Architecture

This project is divided into three primary modules, each mapping to a specific syllabus area of Artificial Intelligence:

### Module A: CSP Map Generator

Every level features a fresh, randomly generated map using **Backtracking Search with Forward Checking**.

- **Variables:** 676 individual tiles (26×26)
- **Domain:** `{Empty, Brick, Steel, Water, Forest, Eagle}`
- **Key Constraints:**
  - **Base Safety:** The Eagle must be protected by a ring of walls
  - **Reachability:** A valid BFS path must exist from every spawn point to the Eagle
  - **Density:** Wall types cannot exceed 40% of the total map area

---

### Module B: Search & Agent Behaviors

We implement three distinct agent architectures, each utilizing a unique search algorithm:

| Agent | Search Algorithm | Behavior |
|---|---|---|
| Basic Tank | BFS | Simple Reflex |
| Fast Tank | Greedy Best-First | Goal-Based |
| Armor Tank | A\* | Model-Based Reflex |

1. **Basic Tank (Simple Reflex):** Uses **Breadth-First Search (BFS)** for shortest-hop navigation. Ignores costs and seeks the most direct open route.

2. **Fast Tank (Goal-Based):** Employs **Greedy Best-First Search** based on Manhattan distance to the Eagle. Fast but susceptible to local minima.

3. **Armor Tank (Model-Based Reflex):** Utilizes **A\*** with a cost-aware heuristic (`Brick=3`, `Empty=1`). Strategically drills through walls if it's more efficient than detouring. Also maintains an internal `hitCount` state to trigger a **"Retreat to Cover"** behavior after 3 hits.

---

### Module C: Adversarial Search (The Boss)

The final level introduces the **Tank Commander**, an adversarial agent using **Minimax with Alpha-Beta Pruning**.

- **Dynamic Depth:** Search depth increases from `2` to `4` as the Boss's HP decreases
- **Evaluation Heuristic:** Scores are based on line-of-sight, proximity to the player, and available cover
- **Performance:** Alpha-Beta pruning provides a **~25× speedup**, enabling real-time decision-making at depth 4

---

## ⚙️ Technical Specifications

| Property | Detail |
|---|---|
| Language | Python |
| Environment | 26×26 Matrix |
| Game Loop | 10-step sequence |
| Dynamic Environments | Brick walls are destructible; AI agents re-validate paths mid-game |

**Game Loop Sequence:**
```
Input → Agent Decisions → Move → Shoot → Bullet Update →
Collision Detection → State Update → Spawn Check → Render → Win/Lose Check
```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd alphabeta-armor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

---

---

## 📈 Development Progress

- [x] **Phase 1: Foundation & Project Structure** (Completed)
- [x] **Phase 2: Movement, Shooting & Player Control** (Completed)
- [x] **Phase 3: Module A - CSP Map Generator** (Completed)
- [x] **Phase 4: Module B - Search Algorithms & Enemy Agents** (Completed)
- [ ] **Phase 5: Module C - Adversarial Search (Boss Level)**
- [ ] **Phase 6: Visual Polish, Effects & UI**
- [ ] **Phase 7: Documentation & Final Delivery**

---

## 📊 Performance Analysis

The project includes a report analyzing the efficiency of the search algorithms, including a comparison of nodes evaluated **with and without Alpha-Beta pruning** in the Boss level.
