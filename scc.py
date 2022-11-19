import numpy


def load_adj_matrix(filename):
    with open(filename) as csv:
        return numpy.loadtxt(csv, delimiter=',')


def dfs(adj_matrix):
    visited = [False] * len(adj_matrix)
    finished = [False] * len(adj_matrix)
    finish_order = []

    for u in range(len(adj_matrix)):
        if not visited[u]:
            dfs_visit(adj_matrix, u, visited, finished, finish_order)

    finish_order.reverse()
    return finish_order


def dfs_visit(adj_matrix, u, visited, finished, finish_order):
    visited[u] = True
    for v in range(len(adj_matrix[u])):
        if (adj_matrix[u][v]) and (not visited[v]):
            dfs_visit(adj_matrix, v, visited, finished, finish_order)
    finished[u] = True
    finish_order.append(u)


def transpose_graph(adj_matrix):
    return adj_matrix.transpose()


def find_sccs(adj_matrix):
    adj_matrix = adj_matrix.copy()

    transposed_matrix = transpose_graph(adj_matrix)
    topological_sort = dfs(transposed_matrix)  # *Absteigende* Finish-Zeiten

    components = []

    while topological_sort:
        sink = topological_sort[0]  # Source in transposed_matrix <=> Sink in adj_matrix

        visited = [False] * len(adj_matrix)   # werden nicht wirklich benötigt
        finished = [False] * len(adj_matrix)  # werden nicht wirklich benötigt
        finish_order = []

        dfs_visit(adj_matrix, sink, visited, finished, finish_order)


        # Alle Komponenten, die bei diesem dfs_visit besucht wurden (finish_order) gehören zu der Sink-Komponente
        components.append(finish_order)

        for sink_comp_node in finish_order:
            topological_sort.remove(sink_comp_node)
            for i in range(len(adj_matrix)):
                adj_matrix[i][sink_comp_node] = 0
                adj_matrix[sink_comp_node][i] = 0

    return components
    


def main():
    adj_matrix = load_adj_matrix('./big_graph.csv')
    components = find_sccs(adj_matrix)

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            comp_i = next(c for c in components if i in c)

            if j not in comp_i:
                if adj_matrix[i][j]:
                    print(f'Edge from {i} to {j}!')
                


if __name__ == '__main__':
    main()