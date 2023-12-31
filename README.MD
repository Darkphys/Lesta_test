# Тестовый проект для Lesta Games

Добро пожаловать! Здесь представлена информация о проекте, его особенностях и инструкции для запуска и тестирования.

## О проекте

Этот проект является *многозадачным приложением*, написанным на языке программирования **Python версии 3.9.8**. Он включает в себя различные компоненты и задачи, предназначенные для развлечения и функционального тестирования.

## Используемые версии

- **Python**: 3.9.8
- **pip**: 23.2.1

## Задачи проекта

### Задача 1: Автотестирование с помощью pytest

В этой задаче реализован **автотест**, использующий библиотеку **pytest** для тестирования таблицы из статьи Википедии. Этот тест обеспечивает проверку корректности данных в таблице и позволяет обнаруживать возможные ошибки или несоответствия.

### Задача 2: ООП

Вторая задача представляет собой интерактивную **игру**, разработанную на 2D-движке библиотеки **Pygame**. В этой игре управление осуществляется *клавиатурой*:

- **"D"**: Удаляет фигуры с холста и рисует новые, со случайными параметрами.
- **"C"**: Меняет цвет фигур случайным образом.
- **"Q"**: Завершает игру.

Также для этой задачи разработаны **юнит тесты**, которые проверяют различные методы класса 2DEngine, обеспечивая стабильность и правильное функционирование.

### Задача 3: Алгоритмы

Третья задача представляет собой визуализацию **алгоритма** поиска пути А*. В этой задаче пользователю предстоит увидеть, как с помощью алгоритма высчитывается кратчайший путь путушествия плота по воде от одной точки моря до другой.

## Инструкции по установке и запуску

1. Клонируйте репозиторий с проектом на свой локальный компьютер.
2. Убедитесь, что у вас установлена **Python версии 3.9.8** и **pip версии 23.2.1**.
3. Установите необходимые зависимости, выполнив команду: `pip install -r requirements.txt`.
4. Запустите **задачу 1** с помощью команды: `pytest 1/test_wiki.py`.
5. Запустите **задачу 2** с помощью команды: `python 2/engine_2d.py`.
6. Запустите юнит-тесты по **задаче 2** с помощью команды `pytest 2/test_engine_2d.py`.
6. Запустите **задачу 3** с помощью команды `python 3/cells.py`!

## Контакты

Если у вас возникли вопросы, проблемы или вы хотите внести свой вклад в проект, пожалуйста, свяжитесь со мной по следующим контактным данным:

- **Email**: pav_dm@mail.ru
- **Telegram**: t.me/niccmac

**Спасибо за внимание!**
