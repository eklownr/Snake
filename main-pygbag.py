import sys, random, asyncio
import pygame as pg
from pygame.math import Vector2


class Fruit:
    def __init__(self) -> None:
        self.randomize()
        self.fruit_index = 0

    def draw_fruit(self):
        fruit_rect = pg.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(fruit_images[self.fruit_index], fruit_rect)
        #pg.draw.rect(screen, (233,122,44), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)
        self.fruit_index = random.randint(0,len(fruit_images) -1)


class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5,9), Vector2(4,9), Vector2(4,9)]
        self.tail = pg.image.load('images/tail_up.png').convert_alpha()
        self.direction = Vector2(1,0)

        self.head_up = pg.image.load('images/head_up.png').convert_alpha()
        self.head_down = pg.image.load('images/head_down.png').convert_alpha()
        self.head_right = pg.image.load('images/head_right.png').convert_alpha()
        self.head_left = pg.image.load('images/head_left.png').convert_alpha()
		
        self.tail_up = pg.image.load('images/tail_up.png').convert_alpha()
        self.tail_down = pg.image.load('images/tail_down.png').convert_alpha()
        self.tail_right = pg.image.load('images/tail_right.png').convert_alpha()
        self.tail_left = pg.image.load('images/tail_left.png').convert_alpha()

        self.body_vertical = pg.image.load('images/body_vertical.png').convert_alpha()
        self.body_horizontal = pg.image.load('images/body_horizontal.png').convert_alpha()

        self.body_tr = pg.image.load('images/body_tr.png').convert_alpha()
        self.body_tl = pg.image.load('images/body_tl.png').convert_alpha()
        self.body_br = pg.image.load('images/body_br.png').convert_alpha()
        self.body_bl = pg.image.load('images/body_bl.png').convert_alpha()
        self.crunch_sound = pg.mixer.Sound('sounds/crunch.wav')


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pg.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

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
                self.eat_my_tail = True
                pg.quit()
                sys.exit()
        

# Global 
pg.init()
cell_size = 40
cell_number = 20
screen = pg.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pg.time.Clock()
SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)

fruit_images = []
for i in range(0,4):
    fruit_image = pg.image.load("images/fruit_" + str(i) + ".png")
    fruit_images.append(fruit_image)

fruit = Fruit()
snake = Snake()

        
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
        if event.key == pg.K_UP and snake.direction[1] != 1:
            snake.direction = (0, -1)
        if event.key == pg.K_DOWN and snake.direction[1] != -1:
            snake.direction = (0, 1)
        if event.key == pg.K_RIGHT and snake.direction[0] != -1:
            snake.direction = (1, 0)
        if event.key == pg.K_LEFT and snake.direction[0] != 1:
            snake.direction = (-1, 0)
    

def check_collision():
    if fruit.pos == snake.body[0]:
        # add new fruit
        fruit.randomize()
        # Make the snake longer
        snake.add_block()


def draw_elements():
    snake.draw_snake()
    fruit.draw_fruit()


# play mp3-file and loop
pg.mixer.music.set_volume(0.3)
pg.mixer.music.load("sounds/BeepBox.ogg")
pg.mixer.music.play(-1)


async def main():
    while True:
        for event in pg.event.get():
            events(event)

        screen.fill((156,211,166))    
        draw_elements()
        pg.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
   asyncio.run( main() )