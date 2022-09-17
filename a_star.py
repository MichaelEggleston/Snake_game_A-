from queue import PriorityQueue
from search_node import search_node
from heuristics import manhattan_dist
from pygame import time

class a_star():
    def check_goal(self, cur_state, goal_state):
        if cur_state == goal_state:
            return True
        return False

    def get_succ_pos(self, cur_pos, action, snake_size):
        x_pos, y_pos = cur_pos
        if action == 'down':
            y_pos += snake_size
        elif action == 'up':
            y_pos -= snake_size
        elif action == 'right':
            x_pos += snake_size
        elif action == 'left':
            x_pos -= snake_size
        return (x_pos, y_pos)

    def get_succ_snake_body(self, head_pos, snake_body):
        if len(snake_body) != 0:
            succ_snake_body = snake_body.copy()
            succ_snake_body.insert(0, (head_pos))
            succ_snake_body.pop()
            return succ_snake_body
        else:
            return []

    def check_food_visited(self, pos, food_pos):
        if pos == food_pos:
            return True
        return False

    def check_next_to_body(self, cur_dir, pos, body):
        if cur_dir == "up" or cur_dir == "down":
            level_body = [xy for xy in body if xy[1] == pos[1]]
            if len(level_body) > 0:
                return abs(pos[0] - min(level_body)[0] - 10) / 20 
        if cur_dir== "left" or cur_dir == "right":
            level_body = [xy for xy in body if xy[0] == pos[0]]
            if len(level_body) > 0:
                return abs(pos[1] - min(level_body)[1] - 10) / 20
        return 0

    def check_loop(self, cur_pos, body, grid_width, grid_height, snake_size):
        fill_queue = PriorityQueue()
        fill_queue.put(cur_pos)
        #print(cur_pos)
        closed = []
        while not fill_queue.empty():
            #print(closed)
            cur_x, cur_y = fill_queue.get()
            if (cur_x, cur_y) not in closed:
                up = (cur_x, cur_y - 10)
                down = (cur_x, cur_y + 10)
                left = (cur_x - 10, cur_y)
                right = (cur_x + 10, cur_y)
                if up[1] >= 0 and up not in closed and up not in body and up != cur_pos:
                    fill_queue.put(up)
                    
                if down[1] <= grid_height - snake_size and down not in closed and down not in body and down != cur_pos:
                    fill_queue.put(down)
                
                if left[0] >= 0 and left not in closed and left not in body and left != cur_pos:
                    fill_queue.put(left)
                
                if right[0] <= grid_width - snake_size and right not in closed and right not in body and right != cur_pos:
                    fill_queue.put(right)
                
                closed.append((cur_x, cur_y))
        if len(closed) < len(body):
            return True
        return False
    
    def get_succ_node(self, cur_node, goal_state, action, food_pos, grid_width, grid_height, snake_size):
        #print("action", action)
        succ_pos = self.get_succ_pos(cur_node.state[0], action, snake_size)
        if cur_node.state[1]:
            food_visted = True
        else:
            food_visted = self.check_food_visited(succ_pos, food_pos)
        succ_state = [succ_pos, food_visted]
        succ_snake_body = self.get_succ_snake_body(cur_node.state[0], cur_node.snake_body)
        succ_path = cur_node.path.copy()
        succ_path.append(action)
        succ_cost = cur_node.cost + 1
        # if self.check_loop(succ_pos, succ_snake_body, grid_width, grid_height, snake_size):
        #     succ_cost += 300
        #     print("in loop")
        #     #time.wait(2000)
        if food_visted:
            heuristic = manhattan_dist(succ_pos, goal_state[0], snake_size)
        else:
            heuristic = manhattan_dist(succ_pos, food_pos, snake_size) + manhattan_dist(food_pos, goal_state[0], snake_size)
        succ_node = search_node(succ_state, succ_snake_body, action, 10, [], succ_path, succ_cost, heuristic)
        if len(succ_snake_body) > 0:
            succ_node.f_val += self.check_next_to_body(succ_node.dir, succ_pos, succ_snake_body)
        succ_node.get_avail_actions(grid_width, grid_height)
        #print("succ_node_body", succ_node.snake_body)
        return succ_node
        
    def find_path(self, root_node, food_pos, goal_state, grid_width, grid_height, snake_size):
        frontier = PriorityQueue()
        closed = []
        frontier.put(root_node)
        #print(root_node)
        while not frontier.empty():
            #print("not empty")
            cur_node = frontier.get()
            #print("cur_node:", cur_node)
            #time.wait(200)
            for action in cur_node.actions:
                succ = self.get_succ_node(cur_node, goal_state, action, food_pos, grid_width, grid_height, snake_size)
                if succ.state not in closed:
                    frontier.put(succ)
            closed.append(cur_node.state)
            if self.check_goal(cur_node.state, goal_state):
                return cur_node.path
        return []




    