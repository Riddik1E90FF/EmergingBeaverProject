# maze_mapper.py
# Cell, Agent, and maze-image grid.
# No pre-generated maze — the grid grows purely from sensor readings.

import time
import os
from collections import deque


# ─── Direction helpers ────────────────────────────────────────────────────────
DIRS     = [(0, -1), (1, 0), (0, 1), (-1, 0)]   # N, E, S, W
OPPOSITE = [2, 3, 0, 1]                           # index of the reverse direction
DELTA_TO_DIR = {(0, -1): 0, (1, 0): 1, (0, 1): 2, (-1, 0): 3}


class Cell:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.walls    = [True, True, True, True]   # N, E, S, W
        self.visited  = False
        self.is_start  = False
        self.is_target = False


class Agent:
    """Navigates a physical tape maze using sensor readings.

    Attach a SmartCarBridge as agent.smart_car_bridge before calling
    DFS / BFS / find_all_targets.
    """

    def __init__(self):
        self.maze_solution = None
        self._init_grid()

    # ── Grid management ───────────────────────────────────────────────────────

    def _init_grid(self):
        start = Cell(0, 0)
        start.is_start = True
        start.visited  = True
        self.grid   = [[start]]
        self.grid_w = 1
        self.grid_h = 1
        self.img_x  = 0
        self.img_y  = 0
        self.position      = start
        self.maze_solution = None

    def reset(self):
        self._init_grid()

    def _expand(self, direction):
        """Grow the grid by one row/column in the given direction if needed."""
        if direction == 0:          # north
            if self.img_y != 0:
                return
            for col in self.grid:
                col.insert(0, Cell())
            self.grid_h += 1
            self.img_y  += 1
        elif direction == 1:        # east
            if self.img_x != self.grid_w - 1:
                return
            self.grid.append([Cell() for _ in range(self.grid_h)])
            self.grid_w += 1
        elif direction == 2:        # south
            if self.img_y != self.grid_h - 1:
                return
            for col in self.grid:
                col.append(Cell())
            self.grid_h += 1
        elif direction == 3:        # west
            if self.img_x != 0:
                return
            self.grid.insert(0, [Cell() for _ in range(self.grid_h)])
            self.grid_w += 1
            self.img_x  += 1
        # Re-index every cell after reshaping
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                self.grid[x][y].x = x
                self.grid[x][y].y = y

    # ── Sensor / wall helpers ─────────────────────────────────────────────────

    def _set_walls(self, open_directions):
        """Write sensor-derived wall data into the current cell and its neighbors."""
        self.position.walls = [True, True, True, True]
        for d in open_directions:
            self.position.walls[d] = False
        # Propagate known openings to already-existing neighbors
        for di, (dx, dy) in enumerate(DIRS):
            nx, ny = self.img_x + dx, self.img_y + dy
            if 0 <= nx < self.grid_w and 0 <= ny < self.grid_h:
                if not self.position.walls[di]:
                    self.grid[nx][ny].walls[OPPOSITE[di]] = False

    def can_reach_cell(self, target):
        dx, dy = target.x - self.img_x, target.y - self.img_y
        if abs(dx) + abs(dy) != 1:
            return False
        if dx ==  1: return not self.position.walls[1]
        if dx == -1: return not self.position.walls[3]
        if dy ==  1: return not self.position.walls[2]
        if dy == -1: return not self.position.walls[0]
        return False

    def _sense(self, discovered, stack):
        """Read sensors at current cell, update walls, push new neighbors."""
        open_dirs = self.smart_car_bridge.get_open_directions()
        self._set_walls(open_dirs)
        for d in open_dirs:
            dx, dy = DIRS[d]
            self._expand(d)
            neighbor = self.grid[self.img_x + dx][self.img_y + dy]
            if neighbor not in discovered:
                discovered.add(neighbor)
                stack.append(neighbor)
        return open_dirs

    # ── Movement ──────────────────────────────────────────────────────────────

    def move_in_img(self, dx, dy, sleep_time=0.15):
        self.img_x   += dx
        self.img_y   += dy
        self.position = self.grid[self.img_x][self.img_y]
        self.position.visited = True
        os.system('clear')
        self.display()
        time.sleep(sleep_time)

    # ── Search algorithms ─────────────────────────────────────────────────────

    def DFS(self, sleep_time=0.15):
        """Depth-first search: explores the full physical maze."""
        self.reset()
        stack      = []
        discovered = {self.position}
        path       = [self.position]

        self._sense(discovered, stack)

        while stack:
            next_cell = stack.pop()
            if self.img_x != next_cell.x or self.img_y != next_cell.y:
                # Backtrack along path until next_cell is reachable
                while not self.can_reach_cell(next_cell) and len(path) > 1:
                    path.pop()
                    prev = path[-1]
                    self.move_in_img(prev.x - self.img_x,
                                     prev.y - self.img_y,
                                     sleep_time=sleep_time)
                if not self.can_reach_cell(next_cell):
                    continue
                self.move_in_img(next_cell.x - self.img_x,
                                 next_cell.y - self.img_y,
                                 sleep_time=sleep_time)
            path.append(self.position)
            self._sense(discovered, stack)

        os.system('clear')
        self.display()
        print("DFS complete - maze fully mapped!")

    def BFS(self, sleep_time=0.15):
        """Breadth-first search: explores the full physical maze."""
        self.reset()
        queue      = deque([self.position])
        discovered = {self.position}
        explored   = {self.position}

        self._bfs_sense(discovered, queue)

        while queue:
            current = queue.popleft()
            if self.img_x != current.x or self.img_y != current.y:
                nav = self._navigate_to(current, explored)
                if nav is None:
                    continue
                for step in nav[1:]:
                    dx, dy = step.x - self.img_x, step.y - self.img_y
                    self._expand(DELTA_TO_DIR[(dx, dy)])
                    self.move_in_img(dx, dy, sleep_time=sleep_time)
            explored.add(current)
            self._bfs_sense(discovered, queue)

        os.system('clear')
        self.display()
        print("BFS complete - maze fully mapped!")

    def _bfs_sense(self, discovered, queue):
        open_dirs = self.smart_car_bridge.get_open_directions()
        self._set_walls(open_dirs)
        for d in open_dirs:
            dx, dy = DIRS[d]
            self._expand(d)
            neighbor = self.grid[self.img_x + dx][self.img_y + dy]
            if neighbor not in discovered:
                discovered.add(neighbor)
                queue.append(neighbor)

    def _navigate_to(self, goal, explored):
        """BFS through already-explored cells to plan a path to goal."""
        start = self.grid[self.img_x][self.img_y]
        q = deque([start])
        came_from = {start: None}
        while q:
            cell = q.popleft()
            if cell is goal:
                path = []
                while cell is not None:
                    path.append(cell)
                    cell = came_from[cell]
                path.reverse()
                return path
            for di, w in enumerate(cell.walls):
                if w:
                    continue
                dx, dy = DIRS[di]
                nx, ny = cell.x + dx, cell.y + dy
                if not (0 <= nx < self.grid_w and 0 <= ny < self.grid_h):
                    continue
                neighbor = self.grid[nx][ny]
                if neighbor in came_from:
                    continue
                if neighbor is goal or neighbor in explored:
                    came_from[neighbor] = cell
                    q.append(neighbor)
        return None

    def find_all_targets(self, sleep_time=0.15):
        """DFS over the full maze; dead-end cells are automatically marked as targets."""
        self.reset()
        stack      = []
        discovered = {self.position}
        path       = [self.position]
        targets    = []

        open_dirs = self._sense(discovered, stack)
        self._check_dead_end(open_dirs, targets)

        while stack:
            next_cell = stack.pop()
            if self.img_x != next_cell.x or self.img_y != next_cell.y:
                while not self.can_reach_cell(next_cell) and len(path) > 1:
                    path.pop()
                    prev = path[-1]
                    self.move_in_img(prev.x - self.img_x,
                                     prev.y - self.img_y,
                                     sleep_time=sleep_time)
                if not self.can_reach_cell(next_cell):
                    continue
                self.move_in_img(next_cell.x - self.img_x,
                                 next_cell.y - self.img_y,
                                 sleep_time=sleep_time)
            path.append(self.position)
            open_dirs = self._sense(discovered, stack)
            self._check_dead_end(open_dirs, targets)

        os.system('clear')
        self.display()
        print(f"Exploration complete - {len(targets)} dead end(s) found.")
        return targets

    def _check_dead_end(self, open_dirs, targets):
        """Mark the current cell as a target if it is a dead end."""
        came_from_dir = (self.smart_car_bridge.heading + 2) % 4
        sensor_dirs   = [d for d in open_dirs if d != came_from_dir]
        if len(sensor_dirs) == 0 and not self.position.is_start:
            self.position.is_target = True
            targets.append(self.position)

    # ── Display ───────────────────────────────────────────────────────────────

    def display(self, show_solution=False):
        sol = set()
        if show_solution and self.maze_solution:
            sol = {(c.x, c.y) for c in self.maze_solution}

        for y in range(self.grid_h):
            for x in range(self.grid_w):
                print("+---" if self.grid[x][y].walls[0] else "+   ", end="")
            print("+")
            for x in range(self.grid_w):
                wall = "|" if self.grid[x][y].walls[3] else " "
                cell = self.grid[x][y]
                if not show_solution and x == self.img_x and y == self.img_y:
                    ch = "A"
                elif cell.is_start:
                    ch = "O"
                elif cell.is_target:
                    ch = "X"
                elif (x, y) in sol:
                    ch = "■"
                elif not cell.visited:
                    ch = "?"
                else:
                    ch = " "
                print(f"{wall} {ch} ", end="")
            print("|" if self.grid[self.grid_w - 1][y].walls[1] else " ")

        for x in range(self.grid_w):
            print("+---" if self.grid[x][self.grid_h - 1].walls[2] else "+   ", end="")
        print("+")