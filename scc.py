# coding: utf-8

import numpy  # numpy wird zum Einlesen der CSV-Datei verwendet


# Lädt die CSV-Datei `filename` als Adjazenzmatrix ein
def load_adj_matrix(filename):
    with open(filename) as csv:
        return numpy.loadtxt(csv, delimiter=',')


# Tiefensuche auf dem durch die Adjazenzmatrix `adj_matrix` gegebenen Graphen.
# Gibt die besuchten Knoten in absteigender finish-Reihenfolge zurück
def dfs(adj_matrix):
    visited = [False] * len(adj_matrix)
    finished = [False] * len(adj_matrix)
    finish_order = []

    for u in range(len(adj_matrix)):
        if not visited[u]:
            dfs_visit(adj_matrix, u, visited, finished, finish_order)

    finish_order.reverse()
    return finish_order


# Subroutine dfs_visit der Tiefensuche: Besucht einen Knoten im Graphen.
def dfs_visit(adj_matrix, u, visited, finished, finish_order):
    visited[u] = True
    for v in range(len(adj_matrix[u])):
        if (adj_matrix[u][v]) and (not visited[v]):
            dfs_visit(adj_matrix, v, visited, finished, finish_order)
    finished[u] = True
    finish_order.append(u)


# Transponiert einen Graphen (kehrt die Richtungen aller Kanten um) durch Transponieren der Adjazenzmatrix.
def transpose_graph(adj_matrix):
    return adj_matrix.transpose()


# Findet starke Zusammenhangskomponenten im durch die Adjazenzmatrix `adj_matrix` gegebenen Graphen.
def find_sccs(adj_matrix):
    adj_matrix = adj_matrix.copy()  # Lokale Kopie der Matrix wird angelegt, da diese im Algorithmus verändert wird.

    transposed_matrix = transpose_graph(adj_matrix)
    topological_sort = dfs(transposed_matrix)       # *Absteigende* Finish-Zeiten im transponierten Graphen liefern Sinks im Graphen

    components = []  # Liste der gefunden SCCs

    # Solange es noch Einträge in der Liste gibt, wurden noch nicht alle Sinks entfernt, also gibt es noch weitere Komponenten.
    while topological_sort:
        sink = topological_sort[0]  # Source in transposed_matrix <=> Sink in adj_matrix

        visited = [False] * len(adj_matrix)   # wird nicht wirklich verwendet, nur als Argument für dfs_visit nötig.
        finished = [False] * len(adj_matrix)  # wird nicht wirklich verwendet, nur als Argument für dfs_visit nötig.
        visited_nodes = []

        dfs_visit(adj_matrix, sink, visited, finished, visited_nodes)  # Alle besuchten Knoten sind jetzt in `visited_nodes`.


        # Alle Komponenten, die bei diesem dfs_visit besucht wurden (`visited_nodes`), gehören zu der Sink-Komponente.
        components.append(visited_nodes)

        # Alle Knoten der gefundenen SCC werden aus dem Graphen entfernt, so dass die nächste Sink-Komponente gefunden werden kann
        for sink_comp_node in visited_nodes:
            topological_sort.remove(sink_comp_node)  # Entfernen aus der topologischen Ordnung
            for i in range(len(adj_matrix)):         # Entfernen aller Kanten, bei denen Start- oder Zielknoten in der sink component liegt.
                adj_matrix[i][sink_comp_node] = 0
                adj_matrix[sink_comp_node][i] = 0

    return components
    

# Gibt alle Knoten aus, die zwischen zwei verschiednen SCCs des Graphen verlaufen.
def find_edges_between_sccs(adj_matrix, components):
    for i in range(len(adj_matrix)):
        comp_i = next(c for c in components if i in c)

        for j in range(len(adj_matrix)):
            if (adj_matrix[i][j]) and (j not in comp_i):
                print(f'Edge from {i} to {j}!')


def main():
    adj_matrix = load_adj_matrix('./big_graph.csv')
    components = find_sccs(adj_matrix)
    print('\n\n'.join(str(x) for x in components) + '\n\n')  # Ausgabe der gefundenen SCCs

    # Hiermit lassen sich alle Kanten finden, die zwischen zwei verschiednen SCCs verlaufen:
    # find_edges_between_sccs(adj_matrix, components)
                

# Ausführen der main-Funktion, wenn das Skript mit `python3 scc.py` ausgeführt wird.
if __name__ == '__main__':
    main()