class search_node():
    def __init__(self, state = [], snake_body = [], dir = "none", snake_size = 10, actions = [], path = [], cost = 0, heuristic = 0):
        self.state = state
        if len(snake_body) > 0:
            self.snake_body = snake_body
        else:
            self.snake_body = snake_body[:-1]
        self.dir = dir
        self.snake_size = snake_size
        self.actions = actions
        self.path = path
        self.cost = cost
        self.heuristic = heuristic
        self.f_val = self.cost + self.heuristic

    def get_avail_actions(self, grid_width, grid_height):
        up = (self.state[0][0], self.state[0][1] - 10)
        down = (self.state[0][0], self.state[0][1] + 10)
        left = (self.state[0][0] - 10, self.state[0][1])
        right = (self.state[0][0] + 10, self.state[0][1])

        if self.dir != "down" and self.state[0][1] > 0 and up not in self.snake_body:
            self.actions.append("up")

        if self.dir != "up" and self.state[0][1] < grid_height - self.snake_size and down not in self.snake_body:
            self.actions.append("down")

        if self.dir != "right" and self.state[0][0] > 0 and left not in self.snake_body:
            self.actions.append("left")

        if self.dir != "left" and self.state[0][0] < grid_width - self.snake_size and right not in self.snake_body:
            self.actions.append("right")

    def __eq__(self, other):
        return self.state == other.state and self.path == other.path
    
    def __lt__(self, other):
        return self.f_val < other.f_val 

    def __gt__(self, other):
        return self.f_val > other.f_val

    def __ne__(self, other):
        return self.f_val != other.f_val

    def __le__(self, other):
        return self.f_val <= other.f_val
        
    def __ge__(self, other):
        return self.f_val >= other.f_val

    def __str__(self):
        return f'State: {self.state}, body: {self.snake_body}, dir: {self.dir}, actions: {self.actions}, path: {self.path}, cost: {self.cost}, heuristic: {self.heuristic}, f: {self.f_val}\n'


    