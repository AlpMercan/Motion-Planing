import matplotlib.pyplot as plt
import networkx as nx


def dijkstra_visual_with_distances_and_summary(graph, start, target):
    G = nx.Graph()
    for src, dest_info in graph.items():
        for dest, weight in dest_info.items():
            G.add_edge(src, dest, weight=weight)

    pos = nx.spring_layout(G)  
    shortest_distance = {node: float("inf") for node in graph}
    shortest_distance[start] = 0
    predecessor = {}
    unseenNodes = graph.copy()

    plt.figure(figsize=(16, 12))

    def draw_graph(step, distances, final=False, shortest_path=[]):
        plt.clf()
        node_colors = [
            "skyblue" if node != step["current_node"] else "lightgreen"
            for node in G.nodes()
        ]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="black")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels={(u, v): G[u][v]["weight"] for u, v in G.edges()}
        )


        distance_labels = {
            node: f"{dist if dist != float('inf') else '∞'}"
            for node, dist in distances.items()
        }
        for node, (x, y) in pos.items():
            plt.text(
                x,
                y - 0.1,
                s=distance_labels[node],
                bbox=dict(facecolor="white", alpha=0.5),
                horizontalalignment="center",
            )

        if step["path"]:
            path_edges = list(zip(step["path"], step["path"][1:]))
            nx.draw_networkx_edges(
                G, pos, edgelist=path_edges, edge_color="red", width=2
            )

        plt.title(f"Step {step['step_number']}: Processing node {step['current_node']}")

        if final:
            distance = (
                distances[target]
                if distances[target] != float("inf")
                else "Infinity (unreachable)"
            )
            summary_text = f"Finished: Shortest distance from {start} to {target} is {distance}.\nPath: {' -> '.join(shortest_path)}"
            plt.text(
                0.5,
                -0.1,
                summary_text,
                ha="center",
                transform=plt.gca().transAxes,
                fontsize=12,
                bbox=dict(facecolor="white", alpha=0.5),
            )

        plt.pause(1)  

    step_number = 0
    while unseenNodes:
        current_node = min(unseenNodes, key=lambda node: shortest_distance[node])
        draw_graph(
            {"step_number": step_number, "current_node": current_node, "path": []},
            shortest_distance,
        )
        step_number += 1

        for childNode, weight in graph[current_node].items():
            if weight + shortest_distance[current_node] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[current_node]
                predecessor[childNode] = current_node
        unseenNodes.pop(current_node)

    shortest_path = []
    temp_target = target
    while temp_target is not None:
        shortest_path.append(temp_target)
        temp_target = predecessor.get(temp_target)
    shortest_path = shortest_path[::-1]

    
    draw_graph(
        {"step_number": step_number, "current_node": None, "path": []},
        shortest_distance,
        final=True,
        shortest_path=shortest_path,
    )
    plt.show()

    return shortest_distance, shortest_path



if __name__ == "__main__":
    graph = {
        "A": {"B": 4, "C": 2},
        "B": {"A": 4, "C": 5, "D": 10},
        "C": {"A": 2, "B": 5, "D": 3, "E": 3},
        "D": {"B": 10, "C": 3, "E": 4, "F": 11},
        "E": {"C": 3, "D": 4, "F": 8, "G": 2},
        "F": {"D": 11, "E": 8, "G": 5, "H": 1},
        "G": {"E": 2, "F": 5, "H": 3},
        "H": {"F": 1, "G": 3},
    }
    start_node = "A"
    target_node = "H"
    distances, shortest_path = dijkstra_visual_with_distances_and_summary(
        graph, start_node, target_node
    )
    print(f"Shortest distances from node {start_node}: {distances}")
    print(f"Shortest path from {start_node} to {target_node}: {shortest_path}")

