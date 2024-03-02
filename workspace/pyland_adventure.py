from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector

class Player(Image):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def jump(self):
        if self.pos[1] == 100:  # Simple condition to prevent mid-air jumps
            self.velocity_y = 15  # Adjust for desired jump strength

class GameWindow(Widget):
    player = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.velocity_x = -10
        elif keycode[1] == 'right':
            self.player.velocity_x = 10
        elif keycode[1] == 'spacebar':
            self.player.jump()
        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in ('left', 'right'):
            self.player.velocity_x = 0
        return True

    def update(self, dt):
        self.player.move()
        # Simple gravity effect
        if self.player.pos[1] > 100:  # Assuming 100 is ground level
            self.player.velocity_y -= 1  # Adjust for desired gravity strength
        else:
            self.player.velocity_y = 0
            self.player.pos[1] = 100  # Reset to ground level

class PyLandAdventureApp(App):
    def build(self):
        game = GameWindow()
        game.player = Player(source='py_character.png', size=(50, 50), pos=(100, 100))
        game.add_widget(game.player)
        return game

if __name__ == '__main__':
    PyLandAdventureApp().run()