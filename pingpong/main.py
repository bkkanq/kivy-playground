from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use bal.velociy as
    # a shorthand, just like e.. w.pose for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball on step. This
    # will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        # self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
        self.ball.velocity = vel

    def update(self, dt):
        # call ball.move and other stuff
        # we can add an ObjectProperty to the PongGame class, and hook it up to the widget created in the kv rule.
        # Once that’s done, we can easily reference the ball property inside the update method
        # and even make it bounce off the edges:
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        # if (self.ball.x < 0) or (self.ball.right > self.width):
        #     self.ball.velocity_x *= -1

        # went of to a side to score point
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        # We need the move method of our ball to be called regularly.
        # Luckily, Kivy makes this pretty easy by letting us schedule any function we want
        # using the Clock and specifying the interval:

        # This line for example, would cause the update function of the game object to be called
        # once every 60th of a second (60 times per second).
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()

# 1. Add some nicer graphics / images.
# (Hint: check out the source property on the graphics instructions like circle or Rectangle,
# to set an image as the texture.)
#
# 2. Make the game end after a certain score.
# Maybe once a player has 10 points, you can display a large “PLAYER 1 WINS” label and/or add a main menu to start,
# pause and reset the game. (Hint: check out the Button and Label classes, and figure out how to use their add_widget and remove_widget functions to add or remove widgets dynamically.
#
# 3. Make it a 4 player Pong Game. Most tablets have Multi-Touch support,
# so wouldn’t it be cool to have a player on each side and have four people play at the same time?
#
# 4. Fix the simplistic collision check so hitting the ball with an end of the paddle results in a more realistic bounce.