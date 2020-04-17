from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

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
world.print_rooms()


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


def add_room(room_id, directions, visited_graph):
    if room_id not in visited_graph:
        visited_graph[room_id] = {}
        for direction in directions:
            visited_graph[room_id][direction] = '?'
    return visited_graph


def get_opposite_direction(direction):
    if direction == "n":
        return 's'
    if direction == "s":
        return "n"
    if direction == "e":
        return 'w'
    if direction == 'w':
        return 'e'


def get_possible_exits(room_id, visited_graph):
    possible_exits = []
    for direction in visited_graph[room_id]:
        if visited_graph[room_id][direction] == '?':
            possible_exits.append(direction)
    return possible_exits


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def travel_rooms(player):
    visited_graph = {}
    visited_path = []

    # Enqueue first room
    queue = Queue()
    queue.enqueue(player.current_room.id)
    i = 0
    while queue.size() > 0:
        # Base case if all rooms have been visited
        if len(visited_graph) == len(world.rooms):
            return visited_graph
        # Dequeue the room_id
        room_id = queue.dequeue()

        # Add the current room in visited_graph
        current_room_exits = player.current_room.get_exits()
        visited_graph = add_room(room_id, current_room_exits, visited_graph)

        # If player started moving, start filling in '?'
        # Filling in info of current room in relation to last room
        if len(visited_path) > 0:
            # Grab last room_id player was in
            last_room_id = visited_path[-1]['id']
            # Grab the opposite direction the player traveled
            direction_last_room = get_opposite_direction(
                visited_path[-1]['direction'])
            if visited_graph[room_id][direction_last_room] == '?':
                visited_graph[room_id][direction_last_room] = last_room_id

        # Get exit that has a ?
        choices = get_possible_exits(room_id, visited_graph)

        # If there are possible choices
        if len(choices) > 0:
            # Choose a random direction
            choice = random.choice(choices)
            # Player move
            player.travel(choice)
            # Update the graph of where player went
            visited_graph[room_id][choice] = player.current_room.id
            visited_path.append({
                'id': room_id,
                'direction': choice
            })
        # If there are not exits go backwards
        else:
            # Get the opposite direction player went
            choice = direction_last_room
            # Move player back
            player.travel(choice)
            if visited_path:
                visited_path.pop()
            else:
                traversal_path.append(choice)
                return visited_graph

        # Add move to traversal path
        traversal_path.append(choice)
        # Add current room to queue to continue loop
        queue.enqueue(player.current_room.id)
        i += 1


player = Player(world.starting_room)
travel_rooms(player)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
print(traversal_path)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)


if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


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


# def connect_room(direction, ):
