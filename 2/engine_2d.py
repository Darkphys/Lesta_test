import pygame
import sys
import random


class Circle:
    # Круг
    def __init__(self, center_x, center_y, radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

    def draw(self):
        print(f"Drawing Circle: ({self.center_x}, {self.center_y}) with radius {self.radius}")


class Triangle:
    # Треугольник
    def __init__(self, x1, y1, x2, y2, x3, y3, color):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3
        self.color = color

    def draw(self):
        print(f"Drawing Triangle: ({self.x1}, {self.y1}), ({self.x2}, {self.y2}), ({self.x3}, {self.y3})")


class Rectangle:
    # Прямоугольник
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        print(f"Drawing Rectangle: ({self.x}, {self.y}) with width {self.width} and height {self.height}")


class Engine2D:
    # Игровой движок
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.canvas = []
        self.current_color = (255, 255, 255)  # Устанавливаем начальный цвет (белый)

    # Проверить пересечение двух прямоугольников на координатной плоскости
    def check_rectangle_collision(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
        s1 = ( ax1>=bx1 and ax1<=bx2 ) or ( ax2>=bx1 and ax2<=bx2 )
        s2 = ( ay1>=by1 and ay1<=by2 ) or ( ay2>=by1 and ay2<=by2 )
        s3 = ( bx1>=ax1 and bx1<=ax2 ) or ( bx2>=ax1 and bx2<=ax2 )
        s4 = ( by1>=ay1 and by1<=ay2 ) or ( by2>=ay1 and by2<=ay2 )

        if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)):
            return True
        
        return False

    # Проверить пересечение прямоугольных хитбоксов всех объектов на холсте
    def check_all_collisions(
            self, 
            center_x, center_y, radius, 
            x1, y1, x2, y2, x3, y3, 
            rect_x1, rect_y1, rect_width, rect_height
        ):
        circle_x1 = center_x - radius
        circle_y1 = center_y - radius
        circle_x2 = center_x + radius
        circle_y2 = center_y + radius

        triangle_x1 = min([x1, x2, x3])
        triangle_y1 = min([y1, y2, y3])
        triangle_x2 = max([x1, x2, x3])
        triangle_y2 = max([y1, y2, y3])

        rect_x2 = rect_x1 + rect_width
        rect_y2 = rect_y1 + rect_height

        if self.check_rectangle_collision(circle_x1, circle_y1, circle_x2, circle_y2, triangle_x1, triangle_y1, triangle_x2, triangle_y2):
            return True

        if self.check_rectangle_collision(triangle_x1, triangle_y1, triangle_x2, triangle_y2, rect_x1, rect_y1, rect_x2, rect_y2):
            return True

        if self.check_rectangle_collision(circle_x1, circle_y1, circle_x2, circle_y2, rect_x1, rect_y1, rect_x2, rect_y2):
            return True

        return False

    # Добавить круг
    def add_circle(self, center_x, center_y, radius):
        circle = Circle(center_x, center_y, radius, self.current_color)
        circle.draw()
        self.canvas.append(circle)

    # Добавить треугольник
    def add_triangle(self, x1, y1, x2, y2, x3, y3):
        triangle = Triangle(x1, y1, x2, y2, x3, y3, self.current_color)
        triangle.draw()
        self.canvas.append(triangle)

    # Добавить прямоугольник
    def add_rectangle(self, x, y, width, height):
        rectangle = Rectangle(x, y, width, height, self.current_color)
        rectangle.draw()
        self.canvas.append(rectangle)

    # Определить цвет для всех фигур
    def set_color(self, color):
        self.current_color = color
        print(f"Color set to RGB {color} for all figures.")

    # Отрисовать фигуры на холсте
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_app()

        # Очищаем экран
        self.screen.fill((0, 0, 0))

        # Отрисовываем примитивы на холсте
        for primitive in self.canvas:
            if isinstance(primitive, Circle):
                pygame.draw.circle(self.screen, self.current_color, (primitive.center_x, primitive.center_y), primitive.radius)
            elif isinstance(primitive, Triangle):
                pygame.draw.polygon(self.screen, self.current_color, [(primitive.x1, primitive.y1), (primitive.x2, primitive.y2), (primitive.x3, primitive.y3)])
            elif isinstance(primitive, Rectangle):
                pygame.draw.rect(self.screen, self.current_color, (primitive.x, primitive.y, primitive.width, primitive.height))

        pygame.display.flip()
        self.clock.tick(60)

    # Удалить все фигуры
    def clear_canvas(self):
        self.canvas = []

    # Завершить работу pygame
    def exit_app(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    engine = Engine2D(800, 600)

    engine.add_circle(center_x=100, center_y=100, radius=30)
    engine.add_triangle(x1=200, y1=200, x2=250, y2=250, x3=300, y3=200)
    engine.add_rectangle(x=400, y=150, width=50, height=80)

    engine.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.exit_app()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    engine.exit_app()
                elif event.key == pygame.K_c:
                    # Генерируем случайный цвет RGB
                    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    engine.set_color(random_color)
                    engine.draw()
                elif event.key == pygame.K_d:
                    # Очищаем холст
                    engine.clear_canvas()
                    # Генерируем фигуры
                    while True:
                        random_circle_x = random.randint(100, 700)
                        random_circle_y = random.randint(100, 500)
                        random_circle_radius = random.randint(20, 90)

                        random_triangle_x1, random_triangle_y1 = random.randint(50, 750), random.randint(50, 550)
                        random_triangle_x2, random_triangle_y2 = random.randint(50, 750), random.randint(50, 550)
                        random_triangle_x3, random_triangle_y3 = random.randint(50, 750), random.randint(50, 550)

                        random_rectangle_x = random.randint(50, 600)
                        random_rectangle_y = random.randint(50, 400)
                        random_rectangle_width = random.randint(20, 190)
                        random_rectangle_height = random.randint(20, 190)

                        if not engine.check_all_collisions(random_circle_x, random_circle_y, random_circle_radius,
                                                       random_triangle_x1, random_triangle_y1, random_triangle_x2, random_triangle_y2, random_triangle_x3, random_triangle_y3,
                                                       random_rectangle_x, random_rectangle_y, random_rectangle_width, random_rectangle_height):
                            break

                    engine.add_circle(center_x=random_circle_x, center_y=random_circle_y, radius=random_circle_radius)
                    engine.add_triangle(random_triangle_x1, random_triangle_y1, random_triangle_x2, random_triangle_y2, random_triangle_x3, random_triangle_y3)
                    engine.add_rectangle(x=random_rectangle_x, y=random_rectangle_y, width=random_rectangle_width, height=random_rectangle_height)

                    engine.draw()
