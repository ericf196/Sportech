#!/usr/bin/env python
#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from app.bin import MainForm  # Módulo principal de la interfaz de usuario

presentation = Builder.load_file("layout/main.kv")

class MyApp(App):

    global config

    mainForm = MainForm.MainForm()

    def build(self):

        Window.maximize()

        Window.bind(on_close=self.mainForm.on_close_window)

        Window.set_icon("resources/icons/Logo_Sportech37_magenta_mini_only.png")

        self.title = 'Sportech 37'

        self.mainForm.console_writer("INFO", "Símbolos del sistema cargados")

        self.mainForm.load_configuration_app_screen()

        self.mainForm.load_configuration_app_videoref()

        self.mainForm.load_configuration_app_engarde()

        return self.mainForm


if __name__ == '__main__':
    MyApp().run()