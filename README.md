### Algorithm Used: Simulated Annealing
The algorithm uses simulated annealing to optimize the placement of gates while minimizing the
total wire length. It iteratively perturbs the layout, accepting worse solutions with a probability that
decreases over time, allowing it to escape local optima.
## Methods and Attributes Used
Classes:
• Gate: Represents a gate with attributes like name, width, height, and pins.
Methods:
• simulated_annealing(gates, wire_connections, initial_temp, cooling_rate, width, height,
iterations): Implements the simulated annealing algorithm for gate placement optimization.
• totalCost(gate_positions, wire_connections, gate_dict): Calculates the total wire length using
semi-perimeter wire length (HPWL) method.
• isLayoutValid(gate_positions, gate_dict): Checks if the current layout has any overlapping
gates.
• areGatesOverlapping(gate1_name, gate2_name, gate_positions, gate_dict): Determines if
two specific gates overlap.
• group_connected_wires(wires): Groups connected wires using a breadth-first search
approach.
• read_input_file(filename): Reads the input file and parses gate and wire information.
• writeOutput(gate_positions, wire_connections, total_wire_length, gates, output_file): Writes
the optimized layout to an output file.
## Key Variables:
• gate_positions: Dictionary storing the current positions of all gates.
• wire_connections: List of wire connections between gates.
• initial_temp: Initial temperature for simulated annealing (set to 1000).
• cooling_rate: Cooling rate for temperature reduction (set to 0.99).
• iterations: Number of iterations for the simulated annealing process (set to 10000).

# Time Complexity Analysis
Simulated Annealing Loop: O(I * (G^2 + W))
• I: Number of iterations (10000)
• G: Number of gates
• W: Number of wire connections

# Key Operations:

1. Layout validity check (isLayoutValid): O(G^2)
2. Cost calculation (totalCost): O(W * P), where P is the average number of pins per connection
3. Gate movement: O(1)
# Overall Complexity: O(I * (G^2 + W * P))

The algorithm's performance in practice may be better than this worst-case analysis, especially for
well-structured problems where good solutions are found quickly.
# Design Decisions
1. Semi-Perimeter Wire Length (HPWL): Used as a quick approximation for wire length
calculation.
2. Random Gate Movement: In each iteration, a random gate is selected and moved to a new
random position.
3. Temperature Cooling: A simple geometric cooling schedule is used
 (temperature *= cooling_rate).
4. Initial Layout: Randomly placed gates are used as the starting point, ensuring no overlaps.
5. Wire Grouping: Connected wires are grouped to optimize the cost calculation process
