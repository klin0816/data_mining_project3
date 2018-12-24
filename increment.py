from algorithm import hits, pagerank, simrank
from graph import graph


if __name__ == '__main__':
    for idx in range(1, 4):
        filename = 'hw3dataset/graph_{}.txt'.format(idx)
        graphs = graph()
        print('graph_{}'.format(idx))
        graphs.read_from_file(filename)
        
        h, a, i = hits(graphs)
        print('original hub =', h['1'])
        print('original authority =', a['1'])
        pr, i = pagerank(graphs)
        print("original pagerank =", pr['1'])

        graphs.add_edge(('1', '1'))
        new_h, new_a, i = hits(graphs)
        print('new hub =', new_h['1'])
        print('new authority =', new_a['1'])
        new_pr, i = pagerank(graphs)
        print("new pagerank =", new_pr['1'])
        
        print('')
