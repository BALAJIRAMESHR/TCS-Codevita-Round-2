from collections import defaultdict, deque


class ConveyorSystem:
    def __init__(self):
        self.reverse_graph = defaultdict(list)
        self.switch_count = defaultdict(int)
        self.current_paths = defaultdict(str)
        self.max_switches = 0
        self.manual_costs = []
        self.paths_to_warehouse = {}

    def add_connection(self, from_node, to_nodes):
        for to_node in to_nodes:
            self.reverse_graph[to_node].append(from_node)

    def find_path_to_warehouse(self, gate, warehouse):
        if gate in self.paths_to_warehouse:
            return self.paths_to_warehouse[gate]

        visited = set()
        queue = deque([(gate, [gate])])
        while queue:
            current, path = queue.popleft()
            if current == warehouse:
                self.paths_to_warehouse[gate] = path[::-1]
                return self.paths_to_warehouse[gate]

            for next_node in self.reverse_graph[current]:
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))
        return None

    def process_item(self, gate, warehouse, item_index):
        path = self.find_path_to_warehouse(gate, warehouse)
        if not path:
            return self.manual_costs[item_index]

        for i in range(len(path) - 1):
            junction = path[i]
            next_node = path[i + 1]

            if self.current_paths[junction] != next_node:
                if self.switch_count[junction] >= self.max_switches:
                    return self.manual_costs[item_index]

                self.current_paths[junction] = next_node
                self.switch_count[junction] += 1

        return 0


def solve():
    # Read input with stripped whitespace
    N = int(input().strip())

    system = ConveyorSystem()
    warehouse = None
    connections = []

    # Read and clean up connection inputs
    for _ in range(N):
        line = input().strip().split()
        connections.append((line[0], line[1:]))
        if line[0] == "warehouse":
            warehouse = line[0]

    # Build connections
    for junction, connected_nodes in connections:
        system.add_connection(junction, connected_nodes)

    # Read and clean up sequence
    sequence = input().strip().split()

    # Read and clean up costs
    system.manual_costs = [int(x) for x in input().strip().split()]

    # Read max switches
    system.max_switches = int(input().strip())

    # Process items and calculate total cost
    total_cost = 0
    for i, gate in enumerate(sequence):
        total_cost += system.process_item(gate, warehouse, i)

    # Print result without any extra spaces or newlines
    print(total_cost, end="")


if __name__ == "__main__":
    solve()
