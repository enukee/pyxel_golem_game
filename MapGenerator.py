import random


class MapGenerator:
    TEST_MATRIX = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                   [2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2],
                   [3, 1, 4, 0, 1, 0, 1, 0, 1, 1, 1],
                   [2, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0],
                   [2, 0, 2, 0, 1, 1, 2, 0, 3, 1, 1],
                   [2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2],
                   [2, 0, 3, 1, 1, 0, 3, 1, 4, 0, 2],
                   [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
                   [3, 1, 1, 1, 1, 1, 1, 0, 3, 1, 1]]

    @staticmethod
    def generateMap(width: int, height: int):
        def create_maze(width, height):
            # Инициализация матрицы нулями (стенами)
            maze = [[0 for _ in range(width)] for _ in range(height)]

            # Функция для проверки, находится ли клетка в пределах матрицы
            def in_bounds(x, y):
                return 0 <= x < width and 0 <= y < height

                # Функция для рекурсивного создания лабиринта
            def carve_passages_from(x, y):
                maze[y][x] = 1
                directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
                random.shuffle(directions)

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if in_bounds(nx, ny) and maze[ny][nx] == 0:
                        maze[y + dy // 2][x + dx // 2] = 1
                        carve_passages_from(nx, ny)

                        # Начальная точка (единица)

            start_x, start_y = random.randint(0, width // 2) * 2, random.randint(0, height // 2) * 2
            carve_passages_from(start_x, start_y)

            return maze

        matrix = create_maze(width, height)

        # Изменение типа элементов карты
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 1:
                    if i != 0 and j != len(matrix) - 1 and matrix[i - 1][j] != 0 and matrix[i][j + 1] != 0:
                        matrix[i][j] = 3
                    elif i != 0 and i != len(matrix) - 1 and matrix[i - 1][j] != 0 and matrix[i + 1][j] != 0:
                        matrix[i][j] = 2
                    elif j != 0 and i != len(matrix) - 1 and j != len(matrix) - 1 and matrix[i][j - 1] != 0 and \
                            matrix[i + 1][j] != 0 and matrix[i][j + 1] == 0:
                        matrix[i][j] = 4

        return matrix
