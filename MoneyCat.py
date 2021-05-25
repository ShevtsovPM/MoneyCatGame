from superwires import games, color
import random
games.init(screen_width=640, screen_height=480, fps=50)


class Worker(games.Sprite):

    reward = 0

    def __init__(self):
        super().__init__(image=games.load_image('worker.png', transparent=True),
                         x=games.mouse.x,
                         bottom=games.screen.height)

    def update(self):
        self.x = games.mouse.x
        if self.left < 0:
            self.x = 0
        if self.right > games.screen.width:
            self.x = games.screen.width
        self.check_catch()

    def check_catch(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.if_catch()


class Money(games.Sprite):

    def __init__(self, x, y=0):
        self.speed = random.randrange(3, 5)
        super().__init__(image=games.load_image('Money.png', transparent=True),
                         x=x, y=y,
                         dy=self.speed)

    def update(self):
        if self.bottom > games.screen.height:
            self.destroy()
            x = random.randrange(1, games.screen.width)
            new_pay = Money(x)
            games.screen.add(new_pay)

    def if_catch(self):
        Worker.reward += 1
        self.destroy()
        x = random.randrange(1, games.screen.width)
        new_pay = Money(x)
        games.screen.add(new_pay)


class Doc(games.Sprite):

    def __init__(self, x, y=0):
        self.speed = random.randrange(3, 5)
        super().__init__(image=games.load_image('papers.png', transparent=True),
                         x=x, y=y,
                         dy=self.speed)

    def update(self):
        if self.bottom > games.screen.height:
            self.destroy()
            x = random.randrange(1, games.screen.width)
            new_doc = Doc(x)
            games.screen.add(new_doc)

    def if_catch(self):
        won_message = games.Message(value='Game Over',
                                    size=100,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=150,
                                    after_death=games.screen.quit)
        games.screen.add(won_message)


class Score(games.Text):
    def update(self):
        self.value = f'{Worker.reward} $'


def main():
    wall_image = games.load_image('office.jpg', transparent=False)
    games.screen.background = wall_image
    worker = Worker()
    games.screen.add(worker)
    for i in range(2):
        x = random.randrange(1, games.screen.width)
        doc = Doc(x)
        games.screen.add(doc)
    for i in range(2):
        x = random.randrange(1, games.screen.width)
        pay = Money(x)
        games.screen.add(pay)
    reward = Score(value=Worker.reward,
                  size=40,
                  color=color.dark_green,
                  top=5,
                  right=games.screen.width - 20)
    games.screen.add(reward)
    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()


main()