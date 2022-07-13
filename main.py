

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from functions import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

Builder.load_file("gui.kv")

class MyFigure(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super().__init__(figure = plt.gcf(), **kwargs)
        plt.show()
        print("HI")
        exit()

class WorkWin(Screen):
    def __init__(self, path, **kw):
        super().__init__(**kw)
        box = self.ids.permnt_img
        self.path = path
        plt.imshow(mpimage.imread(path))
        self.permnt_fig = plt.gcf()
        self.permnt_kivfig = FigureCanvasKivyAgg(self.permnt_fig)
        box.add_widget(self.permnt_kivfig)

        box = self.ids.varibl_img
        self.fig = self.permnt_fig
        self.kivfig = FigureCanvasKivyAgg(self.fig)
        box.add_widget(self.kivfig)

    def on_press_toggle(self, id):
        self.toggle = id
        plt.imshow(self.imgs[id][self.n_remove])
        self.fig = plt.gcf()
        self.kivfig.draw()
        plt.clf()

    def on_text_validate(self, val):
        self.n_remove = int(val)
        self.toggle = 0
        self.imgs = shorten(self.path, self.n_remove)
        self.n_remove = 0
        self.ids.nth_seam.disabled = False
    
        plt.imshow(self.imgs[0][-1])
        self.fig = plt.gcf()
        self.kivfig.draw()
        plt.clf()

    def nth_seam(self, val):
        self.n_remove = int(val)
        plt.imshow(self.imgs[self.toggle][self.n_remove])
        self.fig = plt.gcf()
        self.kivfig.draw()
        plt.clf()
        print("HI")
       
class MyFileChooser(Screen):
    def on_selection(self, selection):
        next = WorkWin(path = selection[0], name = "WorkWin")
        self.manager.add_widget(next)
        self.manager.current = "WorkWin"

class MyScreen(Screen):
    pass


class SeamApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MyScreen(name = "HomeSreen"))
        sm.add_widget(MyFileChooser(name = 'FileChooser'))
        return sm

SeamApp().run()
