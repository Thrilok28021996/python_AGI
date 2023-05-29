from queue import PriorityQueue


def astar(start, target):
    # Check if the input strings are of the same length
    if len(start) != len(target):
        raise ValueError("Input strings must be of the same length")

    # Initialize the priority queue with the starting string and its cost
    pq = PriorityQueue()
    pq.put((0, start))

    # Initialize the set of visited strings
    visited = set()

    while not pq.empty():
        # Get the string with the lowest cost from the priority queue
        cost, current = pq.get()

        # Check if we have reached the target string
        if current == target:
            return cost

        # Add the current string to the set of visited strings
        visited.add(current)

        # Generate all possible next strings by swapping adjacent characters
        for i in range(len(current) - 1):
            next_string = current[:i] + current[i + 1] + current[i] + current[i + 2 :]

            # Check if the next string has not been visited before
            if next_string not in visited:
                # Calculate the cost of the next string
                next_cost = cost + 1 + heuristic(next_string, target)

                # Add the next string and its cost to the priority queue
                pq.put((next_cost, next_string))
                print(f"String -> {next_string}")

    # If we have exhausted all possible strings without reaching the target string, return -1
    return -1


def heuristic(current, target):
    # Calculate the number of characters that are in the wrong position in the current string compared to the target string
    return sum([1 for i in range(len(current)) if current[i] != target[i]])


# Test the function with sample inputs
start = "thrilok"
target = "kolirht"
print(astar(start, target))
