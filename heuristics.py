def manhattan_dist(cur_pos, goal_pos, snake_size):
    return (abs(cur_pos[0] - goal_pos[0]) + abs(cur_pos[1] - goal_pos[1]))/10


if __name__ == "__main__":
    print(manhattan_dist((0,0), (150, 150)) + manhattan_dist((150, 150), (0,0)))