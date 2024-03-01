from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.core.window import Window
from random import randint

class Player(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Asteroid(Widget):
    pass

class GameWidget(Widget):
    player = ObjectProperty(None)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_asteroid, 1)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.velocity_x = -4
        elif keycode[1] == 'right':
            self.player.velocity_x = 4
        elif keycode[1] == 'up':
            self.player.velocity_y = 4
        elif keycode[1] == 'down':
            self.player.velocity_y = -4
        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] == 'left' or keycode[1] == 'right':
            self.player.velocity_x = 0
        elif keycode[1] == 'up' or keycode[1] == 'down':
            self.player.velocity_y = 0
        return True

    def spawn_asteroid(self, dt):
        asteroid = Asteroid()
        asteroid.pos = randint(0, self.width), self.height
        self.add_widget(asteroid)

    def update(self, dt):
        self.player.move()
        for asteroid in self.children[:]:
            if isinstance(asteroid, Asteroid):
                asteroid.y -= 2
                if asteroid.y < 0:
                    self.remove_widget(asteroid)
                if self.player.collide_widget(asteroid):
                    self.remove_widget(asteroid)
                    self.score += 1  # Increment score for each asteroid avoided/destroyed

class PySpaceDefenderApp(App):
    def build(self):
        game = GameWidget()
        return game

if __name__ == '__main__':
    PySpaceDefenderApp().run()