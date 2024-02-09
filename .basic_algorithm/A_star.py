
import matplotlib.pyplot as plt
import numpy as np


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = [start_node]
    closed_list = []

    while open_list:
        current_node = min(open_list, key=lambda x: x.f)
        open_list.remove(current_node)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return (
                path[::-1],
                closed_list,
            )  

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1],
            )
            if not (
                0 <= node_position[0] < len(maze)
                and 0 <= node_position[1] < len(maze[0])
                and maze[node_position[0]][node_position[1]] == 0
            ):
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(
                child.position[1] - end_node.position[1]
            )
            child.f = child.g + child.h

            if any(
                child == open_node and child.g > open_node.g for open_node in open_list
            ):
                continue

            open_list.append(child)


def plot_maze(maze, start, end, path, closed_list):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(maze, cmap="gray")

    # Plot closed list as explored nodes
    for node in closed_list:
        ax.scatter(
            node.position[1],
            node.position[0],
            color="lightblue",
            s=50,
            label="Explored" if node == closed_list[0] else "",
        )
    if path:
        for position in path:
            ax.scatter(
                position[1],
                position[0],
                color="yellow",
                s=100,
                label="Shortest Path" if position == path[0] else "",
            )

    ax.scatter(start[1], start[0], marker="*", color="blue", s=200, label="Start")
    ax.scatter(end[1], end[0], marker="*", color="red", s=200, label="End")

    handles, labels = ax.get_legend_handles_labels()
    unique = [
        (h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]
    ]
    ax.legend(*zip(*unique), loc="best")

    plt.title("A* Pathfinding Visualization")
    plt.show()


if __name__ == "__main__":
    maze = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    end = (4, 4)

    path, closed_list = astar(maze, start, end)
    plot_maze(maze, start, end, path, closed_list)
