import sys, random, asyncio
import pygame as pg
from pygame.math import Vector2


class Fruit:
    def __init__(self) -> None:
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pg.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pg.draw.rect(screen, (233,122,44), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5,9), Vector2(4,9), Vector2(4,9)]
        self.direction = Vector2(1,0)

    def draw_snake(self):
        for block in self.body:
            snake_rect = pg.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pg.draw.rect(screen, (133,122,233), snake_rect)
            
    def add_block(self):
        body_copy = self.body[:]
        head = body_copy[0] + self.direction
        body_copy.insert(0, head)
        self.body = body_copy[:]

    def move_snake(self):
        body_copy = self.body[:-1]  # copy all blocks except the last block
        head = body_copy[0] + self.direction
        body_copy.insert(0, head)
        self.body = body_copy[:]
        # check if the snake is outside of the screen
        if head[0] > cell_number -1:
            head[0] = 0
        if head[0] < 0:
            head[0] = cell_number -1
        if head[1] > cell_number -1:
            head[1] = 0
        if head[1] < 0:
            head[1] = cell_number -1
        # check if the snake is eating his tail
        for block in snake.body[1:]:
            if block == snake.body[0]:
                pg.quit()
                sys.exit()
        
        
def events(event):
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
    # Check timer, set to 150 milli sec
    if event.type == SCREEN_UPDATE:
         snake.move_snake()
         check_collision()
    # User input
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
            snake.direction = (0, -1)
        if event.key == pg.K_DOWN:
            snake.direction = (0, 1)
        if event.key == pg.K_RIGHT:
            snake.direction = (1, 0)
        if event.key == pg.K_LEFT:
            snake.direction = (-1, 0)
    
def check_collision():
    if fruit.pos == snake.body[0]:
        # add new fruit
        fruit.randomize()
        # Make the snake longer
        snake.add_block()

def draw_elenents():
    snake.draw_snake()
    fruit.draw_fruit()
    

# Global 
pg.init()
cell_size = 40
cell_number = 20
screen = pg.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pg.time.Clock()
fruit = Fruit()
snake = Snake()
SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)
game_running = True

# play mp3-file and loop
pg.mixer.music.set_volume(0.5)
pg.mixer.music.load("BeepBox.ogg")
pg.mixer.music.play(-1)


async def main():
    while game_running:
        for event in pg.event.get():
            events(event)

        screen.fill((156,211,166))    
        draw_elenents()
        pg.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
   asyncio.run( main() )