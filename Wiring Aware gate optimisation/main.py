import math
import random

class Gate:
    def __init__(self, name, width, height, pins):
        self.x = None
        self.y = None
        self.name = name
        self.width = int(width)
        self.height = int(height)
        self.pins = pins

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def pin_positions(self):
        return [(self.x + int(px), self.y + int(py)) for _, (px, py) in self.pins]

def totalCost(gate_positions, wire_connections, gate_dict):
    total_cost = 0
    for connection in wire_connections:
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for pin in connection:
            gate_name, pin_name = pin.split('.')
            gate = gate_dict[gate_name]
            x, y = gate_positions[gate_name]

            pin_number = int(pin_name[1:])  

            pin_x, pin_y = x + int(gate.pins[pin_number - 1][1][0]), y + int(gate.pins[pin_number - 1][1][1])

            min_x = min(min_x, pin_x)
            max_x = max(max_x, pin_x)
            min_y = min(min_y, pin_y)
            max_y = max(max_y, pin_y)

        semi_perimeter = (max_x - min_x) + (max_y - min_y)
        total_cost = total_cost + semi_perimeter

    return total_cost

def group_connected_wires(wires):
    graph = {}
    visited = []
    for pin1, pin2 in wires:
        if pin1 not in graph:
            graph[pin1] = []
        if pin2 not in graph:
            graph[pin2] = []

        graph[pin1].append(pin2)
        graph[pin2].append(pin1)

    wire_connections = []

    def bfs(node):
        queue = [node]
        component = []
        visited.append(node)

        while queue:
            top = queue.pop(0)
            component.append(top)
            for nbr in graph[top]:
                if nbr not in visited:
                    visited.append(nbr)
                    queue.append(nbr)
        return component

    for pin in graph:
        if pin not in visited:
            component = bfs(pin)
            wire_connections.append(component)
    return wire_connections

def read_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    gates = []
    connections = []
    total_width = 0
    total_height = 0

    i = 0
    gates_count = 0
    while i < len(lines):
        if lines[i].startswith('wire'):
            wire = tuple(lines[i].split()[1:])
            connections.append(wire)
            i += 1
        else:
            gate_data = lines[i].split()
            gates_count += 1
            name = gate_data[0] 
            width = gate_data[1]
            height = gate_data[2]
            i += 1
            pins_final = None
            if lines[i].startswith('pins'):
                pin_locations = lines[i].split()[2:]
                pins_final = [(f'p{j+1}', (pin_locations[2 * j], pin_locations[2 * j + 1])) for j in range(len(pin_locations) // 2)]
            i += 1
            total_width=total_width+int(width)
            total_height=total_height+int(height)
            gates.append(Gate(name, width=width, height=height, pins=pins_final))

    return gates, connections, gates_count,total_width,total_height

# Function to check if two gates overlap
def areGatesOverlapping(gate1_name, gate2_name, gate_positions, gate_dict):
    x1, y1 = gate_positions[gate1_name]
    x2, y2 = gate_positions[gate2_name]
    
    gate1 = gate_dict[gate1_name]
    gate2 = gate_dict[gate2_name]
    
    # Check if the two gates overlap
    if (x1 + gate1.width <= x2 or x2 + gate2.width <= x1 or
        y1 + gate1.height <= y2 or y2 + gate2.height <= y1):
        return False  
    return True  

def isLayoutValid(gate_positions, gate_dict):
    gate_names = list(gate_positions.keys())
    flag = False
    # Check every pair of gates for overlap
    for i in range(len(gate_names)):
        for j in range(i + 1, len(gate_names)):
            if areGatesOverlapping(gate_names[i], gate_names[j], gate_positions, gate_dict):
                return False  
    return True  

def simulated_annealing(gates, wire_connections, initial_temp, cooling_rate,width,height, iterations):
    layout_width = width 
    layout_height = height

    gate_positions = {gate.name: (random.randint(0, layout_width - gate.width), random.randint(0, layout_height - gate.height)) for gate in gates}
    
    gate_dict = {gate.name: gate for gate in gates}
    while not isLayoutValid(gate_positions,gate_dict):
            gate_positions = {gate.name: (random.randint(0, layout_width - gate.width), random.randint(0, layout_height - gate.height)) for gate in gates}

    current_cost = totalCost(gate_positions, wire_connections, gate_dict)
    best_solution = gate_positions.copy()
    best_cost = current_cost

    temperature = initial_temp

    for i in range(iterations):
        temp = gate_positions.copy()
        gate_to_move = random.choice(gates)
        new_x = random.randint(0, layout_width - gate_to_move.width)
        new_y = random.randint(0, layout_height - gate_to_move.height)
        temp[gate_to_move.name] = (new_x, new_y)
        if not isLayoutValid(temp, gate_dict):
            continue  

        new_cost = totalCost(temp, wire_connections, gate_dict)

        
        if new_cost < current_cost or random.uniform(0, 1) < math.exp(-(new_cost - current_cost) / temperature):
            gate_positions = temp
            current_cost = new_cost

            if new_cost < best_cost:
                best_solution = temp
                best_cost = new_cost

        temperature *= cooling_rate

        if i % 100 == 0:
            print(f"Iteration {i}: Best cost = {best_cost}")

    return best_solution, best_cost

# Function to write the output to file
def writeOutput(gate_positions, wire_connections, total_wire_length, gates, output_file="output.txt"):
    # Create a dictionary to map gate names to gate objects for reference
    gate_dict = {gate.name: gate for gate in gates}

    
    min_x = min(gate_positions[gate_name][0] for gate_name in gate_positions)
    max_x = max(gate_positions[gate_name][0] + gate_dict[gate_name].width for gate_name in gate_positions)
    min_y = min(gate_positions[gate_name][1] for gate_name in gate_positions)
    max_y = max(gate_positions[gate_name][1] + gate_dict[gate_name].height for gate_name in gate_positions)

    with open(output_file, 'w') as f:
        f.write(f"bounding_box {max_x-min_x} {max_y-min_y}\n")
        
        for gate_name, (x, y) in gate_positions.items():
            x_f=x-min_x
            y_f=y-min_y
            f.write(f"{gate_name} {x_f} {y_f}\n")
        
        f.write(f"wire_length {total_wire_length}\n")

gates, connections, totalGates,width,height = read_input_file('input.txt')
wire_connections = group_connected_wires(connections)

initial_temp = 1000
cooling_rate = 0.99
iter = 10000

best_solution, best_cost = simulated_annealing(gates, wire_connections, initial_temp, cooling_rate,width,height, iter)

writeOutput(best_solution, wire_connections, best_cost, gates)