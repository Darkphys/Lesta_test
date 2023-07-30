import pytest
from engine_2d import Engine2D, Circle, Triangle, Rectangle


# Тестирование добавления круга
def test_add_circle():
    engine = Engine2D(800, 600)
    engine.add_circle(100, 100, 30)
    assert len(engine.canvas) == 1
    assert isinstance(engine.canvas[0], Circle)


# Тестирование добавления треугольника
def test_add_triangle():
    engine = Engine2D(800, 600)
    engine.add_triangle(200, 200, 250, 250, 300, 200)
    assert len(engine.canvas) == 1
    assert isinstance(engine.canvas[0], Triangle)


# Тестирование добавления прямоугольника
def test_add_rectangle():
    engine = Engine2D(800, 600)
    engine.add_rectangle(400, 150, 50, 80)
    assert len(engine.canvas) == 1
    assert isinstance(engine.canvas[0], Rectangle)


# Тестирование установки цвета
def test_set_color():
    engine = Engine2D(800, 600)
    color = (255, 0, 0)  # Красный
    engine.set_color(color)
    assert engine.current_color == color


# Тестирование метода check_rectangle_collision
def test_check_rectangle_collision():
    engine = Engine2D(800, 600)
    assert engine.check_rectangle_collision(0, 0, 50, 50, 25, 25, 75, 75)  # Ожидаем столкновение
    assert not engine.check_rectangle_collision(0, 0, 50, 50, 51, 51, 100, 100)  # Ожидаем нестолкновение


# Тестирование метода check_all_collisions
def test_check_all_collisions():
    engine = Engine2D(800, 600)
    assert engine.check_all_collisions(400, 300, 200, 300, 200, 500, 400, 500, 200, 100, 100, 600, 400)  # Ожидаем столкновение
    assert not engine.check_all_collisions(100, 100, 30, 700, 500, 750, 550, 750, 500, 600, 100, 50, 50)  # Ожидаем нестолкновение


# Тестирование метода draw
def test_draw():
    engine = Engine2D(800, 600)
    engine.add_circle(100, 100, 30)
    engine.add_triangle(200, 200, 250, 250, 300, 200)
    engine.add_rectangle(400, 150, 50, 80)
    try:
        engine.draw()
    except Exception as e:
        assert False, f"Метод draw вызвал ошибку: {e}"
    else:
        assert True


# Тестирование очистки холста
def test_clear_canvas():
    engine = Engine2D(800, 600)
    engine.add_circle(100, 100, 30)
    engine.add_triangle(200, 200, 250, 250, 300, 200)
    engine.add_rectangle(400, 150, 50, 80)
    assert len(engine.canvas) > 0  # Проверяем, что холст не пустой перед очисткой

    engine.clear_canvas()
    assert len(engine.canvas) == 0  # Ожидаем, что холст будет пустым после очистки


# При необходимости раскомментировать
# if __name__ == "__main__":
#     pytest.main([__file__])
