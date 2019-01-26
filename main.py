from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import (ListProperty, NumericProperty)
from random import randint, choice
from math import log

def concatenate(line):
    i = 0
    if 0 in line:
        for i in range(4):
            line.remove(0)
            line.append(0)
    for i in range(3):
        if line[i] == line[i + 1]:
            line[i] *= 2
            line.pop(i + 1)
            line.append(0)
    return line



class DMQHGame(AnchorLayout):
    tiles = ListProperty()

    colors = [(255,255,255),(155,229,204),(255,204,153),(255,178,102),(255,153,51),(255,128,0),(204,102,0),(153,76,0),(102,51,0),(51,25,0),(0,0,0)]

    def __init__(self, **args):
        super(DMQHGame, self).__init__(**args)
        self.grid = GridLayout(cols=4, center=(0,0))
        self.add_widget(self.grid)
        self.start()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.move_left()
        elif keycode[1] == 'up':
            self.rotate()
            self.move_left()
            self.rotate()
            self.rotate()
            self.rotate()
        elif keycode[1] == 'down':
            self.rotate()
            self.rotate()
            self.rotate()
            self.move_left()
            self.rotate()
        elif keycode[1] == 'right':
            self.rotate()
            self.rotate()
            self.move_left()
            self.rotate()
            self.rotate()
        else:
            return True
        zero_index = [i for i in range(16) if self.tiles[i] == 0]
        if zero_index == []:
            content = Button(text='Cliquez pour recommencer')
            popup = Popup(title = 'Perdu !', content=content,size_hint=(None, None), size=(400, 400), auto_dismiss=False)
            content.bind(on_press=popup.dismiss)
            popup.open()
            self.start()
            return True
        if 2048 in self.tiles:
            content = Button(text='Cliquez pour recommencer')
            popup = Popup(title='Gagné !', content=content, size_hint=(None, None), size=(400, 400), auto_dismiss=False)
            content.bind(on_press=popup.dismiss)
            popup.open()
            self.start()
            return True
        self.tiles[choice(zero_index)] = choice([2, 2, 2, 4])
        self.update_grid()
        return True

    def start(self):
        self.tiles=[0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0, 0]
        self.tiles[randint(0, 15)] = 2
        self.tiles[randint(0, 15)] = 2
        self.update_grid()

    def update_grid(self):
        self.grid.clear_widgets()
        for i in range(16):
            color = self.colors[int(log(self.tiles[i]+1)/log(2))]
            self.grid.add_widget(Button(text=str(self.tiles[i]), font_size=50, color=(1,1,1,1), background_color=(color[0]/255,color[1]/255,color[2]/255,1), background_normal=''))

    def f(self,i):
        return 4 * ((i + 1) % 4) - (i // 4 + 1)

    def move_left(self):
        for i in range(4):
            self.tiles[4 * i:4 * (i + 1)] = concatenate(self.tiles[4 * i:4 * (i + 1)])

    def rotate(self):
        self.tiles = [self.tiles[self.f(i)] for i in range(16)]


class DMQHApp(App):
    def build(self):
        return DMQHGame()

if __name__ == '__main__':
    DMQHApp().run()

def concatenate(line):
    i = 0
    if 0 in line:
        for i in range(4):
            line.remove(0)
            line.append(0)
    for i in range(3):
        if line[i] == line[i+1]:
            line[i] *= 2
            line.pop(i+1)
            line.append(0)
    return line
