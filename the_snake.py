from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.
class GameObject:

    """
    Базовый класс, от которого наследуются все объекты.
    Содержит общие атрибуты: позиция и цвет.
    """

    def __init__(self, position=None, body_color=None):
        if position is None:
            self.position = (320, 240)
        else:
            self.position = position
    def draw(self, surface):
        pass

class Apple(GameObject):
    apple_color = (255,0,0)
    super().randomize_position
    self.randomaze_position

    def randomaze_position(self):
        max_x = 640 - 20
        max_y = 480 - 20

        x.random.randrage (0, max_x + 1, 20)
        y.random.randrage (0, max_y + 1, 20)
        self.position = (x, y)

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            20,
            20
        )
        pygame.draw.rect(surface, self.body_color, rect)


    def __init__(self, position=None, body_color=None):
        """
        Конструктор базового игрового объекта.
        Аргументы: position (координаты), body_color (цвет).
        """
        if position is None:
            self.position = (320, 240)
        else:
            self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта на экране.
        Аргумент: surface (поверхность, на которой рисуем)
        """
        pass


class Apple(GameObject):
    """
    Класс Apple. Наследуется от GameObject.
    Появляется в случайном месте поля.
    """

    def __init__(self):
        """
        Инициализирует яблоко с красным цветом и случайной позицией.
        """
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает координаты для яблока.
        """
        max_x = 640 - 20
        max_y = 480 - 20

        x = randint(0, max_x // GRID_SIZE) * GRID_SIZE
        y = randint(0, max_y // GRID_SIZE) * GRID_SIZE

        self.position = (x, y)

    def draw(self, surface):
        """
        Отрисовывает яблоко на игровом поле.
        """
        rect = pygame.Rect(
            (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    """
    Класс Snake. Наследуется от GameObject.
    Описывает змейку и её поведение.
    """

    def __init__(self):
        """
        Инициализирует змейку с зелёным цветом, длиной 1 и движением вправо.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """
        Обновляет направление движения змейки.
        """
        if self.next_direction:
            # Запрет на движение в противоположном направлении
            opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
            if self.next_direction != opposite.get(self.direction):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции).
        """
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        # Прохождение сквозь границы
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """
        Отрисовывает змейку на экране и затирает её след.
        """
        # Затираем хвост
        if len(self.positions) > 1:
            tail_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, tail_rect)

        # Отрисовываем сегменты
        for segment in self.positions:
            seg_rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, seg_rect)
            pygame.draw.rect(screen, BORDER_COLOR, seg_rect, 1)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние после столкновения с собой.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT

def main():
    """
    Основная функция, запускающая игровой цикл.
    """
    # Инициализация PyGame:
    pygame.init()
    # Создаём экземпляры классов:
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка: съела ли змейка яблоко?
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()



if __name__ == '__main__':
    main()