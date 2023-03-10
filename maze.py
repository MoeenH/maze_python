import random
from PIL import Image, ImageDraw
import argparse
from queue import Queue


class Cell:
    def __init__(self):
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False
        


class Maze:
    
    def __init__(self, width=20, height=20, cell_width=20):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cells = [[Cell() for _ in range(height)] for _ in range(width)]
        self.num_moves_to_reach_goal = 0
        self.num_moves_to_find_shortest_path = 0
        self.num_deadends_found = 0

    def generate(self):
        x, y = random.choice(range(self.width)), random.choice(range(self.height))
        self.cells[x][y].visited = True
        path = [(x, y)]

        while not all(all(c.visited for c in cell) for cell in self.cells):
            x, y = path[len(path) - 1][0], path[len(path) - 1][1]

            good_adj_cells = []
            if self.exists(x, y - 1) and not self.cells[x][y - 1].visited:
                good_adj_cells.append('north')
            if self.exists(x, y + 1) and not self.cells[x][y + 1].visited:
                good_adj_cells.append('south')
            if self.exists(x + 1, y) and not self.cells[x + 1][y].visited:
                good_adj_cells.append('east')
            if self.exists(x - 1, y) and not self.cells[x - 1][y].visited:
                good_adj_cells.append('west')

            if good_adj_cells:
                go = random.choice(good_adj_cells)
                if go == 'north':
                    self.cells[x][y].north = False
                    self.cells[x][y - 1].south = False
                    self.cells[x][y - 1].visited = True
                    path.append((x, y - 1))
                    self.num_moves_to_find_shortest_path += 1
                if go == 'south':
                    self.cells[x][y].south = False
                    self.cells[x][y + 1].north = False
                    self.cells[x][y + 1].visited = True
                    path.append((x, y + 1))
                    self.num_moves_to_find_shortest_path += 1
                if go == 'east':
                    self.cells[x][y].east = False
                    self.cells[x + 1][y].west = False
                    self.cells[x + 1][y].visited = True
                    path.append((x + 1, y))
                    self.num_moves_to_find_shortest_path += 1
                if go == 'west':
                    self.cells[x][y].west = False
                    self.cells[x - 1][y].east = False
                    self.cells[x - 1][y].visited = True
                    path.append((x - 1, y))
                    self.num_moves_to_find_shortest_path += 1
            else:
                path.pop()
                self.num_deadends_found += 1
        self.num_moves_to_reach_goal = len(path) - 1

    def exists(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return True

    def get_direction(self, direction, x, y):
        if direction == 'north':
            return x, y - 1
        if direction == 'south':
            return x, y + 1
        if direction == 'east':
            return x + 1, y
        if direction == 'west':
            return x - 1, y
            
    def draw(self,path, start=None,goal=None):
        canvas_width, canvas_height = self.cell_width * self.width, self.cell_width * self.height
        im = Image.new('RGB', (canvas_width, canvas_height))
        draw = ImageDraw.Draw(im)

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y].north:
                    draw.line(
                        (x * self.cell_width, y * self.cell_width, (x + 1) * self.cell_width, y * self.cell_width))
                if self.cells[x][y].south:
                    draw.line((x * self.cell_width, (y + 1) * self.cell_width, (x + 1) * self.cell_width,
                               (y + 1) * self.cell_width))
                if self.cells[x][y].east:
                    draw.line(((x + 1) * self.cell_width, y * self.cell_width, (x + 1) * self.cell_width,
                               (y + 1) * self.cell_width))
                if self.cells[x][y].west:
                    draw.line(
                        (x * self.cell_width, y * self.cell_width, x * self.cell_width, (y + 1) * self.cell_width))
       
        if path is not None:
            print(f'Path from {start} to {goal}: {path}')
            for point in path:
                self.drawRect(draw, point, 'blue')
        else:
            print(f'No path found from {start} to {goal}')
        
        
        if start is not None:
            self.drawRect(draw,start,"red")
        if goal is not None:
            self.drawRect(draw,goal,"green")
            
        
        
        im.show()
        
    def drawRect(self,draw,point,color="red"):
        x,y = point
        shape = [(x*self.cell_width + 2, y*self.cell_width + 2), ((x+1)*self.cell_width - 2, (y+1)*self.cell_width - 2)]
        draw.rectangle(shape, fill = color)

    def solve_bfs(self, start, goal):
        
        visited = {}
        movebfs = 0
        
        for x in range(self.width):
            for y in range(self.height):
                visited[(x, y)] = False

        
        q = Queue()
        q.put(start)
        visited[start] = True

        parent = {}
        parent[start] = None

        while not q.empty():
            curr = q.get()

            if curr == goal:
                path = []
                while curr is not None:
                    path.append(curr)
                
                    curr = parent[curr]
                return path[::-1]

            for direction in ['north', 'south', 'east', 'west']:
                neighbor = self.get_direction(direction, *curr)
                if self.exists(*neighbor) and not visited[neighbor] and not self.cells[curr[0]][curr[1]].__dict__[direction]:
                    q.put(neighbor)
                    visited[neighbor] = True
                    parent[neighbor] = curr
        
        return None

    def solve_dfs(self, start, goal):
        stack = [start]
        visited1 = set()
        parent1 = {}
        movesdfs= 0
        

        while stack:
            current = stack.pop()
            movesdfs=+1
        

            if current == goal:
                path = [current]
                while current != start:
                    current = parent1[current]
                    path.append(current)
                path.reverse()
                return path

            visited1.add(current)
            x, y = current
            for direction in ['north', 'south', 'east', 'west']:
                nx, ny = self.get_direction(direction, x, y)
                if self.exists(nx, ny) and not self.cells[x][y].__dict__[direction] and (nx, ny) not in visited1:
                    parent1[(nx, ny)] = current
                    stack.append((nx, ny))
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-width',type=int)
    parser.add_argument('-height',type=int)
    parser.add_argument('-start', nargs='+', type=int)
    parser.add_argument('-goal', nargs='+', type=int)
    args = parser.parse_args()

    maze = Maze(width=args.width, height=args.height)
    maze.generate()

    start = tuple(args.start) if args.start else (0, 0)
    goal = tuple(args.goal) if args.goal else (maze.width-1, maze.height-1)

    path = maze.solve_bfs(start, goal)
    maze.draw(path,start,goal)

    
    # DFS 
   

    start = (0, 0)
    goal = (args.width - 1, args.height - 1)
    path = maze.solve_dfs(start, goal)
    maze.draw(path, start=start, goal=goal)

    print("number of moves to reach goal",maze.num_moves_to_reach_goal)
    print("number of deadends",maze.num_deadends_found)
    print("number of moves to find shortest path",maze.num_moves_to_find_shortest_path)

   
   
    # if path is not None:
    #     print(f'Path from {start} to {goal}: {path}')
    #     maze.draw(start, goal)
    #     for point in path:
    #         maze.drawRect(maze.draw, point, 'blue')
    # else:
    #     print(f'No path found from {start} to {goal}')
    #     maze.draw(start, goal)

