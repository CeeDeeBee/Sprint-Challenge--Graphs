from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def solution():
    # Load world
    world = World()

    # You may uncomment the smaller graphs for development and testing purposes.
    # map_file = "maps/test_line.txt"
    # map_file = "maps/test_cross.txt"
    # map_file = "maps/test_loop.txt"
    # map_file = "maps/test_loop_fork.txt"
    map_file = "maps/main_maze.txt"

    # Loads the map into a dictionary
    room_graph = literal_eval(open(map_file, "r").read())
    world.load_graph(room_graph)

    # Print an ASCII map
    # world.print_rooms()

    player = Player(world.starting_room)

    opp_direction = {"n": "s", "s": "n", "e": "w", "w": "e"}

    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']
    traversal_path = []
    traversal_graph = {}
    traversal_graph[player.current_room.id] = {}
    for direction in player.current_room.get_exits():
        traversal_graph[player.current_room.id][direction] = "?"

    # bfs for backtracking

    def bfs():
        current_room = player.current_room
        q = Queue()
        visited = set()
        # path = [opp_direction[traversal_path[-1]]]
        q.enqueue([player.current_room])

        # print(q.size())
        while q.size() > 0:
            path = q.dequeue()
            current_room = path[-1]
            # print(current_room.id)
            # print(direction)
            # print(visited)
            # print(path)

            if current_room not in visited:
                visited.add(current_room)

                if "?" in traversal_graph[current_room.id].values():
                    # print("path")
                    # print(path)
                    return path[1:]

                # print(current_room.id)
                # print(current_room.get_exits())
                for next_dir in current_room.get_exits():
                    next_room = current_room.get_room_in_direction(next_dir)
                    if next_room not in visited:
                        path_copy = path.copy()
                        path_copy.append(next_room)
                        q.enqueue(path_copy)

    def dfs():
        current_room = player.current_room
        s = Stack()
        visited = set()
        s.push([player.current_room])

        while s.size() > 0:
            path = s.pop()
            current_room = path[-1]

            if current_room not in visited:
                visited.add(current_room)

                if "?" in traversal_graph[current_room.id].values():
                    return path[1:]

                for next_dir in current_room.get_exits():
                    next_room = current_room.get_room_in_direction(next_dir)
                    if next_room not in visited:
                        path_copy = path.copy()
                        path_copy.append(next_room)
                        s.push(path_copy)

    while len(traversal_graph) < 500:
        # print(traversal_path)
        # print(traversal_graph)
        # print(player.current_room.id)
        # world.print_rooms(player.current_room)
        # print(len(traversal_path))
        # input("Press any key to continue")
        if "?" in traversal_graph[player.current_room.id].values():
            possible_dirs = [direction for direction,
                             status in traversal_graph[player.current_room.id].items() if status == "?"]
            move_dir = random.choice(possible_dirs)
            prev_room = player.current_room.id
            player.travel(move_dir)
            traversal_path.append(move_dir)
            traversal_graph[prev_room][move_dir] = player.current_room.id

            if player.current_room.id not in traversal_graph:
                traversal_graph[player.current_room.id] = {}

                for direction in player.current_room.get_exits():
                    traversal_graph[player.current_room.id][direction] = "?"

            traversal_graph[player.current_room.id][opp_direction[move_dir]] = prev_room
        else:
            bfs_path = bfs()
            if not bfs_path:
                break
            # print(bfs_path)
            # prev_room = player.current_room
            # room_to_move_to = prev_room
            for room in bfs_path:
                for direction, room_id in traversal_graph[player.current_room.id].items():
                    if room_id == room.id:
                        player.travel(direction)
                        traversal_path.append(direction)
                        # world.print_rooms(player.current_room)
                        # print(len(traversal_path))
                        # input("Press any key to continue")
                        break

    # TRAVERSAL TEST - DO NOT MODIFY
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        print(
            f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
        print(sorted([room.id for room in visited_rooms]))

    return len(traversal_path)


lowest_solution = float("inf")
moves = solution()
while moves >= 960:
    moves = solution()
    if moves < lowest_solution:
        lowest_solution = moves
    print(lowest_solution)
print(lowest_solution)

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
