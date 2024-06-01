import time
from collections import deque


class Robot:
    def __init__(self, id, loc, dir, is_dead, coll_loc, coll_time):
        self.ID = id
        self.loc = loc
        self.dir = dir
        self.current_dir = dir
        self.is_dead = is_dead
        self.coll_loc = coll_loc
        self.coll_time = coll_time
        self.pair = -1


class CollisionPair:
    def __init__(self, id1, id2, coll_loc, coll_time):
        self.ID1 = id1
        self.ID2 = id2
        self.coll_loc = coll_loc
        self.coll_time = coll_time


robots = []

e_stack = deque()
o_stack = deque()

collision_pairs = []

num_r = 0

with open('Robots.txt') as file:
    for line_num, line in enumerate(file):

        if line_num == 0:
            x_limit = int(line.strip())

        else:
            num_r += 1

            parts = line.strip().split()
            r_loc, r_dir = int(parts[0]), int(parts[1])
            temp_r = Robot(line_num - 1, r_loc, r_dir, False, -1, -1)
            robots.append(temp_r)


def check_collision(collisionPair):
    if robots[collisionPair.ID1].loc > robots[collisionPair.ID2].loc:
        left_robot_location, left_robot_direction = robots[collisionPair.ID2].loc, robots[collisionPair.ID2].dir
        right_robot_location, right_robot_direction = robots[collisionPair.ID1].loc, robots[collisionPair.ID1].dir

    else:
        left_robot_location, left_robot_direction = robots[collisionPair.ID1].loc, robots[collisionPair.ID1].dir
        right_robot_location, right_robot_direction = robots[collisionPair.ID2].loc, robots[collisionPair.ID2].dir

    if (robots[collisionPair.ID1].loc - robots[collisionPair.ID2].loc) % 2 == 0:
        # CASE 1

        if left_robot_direction == 1 and right_robot_direction == -1:
            hit_point = ((right_robot_location - left_robot_location) / 2) + left_robot_location
            time_of_collision = (right_robot_location - left_robot_location) / 2
            collisionPair.coll_loc = hit_point
            collisionPair.coll_time = time_of_collision

        # CASE 2

        if left_robot_direction == right_robot_direction == -1:
            hit_point = (right_robot_location - left_robot_location) / 2
            time_of_collision = ((right_robot_location - left_robot_location) / 2) + left_robot_location
            collisionPair.coll_loc = hit_point
            collisionPair.coll_time = time_of_collision

        # CASE 3

        if left_robot_direction == right_robot_direction == 1:
            hit_point = ((right_robot_location - left_robot_location) / 2) + x_limit + left_robot_location - right_robot_location
            time_of_collision = x_limit - right_robot_location + (right_robot_location - left_robot_location) / 2
            collisionPair.coll_loc = hit_point
            collisionPair.coll_time = time_of_collision

        # CASE 4

        if left_robot_direction == -1 and right_robot_direction == 1:
            hit_point = x_limit - right_robot_location + (right_robot_location - left_robot_location) / 2
            time_of_collision = ((right_robot_location - left_robot_location) / 2) + x_limit + left_robot_location - right_robot_location
            collisionPair.coll_loc = hit_point
            collisionPair.coll_time = time_of_collision

    else:
        collisionPair.coll_loc = -1
        collisionPair.coll_time = -1


version = int(input("V1 or V2: "))
print("")

if version == 1:

    start_time = time.perf_counter()
    print("")
    for i in range(num_r):
        for j in range(i + 1, num_r):
            temp_coll_pair = CollisionPair(i, j, -1, -1)
            check_collision(temp_coll_pair)
            if temp_coll_pair.coll_time != -1 or temp_coll_pair.coll_loc != -1:
                collision_pairs.append(temp_coll_pair)

    collision_pairs.sort(key=lambda x: x.coll_time)

    for collision_pair in collision_pairs:
        if robots[collision_pair.ID1].is_dead is not True and robots[collision_pair.ID2].is_dead is not True:
            robots[collision_pair.ID1].is_dead = True
            robots[collision_pair.ID2].is_dead = True
            robots[collision_pair.ID1].coll_time = collision_pair.coll_time
            robots[collision_pair.ID2].coll_time = collision_pair.coll_time
            robots[collision_pair.ID1].coll_loc = collision_pair.coll_loc
            robots[collision_pair.ID2].coll_loc = collision_pair.coll_loc

    for i, r in enumerate(robots):
        print(f"Robot {robots[i].ID + 1} Statistics:")
        if robots[i].is_dead is True:
            print(f"Collision location: {robots[i].coll_loc}")
            print(f"Collision time: {robots[i].coll_time}")
            print("")
        else:
            print("No collision")
            print("")
    end_time = time.perf_counter()
    elapsed_time = round(end_time - start_time, 6)

    print(f'Time elapsed: {elapsed_time}')


else:
    robots.sort(key=lambda rob: rob.loc)
    for i, robot in enumerate(robots):
        robot.ID = i
    start_time = time.perf_counter()

    for i, robot in enumerate(robots):
        if robot.loc % 2 == 0:
            stack = e_stack
        else:
            stack = o_stack

        if len(stack) == 0:
            if robot.dir == -1:
                robot.current_dir = 1
            stack.append(robot)
        else:
            top = stack[-1]
            if top.current_dir == 1 and robot.current_dir == -1:
                temp_pair = CollisionPair(top.ID, robot.ID, -1, -1)
                check_collision(temp_pair)

                if temp_pair.coll_loc != -1:
                    top.coll_loc, top.coll_time, top.is_dead, top.pair = temp_pair.coll_loc, temp_pair.coll_time, True, robot.loc
                    robot.coll_loc, robot.coll_time, robot.is_dead, robot.pair = temp_pair.coll_loc, temp_pair.coll_time, True, top.loc
                    stack.pop()
            else:
                stack.append(robot)

    while len(e_stack) > 0:
        rob = e_stack.pop()
        if len(e_stack) > 0:
            rob2 = e_stack.pop()
            temp_pair = CollisionPair(rob.ID, rob2.ID, -1, -1)
            check_collision(temp_pair)
            rob.coll_loc, rob.coll_time, rob.is_dead, rob.pair = temp_pair.coll_loc, temp_pair.coll_time, True, rob2.loc
            rob2.coll_loc, rob2.coll_time, rob2.is_dead, rob2.pair = temp_pair.coll_loc, temp_pair.coll_time, True, rob.loc

    while len(o_stack) > 0:
        rob = o_stack.pop()
        if len(o_stack) > 0:
            rob2 = o_stack.pop()
            temp_pair = CollisionPair(rob.ID, rob2.ID, -1, -1)
            check_collision(temp_pair)
            rob.coll_loc, rob.coll_time, rob.is_dead, rob.pair = temp_pair.coll_loc, temp_pair.coll_time, True, rob2.loc
            rob2.coll_loc, rob2.coll_time, rob2.is_dead, rob2.pair = temp_pair.coll_loc, temp_pair.coll_time, True, rob.loc

    for i, robot in enumerate(robots):
        print(f"Robot at location {robot.loc} Statistics:")
        if robots[i].is_dead is True:
            print(f'Collided with robot at location: {robot.pair}')
            print(f"Collision location: {robots[i].coll_loc}")
            print(f"Collision time: {robots[i].coll_time}")
            print("")
        else:
            print("No collision")
            print("")

    end_time = time.perf_counter()
    elapsed_time = round(end_time - start_time, 6)

    print(f'Time elapsed: {elapsed_time}')
