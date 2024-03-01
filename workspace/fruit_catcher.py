from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.vector import Vector
from random import randint
from kivy.uix.widget import Widget
from kivy.core.window import Window
Window.size = (360, 600)

class Basket(Widget):
    def move(self, touch):
        # Ensure the basket stays within the window bounds
        if touch.x < self.width / 2:
            self.center_x = self.width / 2
        elif touch.x > Window.width - self.width / 2:
            self.center_x = Window.width - self.width / 2
        else:
            self.center_x = touch.x

class FruitCatcherGame(Widget):
    basket = ObjectProperty(None)
    score = NumericProperty(0)
    # Introducing a lives property for game over condition
    lives = NumericProperty(3)

    def __init__(self, **kwargs):
        super(FruitCatcherGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.serve_fruit()

    def _on_keyboard_closed(self):
        pass

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # Add implementation logic for handling key down events
        pass

    def update(self, dt):
        # Add implementation logic for updating game state
        pass

    def serve_fruit(self):
        fruit = Fruit()
        fruit.center_x = randint(0, Window.width)
        fruit.velocity = Vector(0, -1)
        self.add_widget(fruit)

    def on_touch_move(self, touch):
        self.basket.move(touch)

    def on_touch_down(self, touch):
        self.basket.move(touch)

    def on_touch_up(self):
        # Add implementation logic for handling touch up events
        pass
    
class Fruit(Widget):
    velocity = ListProperty([0, 0])

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class FruitCatcherApp(App):
    def build(self):
        game = FruitCatcherGame()
        Clock.schedule_interval(game.serve_fruit, 1.0)
        return game

if __name__ == '__main__':
    FruitCatcherApp().run()