import random
import heapq
import math


LAND = "@"  # Для обозначения суши
WATER = "~"  # Для обозначения воды
PATH = "X"  # Для отображения пути


# Определяем класс узла графа
class Node:
    def __init__(self, x, y):
        self.x = x  # Координата x узла на карте
        self.y = y  # Координата y узла на карте
        self.g = 0  # Расстояние от начального узла до текущего узла
        self.h = 0  # Примерное расстояние от текущего узла до конечного узла
        self.f = 0  # Сумма g и h
        self.parent = None  # Родительский узел, используется для восстановления пути

    # Переопределяем оператор сравнения для сравнения узлов
    def __lt__(self, other):
        return self.f < other.f

    # Переопределяем оператор равенства для сравнения узлов
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # Мы хэшируем объект на основе его координат (x, y), так как координаты являются уникальными идентификаторами для узлов
        return hash((self.x, self.y))


# Автогенерация карты с указанным процентом суши
def generate_map(m, n, land_percentage, water_symbol, land_symbol):
    total_cells = m * n
    num_land_cells = int(total_cells * land_percentage / 100)
    map_grid = [[water_symbol for _ in range(n)] for _ in range(m)]

    land_cells = random.sample(range(total_cells), num_land_cells)
    for cell in land_cells:
        row = cell // n
        col = cell % n
        map_grid[row][col] = land_symbol

    return map_grid


# Отобразить карту
def display_map(map_grid):
    # Отображение индексов столбцов сверху
    print('   ' + ' '.join(str(i) for i in range(len(map_grid[0]))))
    for i, row in enumerate(map_grid):
        # Отображение индекса строки слева
        print(f'{i:2} ', end='')
        print(' '.join(row))
    

# Проверить, что координаты находятся в пределах карты и на воде
def is_valid_cell(x, y, map_grid, land_symbol):
    m = len(map_grid[0])
    n = len(map_grid)
    if x < 0 or x >= m or y < 0 or y >= n:
        print(f"\nНекорректные координаты, пожалуйста, оставайтесь в пределах заданного поля ({m}, {n})!")
        return False
    
    elif map_grid[y][x] == land_symbol:
        print("\nПлот не может плыть по суше, введите координаты на воде!")
        return False
    
    return True


# Найти кратчайший путь с помощью алгоритма A*
def find_the_shortest_path(start, end, map_grid, land_symbol):
    # Создаем начальный и конечный узлы
    start_node = Node(start[0], start[1])
    end_node = Node(end[0], end[1])

    # Инициализируем очередь с приоритетами
    open_list = []
    heapq.heappush(open_list, start_node)

    # Инициализируем множество посещенных узлов
    closed_set = set()

    # Пока очередь с приоритетами не пуста
    while open_list:
        # Извлекаем узел с наименьшей оценкой f
        current_node = heapq.heappop(open_list)

        # Если текущий узел является конечным
        if current_node == end_node:
            # Восстанавливаем путь от конечного узла до начального
            path_list = []
            while current_node is not None:
                path_list.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path_list[::-1]

        # Добавляем текущий узел в множество посещенных узлов
        closed_set.add(current_node)

        # Получаем соседние узлы (только сверху, справа, снизу и слева)
        neighbors = []
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            # Вычисляем координаты соседнего узла
            x = current_node.x + dx
            y = current_node.y + dy
            # Игнорируем узлы за пределами карты
            if x < 0 or x >= len(map_grid[0]) or y < 0 or y >= len(map_grid):
                continue
            # Игнорируем препятствия
            if map_grid[y][x] == land_symbol:
                continue
            # Создаем новый узел и добавляем его в список соседей
            neighbor = Node(x, y)
            neighbors.append(neighbor)

        # Для каждого соседнего узла
        for neighbor in neighbors:
            # Если соседний узел уже был посещен, пропускаем его
            if neighbor in closed_set:
                continue

            # Вычисляем расстояние от начального узла до соседнего узла
            new_g = current_node.g + 1

            # Если соседний узел уже находится в очереди с приоритетами
            if neighbor in open_list:
                # Если новое расстояние до соседнего узла меньше, чем старое, обновляем значения g, h и f
                if new_g < neighbor.g:
                    neighbor.g = new_g
                    neighbor.h = math.sqrt((end_node.x - neighbor.x) ** 2 + (end_node.y - neighbor.y) ** 2)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node
                    # Обновляем приоритет соседнего узла в очереди с приоритетами
                    heapq.heapify(open_list)
            else:
                # Иначе добавляем соседний узел в очередь с приоритетами и вычисляем значения g, h и f
                neighbor.g = new_g
                neighbor.h = math.sqrt((end_node.x - neighbor.x) ** 2 + (end_node.y - neighbor.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)

    # Если конечный узел недостижим, возвращаем None
    return None


# Отобразить карту с путем плота
def display_map_with_path(map_grid, path_list, path_symbol):
    if path_list is None:
        print("Путь не найден.")
        return

    # Отрисовываем путь на карте
    for x, y in path_list:
        map_grid[y][x] = path_symbol
    display_map(map_grid)


def main():
    # Получение параметров карты
    M = int(input("Введите количество строк M: "))
    N = int(input("Введите количество столбцов N: "))
    land_percentage = 30

    # Генерация карты
    map_grid = generate_map(M, N, land_percentage, WATER, LAND)
    print("\nКарта:")
    display_map(map_grid)
    print()

    # Получение начальных и конечных координат плота
    while True:
        start_x = int(input("Введите координату x для точки A (отсчет с 0): "))
        start_y = int(input("Введите координату y для точки A (отсчет с 0): "))
        if is_valid_cell(start_x, start_y, map_grid, LAND):
            break
    
    print()
    while True:
        end_x = int(input("Введите координату x для точки B (отсчет с 0): "))
        end_y = int(input("Введите координату y для точки B (отсчет с 0): "))
        if is_valid_cell(end_x, end_y, map_grid, LAND):
            break

    # Поиск кратчайшего пути
    start = (start_x, start_y)
    end = (end_x, end_y)
    path_list = find_the_shortest_path(start, end, map_grid, LAND)

    if path_list is None:
        print("\nПуть не найден!")
    else:
        # Вывод кратчайшего пути
        print(f"\nПуть:\n{path_list}")

        # Вывод карты с путем
        print("\nКарта с путем:")
        display_map_with_path(map_grid, path_list, PATH)


if __name__ == "__main__":
    main()
