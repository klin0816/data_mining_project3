from graph import graph
import numpy as np
import matplotlib.pyplot as plt
from pprint import PrettyPrinter


def hits(graph, min_diff=0.01):
    nodes = graph.nodes()
    auth = dict.fromkeys(nodes, 1)
    hub = dict.fromkeys(nodes, 1)
    iteration = 0

    while True:
        iteration += 1
        prev_auth = auth.copy()
        prev_hub = hub.copy()

        for node in nodes:
            auth[node] = sum(prev_hub.get(parent, 0) for parent in graph.parents(node))
            hub[node] = sum(prev_auth.get(child, 0) for child in graph.childrens(node))

        norm_auth = sum(auth.values())
        norm_hub = sum(hub.values())
        auth = {key: val / norm_auth for key, val in auth.items()}
        hub = {key: val / norm_hub for key, val in hub.items()}

        diff = sum((abs(prev_hub[k] - hub[k]) for k in hub)) + sum((abs(prev_auth[k] - auth[k]) for k in auth))
        if diff <= min_diff:
            break

    return auth, hub, iteration


def pagerank(graph, min_diff=0.0001, damping_factor=0.15):
    nodes = graph.nodes()
    pagerank = dict.fromkeys(nodes, 1.0 / len(nodes))
    iteration = 0

    while True:
        iteration += 1
        diff = 0

        for node in nodes:
            rank = (1.0 - damping_factor) / len(nodes)
            for parent in graph.parents(node):
                rank += damping_factor * pagerank[parent] / len(graph.childrens(parent))

            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank

        if diff <= min_diff:
            break

    return pagerank, iteration


def simrank(graph, min_diff=0.01, decay_factor=0.8):
    nodes = graph.nodes()
    sim = np.identity(len(nodes))
    iteration = 0

    while True:
        iteration += 1
        prev_sim = np.copy(sim)

        for idx_u, u in enumerate(nodes):
            for idx_v, v in enumerate(nodes):
                if u is v:
                    continue

                len_up = len(graph.parents(u))
                len_vp = len(graph.parents(v))
                if len_up == 0 or len_vp == 0:
                    sim[idx_u][idx_v] = 0
                else:
                    sum = 0
                    for u_p in graph.parents(u):
                        for v_p in graph.parents(v):
                            sum += prev_sim[nodes.index(u_p)][nodes.index(v_p)]
                    
                    sim[idx_u][idx_v] = (decay_factor / (len_up * len_vp)) * sum

        if np.allclose(sim, prev_sim, atol=min_diff):
            break

    return sim, iteration


if __name__ == '__main__':

    graphs = list()
    for i in range(1, 8):
        from graph import graph
        filename = 'hw3dataset/graph_{}.txt'.format(i)
        graph = graph()
        graph.read_from_file(filename)
        graphs.append(graph)


    for idx, graph in enumerate(graphs, 1):
        filename = './result/hits/graph_{}.txt'.format(idx)
        with open(filename, 'w+') as f:
            pp = PrettyPrinter(indent=4, stream=f)
            f.write('\nGraph {}\n'.format(idx))
            a, h, i = hits(graph)
            f.write('Run {} iterations \nhub:\n'.format(i))
            pp.pprint(h)
            f.write('auth:\n')
            pp.pprint(a)
            print('(hits) graph_{}.txt saved'.format(idx))

    for idx, graph in enumerate(graphs, 1):
        filename = './result/pagerank/graph_{}.txt'.format(idx)
        with open(filename, 'w+') as f:
            pp = PrettyPrinter(indent=4, stream=f)
            f.write('\nGraph {}\n'.format(idx))
            pr, i = pagerank(graph)
            f.write('Run {} iterations \nPage Rank:\n'.format(i))
            pp.pprint(pr)
            print('(pagerank) graph_{}.txt saved'.format(idx))

    for idx, graph in enumerate(graphs, 1):
        if idx == 6:
            break

        filename = './result/simrank/graph_{}.txt'.format(idx)    
        with open(filename, 'w+') as f:
            pp = PrettyPrinter(indent=4, stream=f)
            f.write('\nGraph {}\n'.format(idx))
            s, i = simrank(graph)
            f.write('Run {} iterations \nSimRank:\n'.format(i))
            pp.pprint(s)
            print('(simrank) graph_{}.txt saved'.format(idx))

    print('end')
