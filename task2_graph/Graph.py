import matplotlib.pyplot as plt
import numpy as np
import random
from faker import Faker

class Graph:
    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("Введите число больше 0")
        self.n = n
        self.matrix = [[0] * n for _ in range(n)]
        self.idx_to_name = []
        self.name_to_idx = {}

    # ---- Вершины и рёбра ----
    def add_vertex(self, name):
        if name in self.name_to_idx:
            return self.name_to_idx[name]
        if len(self.idx_to_name) >= self.n:
            raise ValueError("Достигнут лимит человек")
        idx = len(self.idx_to_name)
        self.name_to_idx[name] = idx
        self.idx_to_name.append(name)
        return idx

    def add_edge(self, a, b):
        ai = self.add_vertex(a)
        bi = self.add_vertex(b)
        if ai == bi:
            raise ValueError("Петли a=a не поддерживаются для простого графа")
        self.matrix[ai][bi] = 1
        self.matrix[bi][ai] = 1
    # -----------------------

    # ---- Быстрое создание графа ----
    def add_edges(self, name, neighbours):
        for nb in neighbours:
            self.add_edge(name, nb)

    # ---- Рандомный граф ----
    def random_graph(self):
        fake = Faker()

        for _ in range(self.n):
            name = fake.name()
            self.add_vertex(name)

        for name in self.idx_to_name:
            num_of_neighbours = random.randint(0, self.n - 1)
            neighbours = set()

            while len(neighbours) < num_of_neighbours:
                nb = random.choice(self.idx_to_name)
                if nb != name:
                    neighbours.add(nb)

            self.add_edges(name, neighbours)

    # ---- Представления графа ----

    # ---- Матрица смежности ----
    def adjacency_matrix(self):
        return self.matrix

    # ---- Список смежности ----
    def adjacency_list(self, use_only_added=True):
        """Возвращает список смежности по индексам вершин.
           Если use_only_added=True, учитывает только реально добавленные вершины."""
        n_used = len(self.idx_to_name) if use_only_added else self.n
        adj = [[] for _ in range(n_used)]
        for i in range(n_used):
            for j in range(n_used):
                if self.matrix[i][j] == 1:
                    adj[i].append(j)
        return adj

    # ---- Проверка "дерево ли?" ----
    def is_tree(self):
        n_used = len(self.idx_to_name)
        if n_used == 0:
            return False
        if n_used == 1:
            return True

        # 1) нет петель и симметрия среди использованных вершин
        for i in range(n_used):
            if self.matrix[i][i] != 0:
                return False
            for j in range(i + 1, n_used):
                if self.matrix[i][j] != self.matrix[j][i]:
                    return False

        # 2) список смежности
        adj = self.adjacency_list(use_only_added=True)

        # 3) DFS с родителем — ищем цикл
        visited = [False] * n_used

        def dfs(u, parent):
            visited[u] = True
            for v in adj[u]:
                if v == parent:
                    continue
                if visited[v]:
                    return True
                if dfs(v, u):
                    return True
            return False

        if dfs(0, -1):
            return False

        # 4) связность: все вершины с ненулевой степенью должны быть посещены
        for i in range(n_used):
            if adj[i] and not visited[i]:
                return False

        # 5) условие для деревьев: m = n-1
        m = sum(self.matrix[i][j] for i in range(n_used) for j in range(i + 1, n_used))
        return m == n_used - 1

    # ---- Отрисовка матрицы смежности ----
    def drow_adjacency_graph(self):

        matrix = np.array(self.matrix)
        fig, ax = plt.subplots()
        im = ax.imshow(matrix, cmap="Blues")

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                text = ax.text(j, i, matrix[i][j],
                            ha="center", va="center")
        ax.set_title("Матрица смежности")
        plt.show()

    # ---- Отрисовка графа ----
    def drow_graph(self):
        names = self.idx_to_name

        angle = [((2*np.pi * i) / self.n) for i in range(self.n)]
        coords = [(np.cos(a), np.sin(a)) for a in angle]

        plt.figure(figsize=(8, 8))
        plt.axis("off")

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matrix[i][j] == 1:
                    x1, y1 = coords[i]
                    x2, y2 = coords[j]
                    plt.plot([x1, x2], [y1, y2], linewidth=1)

        for idx, (x, y) in enumerate(coords):
            plt.plot(x, y, 'o', markersize = 10)
            plt.text(x, y+0.05, names[idx])
            plt.title("Граф")
        plt.show()

    # ---- Поиск друзей для пикника ----
    def _independent_set_by_order(self, order):
        adj = self.adjacency_list(use_only_added=True)
        banned = set()
        picked = []
        for v in order:
            if v in banned:
                continue
            picked.append(v)
            banned.add(v)
            banned.update(adj[v])
        return picked

    def picnic_time(self):
        n_used = len(self.idx_to_name)
        if n_used == 0:
            return 0, []

        best_size = -1
        best_pick = []

        for shift in range(n_used):
            order = [ (shift + i) % n_used for i in range(n_used) ]
            picked = self._independent_set_by_order(order)
            if len(picked) > best_size:
                best_size = len(picked)
                best_pick = picked

        return best_size, [self.idx_to_name[i] for i in best_pick]
