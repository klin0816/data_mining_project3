from algorithm import hits, pagerank, simrank

import time


def c_time(graphs, method):
    time_list = list()

    if method == 1:
        compute_method = hits
    elif method == 2:
        compute_method = pagerank
    elif method == 3:
        compute_method = simrank

    for idx, graph in enumerate(graphs, 1):
        if method == 3 and idx >= 6:
            break

        start = time.time()
        compute_method(graph)
        end = time.time()

        time_list.append(end - start)
    return time_list


if __name__ == '__main__':
    graphs = list()
    for i in range(1, 8):
        from graph import graph
        filename = 'hw3dataset/graph_{}.txt'.format(i)
        graph = graph()
        graph.read_from_file(filename)
        graphs.append(graph)

    for i, time in enumerate(c_time(graphs, 3)):
        print('Graph {}:'.format(i+1))
        print('Nodes: {}, Edges: {}, Time: {} secs'.format(
            len(graphs[i].nodes()), len(graphs[i].edges()), time
        ))
