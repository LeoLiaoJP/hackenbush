from collections import defaultdict

class GreenHackenbush:
    def __init__(self):
        self.graph = defaultdict(list)
        self.ground = set()

    def add_edge(self, start, end):
        self.graph[start].append(end)

    def remove_edge(self, start, end):
        if start in self.graph and end in self.graph[start]:
            self.graph[start].remove(end)

            # Check if there is a path connected to the ground after removing the edge
            self.check_reachable()

    def add_ground(self, vertex):
        self.ground.add(vertex)

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]
        if vertex in self.ground:
            self.ground.remove(vertex)

    def is_vertex_green(self, vertex):
        return vertex in self.graph

    def is_vertex_on_ground(self, vertex):
        return vertex in self.ground

    def is_reachable(self, vertex):
        if self.is_vertex_on_ground(vertex):
            return True

        visited = set()

        def dfs(v):
            visited.add(v)
            if self.is_vertex_on_ground(v):
                return True
            for neighbor in self.graph[v]:
                if neighbor not in visited and dfs(neighbor):
                    return True
            return False

        return dfs(vertex)

    def check_reachable(self):
        reachable = set()

        def dfs(v):
            reachable.add(v)
            for neighbor in self.graph[v]:
                if neighbor not in reachable:
                    dfs(neighbor)

        for vertex in self.ground:
            dfs(vertex)

        for vertex in list(self.graph.keys()):
            if vertex not in reachable:
                self.remove_vertex(vertex)

    def is_game_over(self):
        return len(self.graph) == 0

    def print_graph(self):
        for vertex, edges in self.graph.items():
            for end in edges:
                print(vertex, "->", end)


game = GreenHackenbush()

game.add_edge('A', 'B')
game.add_edge('B', 'C')
game.add_edge('C', 'D')
game.add_edge('D', 'E')
game.add_edge('E', 'F')

game.add_ground('A')

player = 1
while True:
    print("Current Graph:")
    game.print_graph()

    print("Current Ground:")
    for vertex in game.ground:
        print(vertex)

    if player == 1:
        current_player = 'Player 1'
    else:
        current_player = 'Player 2'

    print(current_player + "'s turn:")
    start = input("Enter the starting vertex of the edge to remove: ")
    end = input("Enter the ending vertex of the edge to remove: ")

    if start == 'A' and end == 'B':
        game.remove_edge(start, end)
        print("Current Graph:")
        game.print_graph()
        print(current_player + " wins!")
        break

    game.remove_edge(start, end)


    if game.is_game_over():
        print("Current Graph:")
        game.print_graph()
        print(current_player + " wins!")
        break

    if not game.graph:
        print("Current Graph:")
        game.print_graph()
        break

    player = 2 if player == 1 else 1
