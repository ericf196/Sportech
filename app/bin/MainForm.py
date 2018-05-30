#!/usr/bin/env python
#-*- coding: utf-8 -*-

import kivy
kivy.require('1.9.0')
from kivy.core.window import Window
from kivy.uix.widget import Widget
from win32api import GetSystemMetrics
from  win32api import  MessageBox
from threading import Timer

from app.bin.engarde import ClientEngarde
from app.bin.videoref import ClientVideoref
from app.bin.tools import SetInterval


import datetime
import re
import ConfigParser
import os

engarde = ClientEngarde.ClientEngarde()
videoref = ClientVideoref.ClientVideoref()
repeated_send_hello = None
update_data_engarde = False
encoding_title_combat = "resources/font/Default/DejaVuSans.ttf"

class MainForm(Widget):

    is_hide_result_grid = False

    alert_active = False

    def __init__(self, **kwargs):
        super(MainForm, self).__init__(**kwargs)
        self.run_app()

    """
        función de inicialización de la aplicación
    """

    def run_app(self):

        self.ids.box_notify.remove_widget(self.ids.notify)

        #agregar eventos de cambios de estado de los slider de configuracion de grilla de resultados de combate en pareja

        self.ids.country_flag_left_x.bind(value=self.country_left_slider_value_change_x)
        self.ids.country_flag_left_y.bind(value=self.country_left_slider_value_change_y)
        self.ids.name_athlete_left_x.bind(value=self.name_athlete_left_slider_value_change_x)
        self.ids.name_athlete_left_y.bind(value=self.name_athlete_left_slider_value_change_y)
        self.ids.light_athlete_left_x.bind(value=self.light_left__slider_value_change_x)
        self.ids.light_athlete_left_y.bind(value=self.light_left_slider_value_change_y)
        self.ids.punctuation_left_x.bind(value=self.punctuation_left_slider_value_change_x)
        self.ids.punctuation_left_y.bind(value=self.punctuation_left_slider_value_change_y)
        self.ids.punctuation_athlete_rift_x.bind(value=self.punctuation_right_slider_value_change_x)
        self.ids.punctuation_athlete_rift_y.bind(value=self.punctuation_right_slider_value_change_y)
        self.ids.light_right_x.bind(value=self.light_right_slider_value_change_x)
        self.ids.light_right_y.bind(value=self.light_right_slider_value_change_y)
        self.ids.name_athlete_right_x.bind(value=self.name_athlete_right_slider_value_change_x)
        self.ids.name_athlete_right_y.bind(value=self.name_athlete_right_slider_value_change_y)
        self.ids.country_flags_right_x.bind(value=self.country_right_slider_value_change_x)
        self.ids.country_flags_right_y.bind(value=self.country_right_slider_value_change_y)
        self.ids.width_title_bar.bind(value=self.whith_title_bar_slider_value_change)
        self.ids.size_title_bar.bind(value=self.size_title_bar_slider_value_change)

        #agregar eventos de cambios de estado de los slider de configuracion de grilla de resultados de combate en equipo

        self.ids.country_flags_left_x_team.bind(value=self.country_flags_team_left_slider_value_change_x)
        self.ids.country_flags_left_y_team.bind(value=self.country_flags_team_left_slider_value_change_y)
        self.ids.name_athlete_left_pos_x_team.bind(value=self.name_athlete_left_slider_pos_change_x_team)
        self.ids.name_athlete_left_pos_y_team.bind(value=self.name_athlete_left_slider_pos_change_y_team)
        self.ids.light_left_pos_x_team.bind(value=self.light_left_slider_pos_change_x_team)
        self.ids.light_left_pos_y_team.bind(value=self.light_left_slider_pos_change_y_team)
        self.ids.punctuation_left_pos_x_team.bind(value=self.points_left_slider_pos_change_x_team)
        self.ids.punctuation_left_pos_y_team.bind(value=self.points_left_slider_pos_change_y_team)
        self.ids.name_team_left_pos_x.bind(value=self.name_team_left_slider_pos_x)
        self.ids.name_team_left_pos_y.bind(value=self.name_team_left_slider_pos_y)
        self.ids.ponits_team_left_pos_x.bind(value=self.points_team_left_slider_pos_x)
        self.ids.ponits_team_left_pos_y.bind(value=self.points_team_left_slider_pos_y)
        self.ids.ponits_athlete_team_right_pos_x.bind(value=self.ponits_athlete_team_right_pos_slider_x)
        self.ids.ponits_athlete_team_right_pos_y.bind(value=self.ponits_athlete_team_right_pos_slider_y)
        self.ids.light_team_right_pos_x.bind(value=self.light_team_right_pos_slider_x)
        self.ids.light_team_right_pos_y.bind(value=self.light_team_right_pos_slider_y)
        self.ids.name_athlete_team_right_pos_x.bind(value=self.name_athlete_team_right_pos_slider_x)
        self.ids.name_athlete_team_right_pos_y.bind(value=self.name_athlete_team_right_pos_slider_y)
        self.ids.country_flags_team_right_pos_x.bind(value=self.country_flags_team_right_pos_x)
        self.ids.country_flags_team_right_pos_y.bind(value=self.country_flags_team_right_pos_y)
        self.ids.points_team_combat_right_pos_x.bind(value=self.points_team_combat_right_pos_slider_x)
        self.ids.points_team_combat_right_pos_y.bind(value=self.points_team_combat_right_pos_slider_y)
        self.ids.name_team_right_pos_x.bind(value=self.name_team_right_pos_slider_x)
        self.ids.name_team_right_pos_y.bind(value=self.name_team_right_pos_slider_y)

       #agregar evento de cambio de estado a los switch de conexion de engarde y videoref, y actualización de engarde

        self.ids.switch_engarde_connection.bind(active=self.switch_connection_to_engarde)
        self.ids.switch_videoref_connection.bind(active=self.switch_connection_to_videoref)
        self.ids.switch_update_data_engarde.bind(active=self.switch_update_data_engarde_to_videoref)

       #agregar evento keys_spress a las cajas de configuración de la grilla de resultado de combate en pareja

        self.ids.font_size_name_athlete.bind(text=self.on_font_size_name_athlete)
        self.ids.length_name_athlete.bind(text=self.on_length_name_athlete)
        self.ids.timer_font_size.bind(text=self.on_timer_font_size)
        self.ids.match_font_size.bind(text=self.on_match_font_size)
        self.ids.points_font_size.bind(text=self.on_points_font_size)
        self.ids.font_size_title_combat.bind(text=self.on_font_size_title_combat)
        self.ids.country_flag_left_x_text.bind(text=self.on_country_flag_left_x_text)
        self.ids.country_flag_left_y_text.bind(text=self.on_country_flag_left_y_text)
        self.ids.name_athlete_left_x_text.bind(text=self.on_name_athlete_left_x_text)
        self.ids.name_athlete_left_y_text.bind(text=self.on_name_athlete_left_y_text)
        self.ids.light_athlete_left_x_text.bind(text=self.on_light_athlete_left_x_text)
        self.ids.light_athlete_left_y_text.bind(text=self.on_light_athlete_left_y_text)
        self.ids.punctuation_left_x_text.bind(text=self.on_punctuation_left_x_text)
        self.ids.punctuation_left_y_text.bind(text=self.on_punctuation_left_y_text)
        self.ids.country_flags_right_x_text.bind(text=self.on_country_flags_right_x_text)
        self.ids.country_flags_right_y_text.bind(text=self.on_country_flags_right_y_text)
        self.ids.name_athlete_right_x_text.bind(text=self.on_name_athlete_right_x_text)
        self.ids.name_athlete_right_y_text.bind(text=self.on_name_athlete_right_y_text)
        self.ids.punctuation_athlete_rift_x_text.bind(text=self.on_punctuation_athlete_rift_x_text)
        self.ids.punctuation_athlete_rift_y_text.bind(text=self.on_punctuation_athlete_rift_y_text)
        self.ids.light_right_x_text.bind(text=self.on_light_right_x_text)
        self.ids.light_right_y_text.bind(text=self.on_light_right_y_text)
        self.ids.width_title_bar_text.bind(text=self.on_width_title_bar_text)
        self.ids.size_title_bar_text.bind(text=self.on_size_title_bar_text)

        #agregar evento keys_spress a las cajas de configuración de la grilla de resultado de combate en equipo

        self.ids.country_flags_left_x_text_team.bind(text=self.on_country_flags_left_x_text_team)
        self.ids.country_flags_left_y_text_team.bind(text=self.on_country_flags_left_y_text_team)
        self.ids.name_athlete_left_pos_x_text_team.bind(text=self.on_name_athlete_left_pos_x_text_team)
        self.ids.name_athlete_left_pos_y_text_team.bind(text=self.on_name_athlete_left_pos_y_text_team)
        self.ids.light_left_pos_x_text_team.bind(text=self.on_light_left_pos_x_text_team)
        self.ids.light_left_pos_y_text_team.bind(text=self.on_light_left_pos_y_text_team)
        self.ids.punctuation_left_pos_x_text_team.bind(text=self.on_punctuation_left_pos_x_text_team)
        self.ids.punctuation_left_pos_y_text_team.bind(text=self.on_punctuation_left_pos_y_text_team)
        self.ids.name_team_left_pos_x_text.bind(text=self.on_name_team_left_pos_x_text)
        self.ids.name_team_left_pos_y_text.bind(text=self.on_name_team_left_pos_y_text)
        self.ids.ponits_team_left_pos_x_text.bind(text=self.on_ponits_team_left_pos_x_text)
        self.ids.ponits_team_left_pos_y_text.bind(text=self.on_ponits_team_left_pos_y_text)
        self.ids.ponits_athlete_team_right_pos_x_text.bind(text=self.on_ponits_athlete_team_right_pos_x_text)
        self.ids.ponits_athlete_team_right_pos_y_text.bind(text=self.on_ponits_athlete_team_right_pos_y_text)
        self.ids.light_team_right_pos_x_text.bind(text=self.on_light_team_right_pos_x_text)
        self.ids.light_team_right_pos_y_text.bind(text=self.on_light_team_right_pos_y_text)
        self.ids.name_athlete_team_right_pos_x_text.bind(text=self.on_name_athlete_team_right_pos_x_text)
        self.ids.name_athlete_team_right_pos_y_text.bind(text=self.on_name_athlete_team_right_pos_y_text)
        self.ids.country_flags_team_right_pos_x_text.bind(text=self.on_country_flags_team_right_pos_x_text)
        self.ids.country_flags_team_right_pos_y_text.bind(text=self.on_country_flags_team_right_pos_y_text)
        self.ids.points_team_combat_right_pos_x_text.bind(text=self.on_points_team_combat_right_pos_x_text)
        self.ids.points_team_combat_right_pos_y_text.bind(text=self.on_points_team_combat_right_pos_y_text)
        self.ids.name_team_right_pos_x_text.bind(text=self.on_name_team_right_pos_x_text)
        self.ids.name_team_right_pos_y_text.bind(text=self.on_name_team_right_pos_y_text)
        self.ids.size_name_athlete_team.bind(text=self.on_size_name_athlete_team)
        self.ids.size_name_team.bind(text=self.on_size_name_team)
        self.ids.size_points_athlete_team.bind(text=self.on_size_points_athlete_team)
        self.ids.size_points_team.bind(text=self.on_size_points_team)
        self.ids.size_timer_team.bind(text=self.on_size_timer_team)
        self.ids.size_match_team.bind(text=self.on_size_match_team)

        #agregar evento de combinación de teclas

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        if self.keyboard.widget:
            pass
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    """
        Función de combinación de teclas
    """

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if keycode[0] == 97L and modifiers == ['ctrl']:
            print('ctrl + a')

        if keycode[1] == 'escape':
            keyboard.release()

        return True

    """
        funcion de cerrado de aplicación (se ejuta al cerrar la aplicacion apagando las conexiones abiertas)
    """

    def on_close_window(self, instance):

        global engarde

        global videoref

        engarde_status = engarde.return_status_run()

        videoref_status = videoref.return_status_run()

        if engarde_status != None:

            engarde.disconnect_connection()

        if videoref_status != None:

            videoref.disconnect_connection()

    """
       eventos de  slider para el cambio de posición de la grilla de resultados pareja
    """

    def country_left_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_left.do_translation_x = True
        self.ids.countryLeft.country_flags_left_x = float(round(value,2))
        self.ids.country_flag_left_x_text.text = str(round(value,2))
        self.ids.scatter_layout_left.do_translation_x = False

    def country_left_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_left.do_translation_y = True
        self.ids.countryLeft.country_flags_left_y = float(round(value,2))
        self.ids.country_flag_left_y_text.text = str(round(value,2))
        self.ids.scatter_layout_left.do_translation_y = False

    def name_athlete_left_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_left.do_translation_x = True
        self.ids.nameAthleteLeft.name_left_translation_x = float(round(value,2))
        self.ids.name_athlete_left_x_text.text = str(round(value,2))
        self.ids.scatter_layout_left.do_translation_x = False

    def name_athlete_left_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_left.do_translation_x = True
        self.ids.nameAthleteLeft.name_left_translation_y = float(round(value,2))
        self.ids.name_athlete_left_y_text.text = str(round(value,2))
        self.ids.scatter_layout_left.do_translation_x = False

    def light_left__slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_left.do_translation_y = True
        self.ids.light_left.light_left_translation_x = float(round(value,2))
        self.ids.light_athlete_left_x_text.text =  str(round(value, 2))
        self.ids.scatter_layout_left.do_translation_y = False

    def light_left_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_left.do_translation_y = True
        self.ids.light_left.light_left_translation_y = float(round(value,2))
        self.ids.light_athlete_left_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_left.do_translation_y = False

    def punctuation_left_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_left.do_translation_y = True
        self.ids.pointsLeft.points_left_translation_x = float(round(value,2))
        self.ids.punctuation_left_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_left.do_translation_y = False

    def punctuation_left_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_left.do_translation_y = True
        self.ids.pointsLeft.points_left_translation_y = float(round(value,2))
        self.ids.punctuation_left_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_left.do_translation_y = False

    def punctuation_right_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.pointsRight.points_right_translation_x = float(round(value,2))
        self.ids.punctuation_athlete_rift_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def punctuation_right_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.pointsRight.points_right_translation_y = float(round(value,2))
        self.ids.punctuation_athlete_rift_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def light_right_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.light_right.light_right_translation_x = float(round(value,2))
        self.ids.light_right_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def light_right_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.light_right.light_right_translation_y = float(round(value,2))
        self.ids.light_right_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def name_athlete_right_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.nameAthleteRight.name_right_translation_x = float(round(value,2))
        self.ids.name_athlete_right_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def name_athlete_right_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.nameAthleteRight.name_right_translation_y= float(round(value,2))
        self.ids.name_athlete_right_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def country_right_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.countryRight.country_flags_right_x = float(round(value,2))
        self.ids.country_flags_right_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def country_right_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_right.do_translation_y = True
        self.ids.countryRight.country_flags_right_y = float(round(value,2))
        self.ids.country_flags_right_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right.do_translation_y = False

    def whith_title_bar_slider_value_change(self, instance, value):

        self.ids.barra_title.whidth_barra_title_cambate = float(round(value,2))
        self.ids.width_title_bar_text.text = str(round(value, 2))

    def size_title_bar_slider_value_change(self, instance, value):

        self.ids.barra_title.size_x_barra_title_cambate = float(round(value,2))
        self.ids.size_title_bar_text.text = str(round(value, 2))

    """
         eventos de  slider para el cambio de posición de la grilla de resultados equipo
    """

    def country_flags_team_left_slider_value_change_x(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.country_flags_left_team_pos.country_flags_left_team_pos_x = float(round(value, 2))
        self.ids.country_flags_left_x_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def country_flags_team_left_slider_value_change_y(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.country_flags_left_team_pos.country_flags_left_team_pos_y = float(round(value, 2))
        self.ids.country_flags_left_y_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def name_athlete_left_slider_pos_change_x_team(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.athlete_name_pos_team.athlete_name_pos_x_team = float(round(value, 2))
        self.ids.name_athlete_left_pos_x_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def name_athlete_left_slider_pos_change_y_team(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.athlete_name_pos_team.athlete_name_pos_y_team = float(round(value, 2))
        self.ids.name_athlete_left_pos_y_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def light_left_slider_pos_change_x_team(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.light_left_pos_team.light_left_pos_x_team = float(round(value, 2))
        self.ids.light_left_pos_x_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def light_left_slider_pos_change_y_team(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.light_left_pos_team.light_left_pos_y_team = float(round(value, 2))
        self.ids.light_left_pos_y_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def points_left_slider_pos_change_x_team(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.points_left_pos_team.points_left_pos_x_team = float(round(value, 2))
        self.ids.punctuation_left_pos_x_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def points_left_slider_pos_change_y_team(self, instance, value):

        self.ids.scatter_layout_left_team = True
        self.ids.points_left_pos_team.points_left_pos_y_team = float(round(value, 2))
        self.ids.punctuation_left_pos_y_text_team.text = str(round(value, 2))
        self.ids.scatter_layout_left_team = False

    def name_team_left_slider_pos_x(self, instance, value):

        self.ids.scatter_layout_left_name_team = True
        self.ids.team_nema_left_pos.team_name_left_pos_x = float(round(value, 2))
        self.ids.name_team_left_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_left_name_team = False

    def name_team_left_slider_pos_y(self, instance, value):

        self.ids.scatter_layout_left_name_team = True
        self.ids.team_nema_left_pos.team_name_left_pos_y = float(round(value, 2))
        self.ids.name_team_left_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_left_name_team = False

    def points_team_left_slider_pos_x(self, instance, value):

        self.ids.scatter_layout_left_name_team = True
        self.ids.team_points_left_pos.team_points_left_pos_x = float(round(value, 2))
        self.ids.ponits_team_left_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_left_name_team = False

    def points_team_left_slider_pos_y(self, instance, value):

        self.ids.scatter_layout_left_name_team = True
        self.ids.team_points_left_pos.team_points_left_pos_y = float(round(value, 2))
        self.ids.ponits_team_left_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_left_name_team = False

    def ponits_athlete_team_right_pos_slider_x(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.points_athlte_team_right_pos.points_athlte_team_right_pos_x = float(round(value, 2))
        self.ids.ponits_athlete_team_right_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def ponits_athlete_team_right_pos_slider_y(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.points_athlte_team_right_pos.points_athlte_team_right_pos_y = float(round(value, 2))
        self.ids.ponits_athlete_team_right_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def light_team_right_pos_slider_x(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.light_athlte_team_right_pos.light_athlte_team_right_pos_x = float(round(value, 2))
        self.ids.light_team_right_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def light_team_right_pos_slider_y(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.light_athlte_team_right_pos.light_athlte_team_right_pos_y = float(round(value, 2))
        self.ids.light_team_right_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def name_athlete_team_right_pos_slider_x(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.name_athlte_team_right_pos.name_athlte_team_right_pos_x = float(round(value, 2))
        self.ids.name_athlete_team_right_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def name_athlete_team_right_pos_slider_y(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.name_athlte_team_right_pos.name_athlte_team_right_pos_y = float(round(value, 2))
        self.ids.name_athlete_team_right_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def country_flags_team_right_pos_x(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.country_flags_team_right_pos.country_flags_team_right_pos_x = float(round(value, 2))
        self.ids.country_flags_team_right_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def country_flags_team_right_pos_y(self, instance, value):

        self.ids.scatter_layout_right_team = True
        self.ids.country_flags_team_right_pos.country_flags_team_right_pos_y = float(round(value, 2))
        self.ids.country_flags_team_right_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_right_team = False

    def points_team_combat_right_pos_slider_x(self, instance, value):

        self.ids.scatter_layout_team_right = True
        self.ids.team_points_right_pos.team_points_right_pos_x = float(round(value, 2))
        self.ids.points_team_combat_right_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_team_right = False

    def points_team_combat_right_pos_slider_y(self, instance, value):

        self.ids.scatter_layout_team_right = True
        self.ids.team_points_right_pos.team_points_right_pos_y = float(round(value, 2))
        self.ids.points_team_combat_right_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_team_right = False

    def name_team_right_pos_slider_x(self, instance, value):

        self.ids.scatter_layout_team_right = True
        self.ids.team_name_right_pos.team_name_right_pos_x = float(round(value, 2))
        self.ids.name_team_right_pos_x_text.text = str(round(value, 2))
        self.ids.scatter_layout_team_right = False

    def name_team_right_pos_slider_y(self, instance, value):

        self.ids.scatter_layout_team_right = True
        self.ids.team_name_right_pos.team_name_right_pos_y = float(round(value, 2))
        self.ids.name_team_right_pos_y_text.text = str(round(value, 2))
        self.ids.scatter_layout_team_right = False

    """
        funciones keys_spress de cajas de texto de configuración de la grilla de resultados pareja
    """

    def on_font_size_name_athlete(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.nameAthleteLeft.font_size_name_left = str(value) + "sp"
                self.ids.nameAthleteRight.font_size_name_right = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.font_size_name_athlete.text = size

    def on_length_name_athlete(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:
                name = str(self.ids.nameAthleteLeft.text)
                #self.ids.nameAthleteLeft.text = name[0:int(value)]

            else:
                size = value[0:2]
                self.ids.length_name_athlete.text = size

    def on_timer_font_size(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.timer.font_size_timer = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.timer_font_size.text = size

    def on_match_font_size(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.match.match_font_size = str(value) + "sp"

            else:

                size = value[0:2]
                self.ids.match_font_size.text = size

    def on_points_font_size(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.pointsLeft.font_size_points_left = str(value) + "sp"
                self.ids.pointsRight.font_size_points_right = str(value) + "sp"

            else:

                size = value[0:2]
                self.ids.points_font_size.text = size

    def on_font_size_title_combat(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.title_combat.font_size_title_combat = str(value) + "sp"

            else:

                size = value[0:2]
                self.ids.font_size_title_combat.text = size

    def on_country_flag_left_x_text(self, instance, value):

        length = len(value)

        size = value

        if re.match("^-?[0-9]\d*(\.\d+)?$", value):

            if int(length) <= 6:

                if float(size) < float(self.ids.country_flag_left_x.min):

                    size = "0.00"

                if float(size) > float(self.ids.country_flag_left_x.max):

                    size = str(self.ids.country_flag_left_x.max)

                self.ids.country_flag_left_x.value = float(size)

            else:

                size = size[0:6]
                self.ids.country_flag_left_x_text.text = size
        else:

            if value != "-" and value != ".":

                size = value[0:(int(length) - 1)]
                self.ids.country_flag_left_x_text.text = size

    def on_country_flag_left_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:

                size_int = size_int[0:3]

            if len(size_float) > 2:

                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:

                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if  float(size) > float(self.ids.country_flag_left_y.max):

                size = str(self.ids.country_flag_left_y.max)

            self.ids.country_flag_left_y.value = float(size)

            self.ids.country_flag_left_y_text.text = size

    def on_name_athlete_left_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.name_athlete_left_x.max):

                size = str(self.ids.name_athlete_left_x.max)

            self.ids.name_athlete_left_x.value = float(size)

            self.ids.name_athlete_left_x_text.text = size

    def on_name_athlete_left_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if  float(size) > float(self.ids.name_athlete_left_y.max):

                size = str(self.ids.name_athlete_left_y.max)

            self.ids.name_athlete_left_y.value = float(size)

            self.ids.name_athlete_left_y_text.text = size

    def on_light_athlete_left_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.light_athlete_left_x.max):

                size = str(self.ids.light_athlete_left_x.max)

            self.ids.light_athlete_left_x.value = float(size)

            self.ids.light_athlete_left_x_text.text = size

    def on_light_athlete_left_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.light_athlete_left_y.max):

                size = str(self.ids.light_athlete_left_y.max)

            self.ids.light_athlete_left_y.value = float(size)

            self.ids.light_athlete_left_y_text.text = size

    def on_punctuation_left_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.punctuation_left_x.max):

                size = str(self.ids.punctuation_left_x.max)

            self.ids.punctuation_left_x.value = float(size)

            self.ids.punctuation_left_x_text.text = size

    def on_punctuation_left_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.punctuation_left_y.max):

                size = str(self.ids.punctuation_left_y.max)

            self.ids.punctuation_left_y.value = float(size)

            self.ids.punctuation_left_y_text.text = size

    def on_country_flags_right_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.country_flags_right_x.max):

                size = str(self.ids.country_flags_right_x.max)

            self.ids.country_flags_right_x.value = float(size)

            self.ids.country_flags_right_x_text.text = size

    def on_country_flags_right_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.country_flags_right_y.max):

                size = str(self.ids.country_flags_right_y.max)

            self.ids.country_flags_right_y.value = float(size)

            self.ids.country_flags_right_y_text.text = size

    def on_name_athlete_right_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.name_athlete_right_x.max):

                size = str(self.ids.name_athlete_right_x.max)

            self.ids.name_athlete_right_x.value = float(size)

            self.ids.name_athlete_right_x_text.text = size

    def on_name_athlete_right_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.name_athlete_right_y.max):

                size = str(self.ids.name_athlete_right_y.max)

            self.ids.name_athlete_right_y.value = float(size)

            self.ids.name_athlete_right_y_text.text = size

    def on_punctuation_athlete_rift_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.punctuation_athlete_rift_x.max):

                size = str(self.ids.punctuation_athlete_rift_x.max)

            self.ids.punctuation_athlete_rift_x.value = float(size)

            self.ids.punctuation_athlete_rift_x_text.text = size

    def on_punctuation_athlete_rift_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.punctuation_athlete_rift_y.max):

                size = str(self.ids.punctuation_athlete_rift_y.max)

            self.ids.punctuation_athlete_rift_y.value = float(size)

            self.ids.punctuation_athlete_rift_y_text.text = size

    def on_light_right_x_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.light_right_x.max):

                size = str(self.ids.light_right_x.max)

            self.ids.light_right_x.value = float(size)

            self.ids.light_right_x_text.text = size

    def on_light_right_y_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.light_right_y.max):

                size = str(self.ids.light_right_y.max)

            self.ids.light_right_y.value = float(size)

            self.ids.light_right_y_text.text = size

    def on_width_title_bar_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.width_title_bar.max):

                size = str(self.ids.width_title_bar.max)

            self.ids.width_title_bar.value = float(size)

            self.ids.width_title_bar_text.text = size

    def on_size_title_bar_text(self, instance, value):

        aux = value.split('.', 1)

        size = ""

        if len(aux) == 2:

            size_int = str(aux[0])

            size_float = str(aux[1])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            if len(size_float) > 2:
                size_float = size_float[0:2]

            size = str(size_int) + "." + str(size_float)

        else:

            size_int = str(aux[0])

            if len(size_int) > 3:
                size_int = size_int[0:3]

            size = str(size_int) + ".00"

        if value.isnumeric() or re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) > float(self.ids.size_title_bar.max):
                size = str(self.ids.size_title_bar.max)

            self.ids.size_title_bar.value = float(size)

            self.ids.size_title_bar_text.text = size

    """
       funciones keys_spress de cajas de texto de configuración de la grilla de resultados equipo
    """

    def on_country_flags_left_x_text_team(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.country_flags_left_x_team.min):

                self.ids.country_flags_left_x_team.value = 0
                self.ids.country_flags_left_x_text_team.text = '0'

            elif float(size) > float(self.ids.country_flags_left_x_team.max):

                self.ids.country_flags_left_x_team.value = 0
                self.ids.country_flags_left_x_text_team.text = '0'

            else:

                self.ids.country_flags_left_x_team.value = float(size)
                self.ids.country_flags_left_x_text_team.text = size

    def on_country_flags_left_y_text_team(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):


            if float(size) < float(self.ids.country_flags_left_y_team.min):

                self.ids.country_flags_left_y_team.value = 0
                self.ids.country_flags_left_y_text_team.text = '0'

            elif float(size) > float(self.ids.country_flags_left_y_team.max):

                self.ids.country_flags_left_y_team.value = 0
                self.ids.country_flags_left_y_text_team.text = '0'

            else:

                self.ids.country_flags_left_y_team.value = float(size)
                self.ids.country_flags_left_y_text_team.text = size

    def on_name_athlete_left_pos_x_text_team(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):


            if float(size) < float(self.ids.name_athlete_left_pos_x_team.min):

                self.ids.name_athlete_left_pos_x_team.value = 0
                self.ids.name_athlete_left_pos_x_text_team.text = '0'

            elif float(size) > float(self.ids.name_athlete_left_pos_x_team.max):

                self.ids.name_athlete_left_pos_x_team.value = 0
                self.ids.name_athlete_left_pos_x_text_team.text = '0'

            else:

                self.ids.name_athlete_left_pos_x_team.value = float(size)
                self.ids.name_athlete_left_pos_x_text_team.text = size

    def on_name_athlete_left_pos_y_text_team(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_athlete_left_pos_y_team.min):

                self.ids.name_athlete_left_pos_y_team.value = 0
                self.ids.name_athlete_left_pos_y_text_team.text = '0'

            elif float(size) > float(self.ids.name_athlete_left_pos_y_team.max):

                self.ids.name_athlete_left_pos_y_team.value = 0
                self.ids.name_athlete_left_pos_y_text_team.text = '0'

            else:

                self.ids.name_athlete_left_pos_y_team.value = float(size)
                self.ids.name_athlete_left_pos_y_text_team.text = size

    def on_light_left_pos_x_text_team(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.light_left_pos_x_team.min):

                self.ids.light_left_pos_x_team.value = 0
                self.ids.light_left_pos_x_text_team.text = '0'

            elif float(size) > float(self.ids.light_left_pos_x_team.max):

                self.ids.light_left_pos_x_team.value = 0
                self.ids.light_left_pos_x_text_team.text = '0'

            else:

                self.ids.light_left_pos_x_team.value = float(size)
                self.ids.light_left_pos_x_text_team.text = size

    def on_light_left_pos_y_text_team(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.light_left_pos_y_team.min):

                self.ids.light_left_pos_y_team.value = 0
                self.ids.light_left_pos_y_text_team.text = '0'

            elif float(size) > float(self.ids.light_left_pos_y_team.max):

                self.ids.light_left_pos_y_team.value = 0
                self.ids.light_left_pos_y_text_team.text = '0'

            else:

                self.ids.light_left_pos_y_team.value = float(size)
                self.ids.light_left_pos_y_text_team.text = size

    def on_punctuation_left_pos_x_text_team(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.punctuation_left_pos_x_team.min):

                self.ids.punctuation_left_pos_x_team.value = 0
                self.ids.punctuation_left_pos_x_text_team.text = '0'

            elif float(size) > float(self.ids.punctuation_left_pos_x_team.max):

                self.ids.punctuation_left_pos_x_team.value = 0
                self.ids.punctuation_left_pos_x_text_team.text = '0'

            else:

                self.ids.punctuation_left_pos_x_team.value = float(size)
                self.ids.punctuation_left_pos_x_text_team.text = size

    def on_punctuation_left_pos_y_text_team(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.punctuation_left_pos_y_team.min):

                self.ids.punctuation_left_pos_y_team.value = 0
                self.ids.punctuation_left_pos_y_text_team.text = '0'

            elif float(size) > float(self.ids.punctuation_left_pos_y_team.max):

                self.ids.punctuation_left_pos_y_team.value = 0
                self.ids.punctuation_left_pos_y_text_team.text = '0'

            else:

                self.ids.punctuation_left_pos_y_team.value = float(size)
                self.ids.punctuation_left_pos_y_text_team.text = size

    def on_name_team_left_pos_x_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_team_left_pos_x.min):

                self.ids.name_team_left_pos_x.value = 0
                self.ids.name_team_left_pos_x_text.text = '0'

            elif float(size) > float(self.ids.name_team_left_pos_x.max):

                self.ids.name_team_left_pos_x.value = 0
                self.ids.name_team_left_pos_x_text.text = '0'

            else:

                self.ids.name_team_left_pos_x.value = float(size)
                self.ids.name_team_left_pos_x_text.text = size

    def on_name_team_left_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_team_left_pos_y.min):

                self.ids.name_team_left_pos_y.value = 0
                self.ids.name_team_left_pos_y_text.text = '0'

            elif float(size) > float(self.ids.name_team_left_pos_y.max):

                self.ids.name_team_left_pos_y.value = 0
                self.ids.name_team_left_pos_y_text.text = '0'

            else:

                self.ids.name_team_left_pos_y.value = float(size)
                self.ids.name_team_left_pos_y_text.text = size

    def on_ponits_team_left_pos_x_text(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.ponits_team_left_pos_x.min):

                self.ids.ponits_team_left_pos_x.value = 0
                self.ids.ponits_team_left_pos_x_text.text = '0'

            elif float(size) > float(self.ids.ponits_team_left_pos_x.max):

                self.ids.ponits_team_left_pos_x.value = 0
                self.ids.ponits_team_left_pos_x_text.text = '0'

            else:

                self.ids.ponits_team_left_pos_x.value = float(size)
                self.ids.ponits_team_left_pos_x_text.text = size

    def on_ponits_team_left_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.ponits_team_left_pos_y.min):

                self.ids.ponits_team_left_pos_y.value = 0
                self.ids.ponits_team_left_pos_y_text.text = '0'

            elif float(size) > float(self.ids.ponits_team_left_pos_y.max):

                self.ids.ponits_team_left_pos_y.value = 0
                self.ids.ponits_team_left_pos_y_text.text = '0'

            else:

                self.ids.ponits_team_left_pos_y.value = float(size)
                self.ids.ponits_team_left_pos_y_text.text = size

    def on_ponits_athlete_team_right_pos_x_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.ponits_athlete_team_right_pos_x.min):

                self.ids.ponits_athlete_team_right_pos_x.value = 0
                self.ids.ponits_athlete_team_right_pos_x_text.text = '0'

            elif float(size) > float(self.ids.ponits_athlete_team_right_pos_x.max):

                self.ids.ponits_athlete_team_right_pos_x.value = 0
                self.ids.ponits_athlete_team_right_pos_x_text.text = '0'

            else:

                self.ids.ponits_athlete_team_right_pos_x.value = float(size)
                self.ids.ponits_athlete_team_right_pos_x_text.text = size

    def on_ponits_athlete_team_right_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.ponits_athlete_team_right_pos_y.min):

                self.ids.ponits_athlete_team_right_pos_y.value = 0
                self.ids.ponits_athlete_team_right_pos_y_text.text = '0'

            elif float(size) > float(self.ids.ponits_athlete_team_right_pos_y.max):

                self.ids.ponits_athlete_team_right_pos_y.value = 0
                self.ids.ponits_athlete_team_right_pos_y_text.text = '0'

            else:

                self.ids.ponits_athlete_team_right_pos_y.value = float(size)
                self.ids.ponits_athlete_team_right_pos_y_text.text = size

    def on_light_team_right_pos_x_text(self, instance, value):

        size = self.is_float(value)


        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.light_team_right_pos_x.min):

                self.ids.light_team_right_pos_x.value = 0
                self.ids.light_team_right_pos_x_text.text = '0'

            elif float(size) > float(self.ids.light_team_right_pos_x.max):

                self.ids.light_team_right_pos_x.value = 0
                self.ids.light_team_right_pos_x_text.text = '0'

            else:

                self.ids.light_team_right_pos_x.value = float(size)
                self.ids.light_team_right_pos_x_text.text = size

    def on_light_team_right_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.light_team_right_pos_y.min):

                self.ids.light_team_right_pos_y.value = 0
                self.ids.light_team_right_pos_y_text.text = '0'

            elif float(size) > float(self.ids.light_team_right_pos_y.max):

                self.ids.light_team_right_pos_y.value = 0
                self.ids.light_team_right_pos_y_text.text = '0'

            else:

                self.ids.light_team_right_pos_y.value = float(size)
                self.ids.light_team_right_pos_y_text.text = size

    def on_name_athlete_team_right_pos_x_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_athlete_team_right_pos_x.min):

                self.ids.name_athlete_team_right_pos_x.value = 0
                self.ids.name_athlete_team_right_pos_x_text.text = '0'

            elif float(size) > float(self.ids.name_athlete_team_right_pos_x.max):

                self.ids.name_athlete_team_right_pos_x.value = 0
                self.ids.name_athlete_team_right_pos_x_text.text = '0'

            else:

                self.ids.name_athlete_team_right_pos_x.value = float(size)
                self.ids.name_athlete_team_right_pos_x_text.text = size

    def on_name_athlete_team_right_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_athlete_team_right_pos_y.min):

                self.ids.name_athlete_team_right_pos_y.value = 0
                self.ids.name_athlete_team_right_pos_y_text.text = '0'

            elif float(size) > float(self.ids.name_athlete_team_right_pos_y.max):

                self.ids.name_athlete_team_right_pos_y.value = 0
                self.ids.name_athlete_team_right_pos_y_text.text = '0'

            else:

                self.ids.name_athlete_team_right_pos_y.value = float(size)
                self.ids.name_athlete_team_right_pos_y_text.text = size

    def on_country_flags_team_right_pos_x_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.country_flags_team_right_pos_x.min):

                self.ids.country_flags_team_right_pos_x.value = 0
                self.ids.country_flags_team_right_pos_x_text.text = '0'

            elif float(size) > float(self.ids.country_flags_team_right_pos_x.max):

                self.ids.country_flags_team_right_pos_x.value = 0
                self.ids.country_flags_team_right_pos_x_text.text = '0'

            else:

                self.ids.country_flags_team_right_pos_x.value = float(size)
                self.ids.country_flags_team_right_pos_x_text.text = size

    def on_country_flags_team_right_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.country_flags_team_right_pos_y.min):

                self.ids.country_flags_team_right_pos_y.value = 0
                self.ids.country_flags_team_right_pos_y_text.text = '0'

            elif float(size) > float(self.ids.country_flags_team_right_pos_y.max):

                self.ids.country_flags_team_right_pos_y.value = 0
                self.ids.country_flags_team_right_pos_y_text.text = '0'

            else:

                self.ids.country_flags_team_right_pos_y.value = float(size)
                self.ids.country_flags_team_right_pos_y_text.text = size

    def on_points_team_combat_right_pos_x_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.points_team_combat_right_pos_x.min):

                self.ids.points_team_combat_right_pos_x.value = 0
                self.ids.points_team_combat_right_pos_x_text.text = '0'

            elif float(size) > float(self.ids.points_team_combat_right_pos_x.max):

                self.ids.points_team_combat_right_pos_x.value = 0
                self.ids.points_team_combat_right_pos_x_text.text = '0'

            else:

                self.ids.points_team_combat_right_pos_x.value = float(size)
                self.ids.points_team_combat_right_pos_x_text.text = size

    def on_points_team_combat_right_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.points_team_combat_right_pos_y.min):

                self.ids.points_team_combat_right_pos_y.value = 0
                self.ids.points_team_combat_right_pos_y_text.text = '0'

            elif float(size) > float(self.ids.points_team_combat_right_pos_y.max):

                self.ids.points_team_combat_right_pos_y.value = 0
                self.ids.points_team_combat_right_pos_y_text.text = '0'

            else:

                self.ids.points_team_combat_right_pos_y.value = float(size)
                self.ids.points_team_combat_right_pos_y_text.text = size

    def on_name_team_right_pos_x_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_team_right_pos_x.min):

                self.ids.name_team_right_pos_x.value = 0
                self.ids.name_team_right_pos_x_text.text = '0'

            elif float(size) > float(self.ids.name_team_right_pos_x.max):

                self.ids.name_team_right_pos_x.value = 0
                self.ids.name_team_right_pos_x_text.text = '0'

            else:

                self.ids.name_team_right_pos_x.value = float(size)
                self.ids.name_team_right_pos_x_text.text = size

    def on_name_team_right_pos_y_text(self, instance, value):

        size = self.is_float(value)

        if re.match("^-?[0-9]\d*(\.\d+)?$", size):

            if float(size) < float(self.ids.name_team_right_pos_y.min):

                self.ids.name_team_right_pos_y.value = 0
                self.ids.name_team_right_pos_y_text.text = '0'

            elif float(size) > float(self.ids.name_team_right_pos_y.max):

                self.ids.name_team_right_pos_y.value = 0
                self.ids.name_team_right_pos_y_text.text = '0'

            else:

                self.ids.name_team_right_pos_y.value = float(size)
                self.ids.name_team_right_pos_y_text.text = size

    def on_size_name_athlete_team(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.athlete_name_pos_team.size_name_team_athlete = str(value) + "sp"
                self.ids.name_athlte_team_right_pos.font_size_athlete_team_right = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.size_name_athlete_team.text = size

    def on_size_name_team(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.team_nema_left_pos.font_size_team_name_left = str(value) + "sp"
                self.ids.team_name_right_pos.font_size_team_name_right = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.size_name_team.text = size

    def on_size_points_athlete_team(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.points_left_pos_team.font_size_points_left = str(value) + "sp"
                self.ids.points_athlte_team_right_pos.font_size_athlete_team_right = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.size_points_athlete_team.text = size

    def on_size_points_team(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.team_points_left_pos.font_size_points_left = str(value) + "sp"
                self.ids.team_points_right_pos.font_size_team_points_right = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.size_points_athlete_team.text = size

    def on_size_timer_team(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.timer_team.font_size_timer = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.size_timer_team.text = size

    def on_size_match_team(self, instance, value):

        if value.isnumeric():

            if len(value) <= 2:

                self.ids.match_team.match_font_size = str(value) + "sp"

            else:
                size = value[0:2]
                self.ids.size_match_team.text = size

    """
        funciones de cambio de codificación de caracteres
    """

    def encoding_grrid_result(self, encoding):

        global encoding_title_combat

        if encoding == "Chinese":

            encoding_ttf = "resources/font/Chinese/Simplified_and_traditional_chinese.ttf"

            if self.ids.encoding_chinese.state != "down":

                 self.ids.encoding_chinese.state = "down"


        elif encoding == "Japanese":

            encoding_ttf = "resources/font/Japanese/japanese.ttf"

            if self.ids.encoding_japanese.state != "down":

                 self.ids.encoding_japanese.state = "down"

        else:

            encoding_ttf = "resources/font/Default/DejaVuSans.ttf"

            if self.ids.encoding_default.state != "down":

                self.ids.encoding_default.state = "down"

        self.ids.input_title_combat.font_name = str(encoding_ttf)

        self.ids.title_combat.font_name = str(encoding_ttf)

        encoding_title_combat = encoding

    def toggle_button_encoding(self, encoding ):

        if encoding == "Default":

            self.ids.encoding_default.state = 'down'

        elif encoding == "Chinese":

            self.ids.encoding_chinese.state='down'

        elif encoding == "Japanese":

            self.ids.encoding_japanese.state = 'down'

    """
        función de cambio de titulo del campeonato
    """

    def value_title_combat(self):

        if self.ids.input_title_combat.text != "":

            self.ids.title_combat.text = self.ids.input_title_combat.text

        else:

            self.console_writer("WARNING", "Introduzca el titulo del combate")

    """
        función de cambio de grilla de resultado entre pareja y equipo
    """

    def change_widget_result_combat(self, widget):

        self.ids.configuration_result_container.remove_widget(self.ids.title_configuration_font)
        self.ids.configuration_result_container.remove_widget(self.ids.title_configuration_pos)
        self.ids.configuration_result_container.remove_widget(self.ids.box_coutry_left_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_name_athlete_left_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_light_left_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_punctuation_left_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_coutry_right_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_name_athlete_right_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_punctuation_rift_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_light_right_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.box_bar_combat)
        self.ids.configuration_result_container.remove_widget(self.ids.box_country_left_team)
        self.ids.configuration_result_container.remove_widget(self.ids.box_name_athlete_left)
        self.ids.configuration_result_container.remove_widget(self.ids.box_light_athlete_left)
        self.ids.configuration_result_container.remove_widget(self.ids.box_punctuation_athlete_left)
        self.ids.configuration_result_container.remove_widget(self.ids.box_name_team_combat)
        self.ids.configuration_result_container.remove_widget(self.ids.box_points_team_combat)
        self.ids.configuration_result_container.remove_widget(self.ids.box_points_team_combat_right)
        self.ids.configuration_result_container.remove_widget(self.ids.box_light_team_combat_right)
        self.ids.configuration_result_container.remove_widget(self.ids.box_name_athlete_team_combat_right)
        self.ids.configuration_result_container.remove_widget(self.ids.box_country_flags_team_combat_right)
        self.ids.configuration_result_container.remove_widget(self.ids.box_team_points_combat_right)
        self.ids.configuration_result_container.remove_widget(self.ids.box_name_team_combat_right)
        self.ids.box_barra_title.remove_widget(self.ids.barra_title)


        self.ids.widget_combat_container.remove_widget(self.ids.widget_combat_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_name_athlete_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_timer_match_couple)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_point_couple)


        self.ids.widget_combat_container.remove_widget(self.ids.widget_combat_team)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_name_athlete_team)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_name_team)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_points_tean)
        self.ids.configuration_result_container.remove_widget(self.ids.configuration_timer_macht_tean)


        if widget == "team":

            self.ids.widget_combat_container.add_widget(self.ids.widget_combat_team)
            self.ids.configuration_result_container.add_widget(self.ids.title_configuration_font)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_name_athlete_team)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_name_team)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_points_tean)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_timer_macht_tean)
            self.ids.configuration_result_container.add_widget(self.ids.title_configuration_pos)
            self.ids.configuration_result_container.add_widget(self.ids.box_country_left_team)
            self.ids.configuration_result_container.add_widget(self.ids.box_name_athlete_left)
            self.ids.configuration_result_container.add_widget(self.ids.box_light_athlete_left)
            self.ids.configuration_result_container.add_widget(self.ids.box_punctuation_athlete_left)
            self.ids.configuration_result_container.add_widget(self.ids.box_name_team_combat)
            self.ids.configuration_result_container.add_widget(self.ids.box_points_team_combat)
            self.ids.configuration_result_container.add_widget(self.ids.box_points_team_combat_right)
            self.ids.configuration_result_container.add_widget(self.ids.box_light_team_combat_right)
            self.ids.configuration_result_container.add_widget(self.ids.box_name_athlete_team_combat_right)
            self.ids.configuration_result_container.add_widget(self.ids.box_country_flags_team_combat_right)
            self.ids.configuration_result_container.add_widget(self.ids.box_team_points_combat_right)
            self.ids.configuration_result_container.add_widget(self.ids.box_name_team_combat_right)


            self.ids.configuration_result_container.add_widget(self.ids.box_bar_combat)

            if self.ids.change_wisget_combat_team.state != "down":

                self.ids.change_wisget_combat_team.state = 'down'

            self.load_configuration_app_screen_team()

        if widget == "couple":

            self.ids.widget_combat_container.add_widget(self.ids.widget_combat_couple)
            self.ids.configuration_result_container.add_widget(self.ids.title_configuration_font)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_name_athlete_couple)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_timer_match_couple)
            self.ids.configuration_result_container.add_widget(self.ids.configuration_point_couple)
            self.ids.configuration_result_container.add_widget(self.ids.title_configuration_pos)
            self.ids.configuration_result_container.add_widget(self.ids.box_coutry_left_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_name_athlete_left_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_light_left_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_punctuation_left_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_coutry_right_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_name_athlete_right_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_punctuation_rift_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_light_right_couple)
            self.ids.configuration_result_container.add_widget(self.ids.box_bar_combat)

            if self.ids.change_wisget_combat_couple.state != "down":

                self.ids.change_wisget_combat_couple.state = 'down'

            self.load_configuration_app_screen_couple()

        self.ids.box_barra_title.add_widget(self.ids.barra_title)


    """
        Ocultar grilla de resultados
    """

    def hide_grid_result(self):

        if self.ids.change_wisget_combat_team.state == "down":

            self.ids.widget_combat_container.remove_widget(self.ids.widget_combat_team)

        else:

            self.ids.widget_combat_container.remove_widget(self.ids.widget_combat_couple)

        self.is_hide_result_grid = True

        self.ids.box_barra_title.remove_widget(self.ids.barra_title)

        if not self.alert_active:

            self.alert_active = True

            self.console_writer("ERROR", "El videoref no responde")

            self.ids.box_notify.add_widget(self.ids.notify)


    def display_result_grid(self):

        if self.is_hide_result_grid:

            self.ids.box_notify.remove_widget(self.ids.notify)

            if self.ids.change_wisget_combat_team.state == "down":

                self.ids.widget_combat_container.add_widget(self.ids.widget_combat_team)

            else:

                self.ids.widget_combat_container.add_widget(self.ids.widget_combat_couple)

            self.is_hide_result_grid = False

            if self.alert_active:

                self.alert_active = False

            self.ids.box_barra_title.add_widget(self.ids.barra_title)

    """
        función de impresion en la consola
    """

    def console_writer(self, type, message):

        dateTime = datetime.datetime.now()

        color = "239b56"

        len_string = len( self.ids.console.text )

        if type == "WARNING":

            color = "f4d03f"

        elif type == "ERROR":

            color = "922b21"

        if int(len_string) > 3000:

            self.ids.console.text = ""


        if self.ids.console.text == "":

            self.ids.console.text = "[color=" + color + "][" + type + "] [" + dateTime.strftime('%d-%m-%Y (%I:%M:%S)') + "] " + message + "[/color]\n"
        else:

            self.ids.console.text += "[color=" + color + "][" + type + "] [" + dateTime.strftime('%d-%m-%Y (%I:%M:%S)') + "] " + message + "[/color]\n"

    """
        Función para formatear el valor introducido en las cajas de textos de la configuracion por equipo
    """

    def is_float(self, value):

        aux = value.split('.', 1)

        aux_int = ""

        aux_float = ""

        size = ""

        if int(len(aux)) > 0 and str(aux[0]) != "":

            number_int = str(aux[0])

        else:

            number_int = "0"

        if int(len(aux)) > 1 and str(aux[0]) != "":

            number_float = str(aux[1])

        else:

            number_float = "0"

        length_number_int = len(number_int)

        # formatear parte entera

        if int(len(number_int)) > 0 and number_int[0] == "-":
            size = "-"

            number_int = number_int[1:int(length_number_int)]

        for char in number_int:

            if re.match("[0-9]", char):
                aux_int += char

        if int(len(aux_int)) <= 3:

            size += aux_int

        else:

            size += aux_int[0:3]

        # formatear parte flotante

        for char in number_float:

            if re.match("[0-9]", char):
                aux_float += char

        if int(len(aux_float)) <= 2:

            size += ("." + str(aux_float))

        else:

            size += ("." + str(aux_float[0:2]))

        return  size

    """
        funciones de conexión y desconección del engarde
    """


    def switch_connection_to_engarde(self, instance, value):

        if re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.ids.ip_engarde.text):

            if re.search("^-?[0-9]+$", self.ids.port_received_engarde.text):

                if re.search("^-?[0-9]+$", self.ids.port_send_engarde.text):

                        if value :

                            self.Connection_to_engarde()
                            self.ids.ip_engarde.readonly = True
                            self.ids.port_received_engarde.readonly = True
                            self.ids.port_send_engarde.readonly = True

                        else:

                            self.disconnect_connection_to_engarde()
                            self.ids.ip_engarde.readonly = False
                            self.ids.port_received_engarde.readonly = False
                            self.ids.port_send_engarde.readonly = False
                else:

                    if value:

                        self.console_writer("WARNING", "El puerto de envio al engarde no cumple con el formato adecuado")
                        self.ids.switch_engarde_connection.active = False

            else:

                if value:

                    self.console_writer("WARNING", "El puerto de escucha para el engarde no cumple con el formato adecuado")
                    self.ids.switch_engarde_connection.active = False

        else:

            if value:

                self.console_writer("WARNING", "La ip del engrde no cumple con el formato adecuado")
                self.ids.switch_engarde_connection.active = False

    def action_bar_connection_to_engarde(self):

        self.ids.switch_engarde_connection.active = True

    def action_bar_disconnect_connection_to_engarde(self):

        self.ids.switch_engarde_connection.active = False

    def Connection_to_engarde(self):

        global engarde

        engarde.run(str(self.ids.ip_engarde.text),
                    int(self.ids.port_received_engarde.text),
                    int(self.ids.port_send_engarde.text))

    def disconnect_connection_to_engarde(self):

        global engarde

        engarde.disconnect_connection()

    """
        funcion de cambio de combate del engarde
    """

    def change_combat_in_engarde(self, option):

        global engarde

        engarde.change_combat_engarde(option)

    """
        funciones de conexión y desconección del videoref
    """

    def switch_connection_to_videoref(self, instance, value):

        if re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.ids.ip_videoref.text):

            if re.search("^-?[0-9]+$", self.ids.port_inicial_videoref.text):

                        if value :

                            self.connection_to_videoref()
                            self.ids.ip_videoref.readonly = True
                            self.ids.port_inicial_videoref.readonly = True

                        else:

                            self.disconnect_connection_to_videoref()
                            self.ids.ip_videoref.readonly = False
                            self.ids.port_inicial_videoref.readonly = False
            else:

                if value:

                    self.console_writer("WARNING", "El puerto de escucha inicial para el videoref no cumple con el formato adecuado")
                    self.ids.switch_videoref_connection.active = False
        else:

            if value:

                self.console_writer("WARNING", "La ip del videoref no cumple con el formato adecuado")
                self.ids.switch_videoref_connection.active = False

    def action_bar_connection_to_videoref(self):

        self.ids.switch_videoref_connection.active = True

    def action_bar_disconnect_connection_to_videoref(self):

        self.ids.switch_videoref_connection.active = False

    def connection_to_videoref(self):

        global videoref

        videoref.run(str(self.ids.ip_videoref.text), int(self.ids.port_inicial_videoref.text))

    def disconnect_connection_to_videoref(self):

        global videoref

        videoref.disconnect_connection()

    """
        funciones de hilo de hello del videoref
    """

    def sloop_send_hello_videoref(self):

        global repeated_send_hello

        global videoref

        active_data = videoref.return_data_active()

        if (repeated_send_hello != None) and (int(active_data) == 0):

            self.send_hello_videoref()

        if ((int(active_data) == 0)):

            self.hide_grid_result()

    def star_sloop_send_hello_videoref(self):

        global repeated_send_hello

        repeated_send_hello = SetInterval.SetInterval(1, self.sloop_send_hello_videoref)

    def stop_sloop_send_hello_videoref(self):

        global repeated_send_hello

        if repeated_send_hello != None:

            repeated_send_hello.stop()

    """
        funciones de los botones hello y coordinate
    """

    def send_hello_videoref(self):

        global videoref

        active = videoref.return_status_run()

        if active != None:

            videoref.respond_hello_videoref()

        else:

            self.console_writer("WARNING", "No es posible enviar el mensaje Hello al videoref, la conexion con el "+
                                "videpref no se encuentra establecida")

    def send_coordinates_videoref(self):

        global videoref

        active = videoref.return_status_run()

        if active != None:

            videoref.respond_coordinates_videoref()

        else:

            self.console_writer("WARNING", "No es posible enviar el mensaje Coordinate al videoref, la conexion con el "+
                                "videpref no se encuentra establecida")

    """
        función del switch de actualización de la data del engarde por el videoref
    """

    def switch_update_data_engarde_to_videoref(self, instance, value):

        global update_data_engarde

        update_data_engarde = value

    def return_value_update_data_engarde_to_videoref(self):

        global update_data_engarde

        return update_data_engarde

    """
        funciones de guardado de configuración de la aplicación
    """

    def save_configuration_app_screen(self):

        config = ConfigParser.ConfigParser()

        global encoding_title_combat

        try:

            filePath = os.path.relpath('app/configuration/app/app.ini')

            if config.read([ filePath ]):

                screen = "screen-" + str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1))

                file = open("app/configuration/app/app.ini", "w")

                title_combat = self.ids.input_title_combat.text

                if self.ids.change_wisget_combat_couple.state == "down":
                    type_combat = "couple"
                else:
                    type_combat = "team"

                if config.has_section(screen):

                    config.set(screen, "encoding_title_combat", encoding_title_combat)

                    config.set(screen, "input_title_combat", title_combat.encode('utf-8'))

                    config.set(screen, "width_title_bar", float(round(self.ids.width_title_bar.value, 2)))

                    config.set(screen, "size_title_bar", float(round(self.ids.size_title_bar.value, 2)))

                    config.set(screen, "type_combat", type_combat)

                    if type_combat == "couple":

                        config.set(screen, "font_size_name_athlete", int(self.ids.font_size_name_athlete.text))

                        config.set(screen, "length_name_athlete", int(self.ids.length_name_athlete.text))

                        config.set(screen, "timer_font_size", int(self.ids.timer_font_size.text))

                        config.set(screen, "match_font_size", int(self.ids.match_font_size.text))

                        config.set(screen, "points_font_size", int(self.ids.points_font_size.text))

                        config.set(screen, "font_size_title_combat", int(self.ids.font_size_title_combat.text))

                        config.set(screen, "name_athlete_left_x", float(round(self.ids.name_athlete_left_x.value,2)))

                        config.set(screen, "name_athlete_left_y", float(round(self.ids.name_athlete_left_y.value,2)))

                        config.set(screen, "country_flag_left_x", float(round(self.ids.country_flag_left_x.value,2)))

                        config.set(screen, "country_flag_left_y", float(round(self.ids.country_flag_left_y.value,2)))

                        config.set(screen, "light_athlete_left_x", float(round(self.ids.light_athlete_left_x.value,2)))

                        config.set(screen, "light_athlete_left_y", float(round(self.ids.light_athlete_left_y.value,2)))

                        config.set(screen, "punctuation_left_x", float(round(self.ids.punctuation_left_x.value,2)))

                        config.set(screen, "punctuation_left_y", float(round(self.ids.punctuation_left_y.value,2)))

                        config.set(screen, "name_athlete_right_x", float(round(self.ids.name_athlete_right_x.value,2)))

                        config.set(screen, "name_athlete_right_y", float(round(self.ids.name_athlete_right_y.value,2)))

                        config.set(screen, "country_flags_right_x", float(round(self.ids.country_flags_right_x.value,2)))

                        config.set(screen, "country_flags_right_y", float(round(self.ids.country_flags_right_y.value,2)))

                        config.set(screen, "light_right_x", float(round(self.ids.light_right_x.value,2)))

                        config.set(screen, "light_right_y", float(round(self.ids.light_right_y.value,2)))

                        config.set(screen, "punctuation_athlete_rift_x", float(round(self.ids.punctuation_athlete_rift_x.value,2)))

                        config.set(screen, "punctuation_athlete_rift_y", float(round(self.ids.punctuation_athlete_rift_y.value,2)))

                    else:

                        config.set(screen, "country_flags_left_x_team",float(round(self.ids.country_flags_left_x_team.value, 2)))

                        config.set(screen, "country_flags_left_y_team", float(round(self.ids.country_flags_left_y_team.value, 2)))

                        config.set(screen, "name_athlete_left_pos_x_team", float(round(self.ids.name_athlete_left_pos_x_team.value, 2)))

                        config.set(screen, "name_athlete_left_pos_y_team", float(round(self.ids.name_athlete_left_pos_y_team.value, 2)))

                        config.set(screen, "light_left_pos_x_team", float(round(self.ids.light_left_pos_x_team.value, 2)))

                        config.set(screen, "light_left_pos_y_team", float(round(self.ids.light_left_pos_y_team.value, 2)))

                        config.set(screen, "punctuation_left_pos_x_team", float(round(self.ids.punctuation_left_pos_x_team.value, 2)))

                        config.set(screen, "punctuation_left_pos_y_team", float(round(self.ids.punctuation_left_pos_y_team.value, 2)))

                        config.set(screen, "name_team_left_pos_x", float(round(self.ids.name_team_left_pos_x.value, 2)))

                        config.set(screen, "name_team_left_pos_y", float(round(self.ids.name_team_left_pos_y.value, 2)))

                        config.set(screen, "ponits_team_left_pos_x", float(round(self.ids.ponits_team_left_pos_x.value, 2)))

                        config.set(screen, "ponits_team_left_pos_y", float(round(self.ids.ponits_team_left_pos_y.value, 2)))

                        config.set(screen, "ponits_athlete_team_right_pos_x", float(round(self.ids.ponits_athlete_team_right_pos_x.value, 2)))

                        config.set(screen, "ponits_athlete_team_right_pos_y", float(round(self.ids.ponits_athlete_team_right_pos_y.value, 2)))

                        config.set(screen, "light_team_right_pos_x", float(round(self.ids.light_team_right_pos_x.value, 2)))

                        config.set(screen, "light_team_right_pos_y", float(round(self.ids.light_team_right_pos_y.value, 2)))

                        config.set(screen, "name_athlete_team_right_pos_x", float(round(self.ids.name_athlete_team_right_pos_x.value, 2)))

                        config.set(screen, "name_athlete_team_right_pos_y", float(round(self.ids.name_athlete_team_right_pos_y.value, 2)))

                        config.set(screen, "country_flags_team_right_pos_x", float(round(self.ids.country_flags_team_right_pos_x.value, 2)))

                        config.set(screen, "country_flags_team_right_pos_y", float(round(self.ids.country_flags_team_right_pos_y.value, 2)))

                        config.set(screen, "points_team_combat_right_pos_x",float(round(self.ids.points_team_combat_right_pos_x.value, 2)))

                        config.set(screen, "points_team_combat_right_pos_y", float(round(self.ids.points_team_combat_right_pos_y.value, 2)))

                        config.set(screen, "name_team_right_pos_x", float(round(self.ids.name_team_right_pos_x.value, 2)))

                        config.set(screen, "name_team_right_pos_y", float(round(self.ids.name_team_right_pos_y.value, 2)))

                        config.set(screen, "size_name_athlete_team", int(self.ids.size_name_athlete_team.text))

                        config.set(screen, "length_name_athlete_team", int(self.ids.length_name_athlete_team.text))

                        config.set(screen, "size_name_team", int(self.ids.size_name_team.text))

                        config.set(screen, "length_name_team", int(self.ids.length_name_team.text))

                        config.set(screen, "size_points_athlete_team", int(self.ids.size_points_athlete_team.text))

                        config.set(screen, "size_points_team", int(self.ids.size_points_team.text))

                        config.set(screen, "size_timer_team", int(self.ids.size_timer_team.text))

                        config.set(screen, "size_match_team", int(self.ids.size_match_team.text))


                else:

                    title_combat = self.ids.input_title_combat.text

                    config.add_section(screen)

                    config.set(screen, "encoding_title_combat", encoding_title_combat)

                    config.set(screen, "input_title_combat", title_combat.encode('utf-8'))

                    config.set(screen, "width_title_bar", float(round(self.ids.width_title_bar.value, 2)))

                    config.set(screen, "size_title_bar", float(round(self.ids.size_title_bar.value, 2)))

                    config.set(screen, "type_combat", type_combat)

                    if type_combat == "couple":

                        config.set(screen, "font_size_name_athlete", int(self.ids.font_size_name_athlete.text))

                        config.set(screen, "length_name_athlete", int(self.ids.length_name_athlete.text))

                        config.set(screen, "timer_font_size", int(self.ids.timer_font_size.text))

                        config.set(screen, "match_font_size", int(self.ids.match_font_size.text))

                        config.set(screen, "points_font_size", int(self.ids.points_font_size.text))

                        config.set(screen, "font_size_title_combat", int(self.ids.font_size_title_combat.text))

                        config.set(screen, "name_athlete_left_x", float(round(self.ids.name_athlete_left_x.value,2)))

                        config.set(screen, "name_athlete_left_y", float(round(self.ids.name_athlete_left_y.value,2)))

                        config.set(screen, "country_flag_left_x", float(round(self.ids.country_flag_left_x.value,2)))

                        config.set(screen, "country_flag_left_y", float(round(self.ids.country_flag_left_y.value,2)))

                        config.set(screen, "light_athlete_left_x", float(round(self.ids.light_athlete_left_x.value,2)))

                        config.set(screen, "light_athlete_left_y", float(round(self.ids.light_athlete_left_y.value,2)))

                        config.set(screen, "punctuation_left_x", float(round(self.ids.punctuation_left_x.value,2)))

                        config.set(screen, "punctuation_left_y", float(round(self.ids.punctuation_left_y.value,2)))

                        config.set(screen, "name_athlete_right_x", float(round(self.ids.name_athlete_right_x.value,2)))

                        config.set(screen, "name_athlete_right_y", float(round(self.ids.name_athlete_right_y.value,2)))

                        config.set(screen, "country_flags_right_x", float(round(self.ids.country_flags_right_x.value,2)))

                        config.set(screen, "country_flags_right_y", float(round(self.ids.country_flags_right_y.value,2)))

                        config.set(screen, "light_right_x", float(round(self.ids.light_right_x.value,2)))

                        config.set(screen, "light_right_y", float(round(self.ids.light_right_y.value,2)))

                        config.set(screen, "punctuation_athlete_rift_x", float(round(self.ids.punctuation_athlete_rift_x.value,2)))

                        config.set(screen, "punctuation_athlete_rift_y", float(round(self.ids.punctuation_athlete_rift_y.value,2)))

                    else:

                        config.set(screen, "country_flags_left_x_team",float(round(self.ids.country_flags_left_x_team.value, 2)))

                        config.set(screen, "country_flags_left_y_team",float(round(self.ids.country_flags_left_y_team.value, 2)))

                        config.set(screen, "name_athlete_left_pos_x_team",float(round(self.ids.name_athlete_left_pos_x_team.value, 2)))

                        config.set(screen, "name_athlete_left_pos_y_team",float(round(self.ids.name_athlete_left_pos_y_team.value, 2)))

                        config.set(screen, "light_left_pos_x_team",float(round(self.ids.light_left_pos_x_team.value, 2)))

                        config.set(screen, "light_left_pos_y_team",float(round(self.ids.light_left_pos_y_team.value, 2)))

                        config.set(screen, "punctuation_left_pos_x_team",float(round(self.ids.punctuation_left_pos_x_team.value, 2)))

                        config.set(screen, "punctuation_left_pos_y_team",float(round(self.ids.punctuation_left_pos_y_team.value, 2)))

                        config.set(screen, "name_team_left_pos_x", float(round(self.ids.name_team_left_pos_x.value, 2)))

                        config.set(screen, "name_team_left_pos_y", float(round(self.ids.name_team_left_pos_y.value, 2)))

                        config.set(screen, "ponits_team_left_pos_x", float(round(self.ids.ponits_team_left_pos_x.value, 2)))

                        config.set(screen, "ponits_team_left_pos_y", float(round(self.ids.ponits_team_left_pos_y.value, 2)))

                        config.set(screen, "ponits_athlete_team_right_pos_x",float(round(self.ids.ponits_athlete_team_right_pos_x.value, 2)))

                        config.set(screen, "ponits_athlete_team_right_pos_y",float(round(self.ids.ponits_athlete_team_right_pos_y.value, 2)))

                        config.set(screen, "light_team_right_pos_x",float(round(self.ids.light_team_right_pos_x.value, 2)))

                        config.set(screen, "light_team_right_pos_y",float(round(self.ids.light_team_right_pos_y.value, 2)))

                        config.set(screen, "name_athlete_team_right_pos_x",float(round(self.ids.name_athlete_team_right_pos_x.value, 2)))

                        config.set(screen, "name_athlete_team_right_pos_y",float(round(self.ids.name_athlete_team_right_pos_y.value, 2)))

                        config.set(screen, "country_flags_team_right_pos_x",float(round(self.ids.country_flags_team_right_pos_x.value, 2)))

                        config.set(screen, "country_flags_team_right_pos_y",float(round(self.ids.country_flags_team_right_pos_y.value, 2)))

                        config.set(screen, "points_team_combat_right_pos_x",float(round(self.ids.points_team_combat_right_pos_x.value, 2)))

                        config.set(screen, "points_team_combat_right_pos_y",float(round(self.ids.points_team_combat_right_pos_y.value, 2)))

                        config.set(screen, "name_team_right_pos_x",float(round(self.ids.name_team_right_pos_x.value, 2)))

                        config.set(screen, "name_team_right_pos_y",float(round(self.ids.name_team_right_pos_y.value, 2)))

                        config.set(screen, "size_name_athlete_team", int(self.ids.size_name_athlete_team.text))

                        config.set(screen, "length_name_athlete_team", int(self.ids.length_name_athlete_team.text))

                        config.set(screen, "size_name_team", int(self.ids.size_name_team.text))

                        config.set(screen, "length_name_team", int(self.ids.length_name_team.text))

                        config.set(screen, "size_points_athlete_team", int(self.ids.size_points_athlete_team.text))

                        config.set(screen, "size_points_team", int(self.ids.size_points_team.text))

                        config.set(screen, "size_timer_team", int(self.ids.size_timer_team.text))

                        config.set(screen, "size_match_team", int(self.ids.size_match_team.text))


                config.write(file)

                file.close()

                self.console_writer("INFO", "El archivo de configuración de la aplicación se a guardado correctamente")

            else:

                self.console_writer("WARNING", "El archivo de configuración para los ajustes de pantalla no ha podido ser cargado")

        except:

            self.console_writer("ERROR", "El archivo de configuración para los ajustes de pantalla ha presentado un error")

    def save_configuration_app_videoref(self):

        config = ConfigParser.ConfigParser()

        try:

            if re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.ids.ip_videoref.text):

                if re.search("^-?[0-9]+$", self.ids.port_inicial_videoref.text):

                    filePath = os.path.relpath('app/configuration/videoref/videoref.ini')

                    if config.read([filePath]):

                        section = "ip_config"

                        file = open("app/configuration/videoref/videoref.ini", "w")

                        if config.has_section(section):

                            config.set(section, "ip_videoref", str(self.ids.ip_videoref.text))

                            config.set(section, "port_inicial_videoref", str(self.ids.port_inicial_videoref.text))

                        else:

                            config.add_section(section)

                            config.set(section, "ip_videoref", str(self.ids.ip_videoref.text))

                            config.set(section, "port_inicial_videoref", str(self.ids.port_inicial_videoref.text))

                        config.write(file)

                        file.close()

                        self.console_writer("INFO", "El archivo de configuración del videoref se a guardado correctamente")


                    else:

                        self.console_writer("WARNING", "El archivo de configuración del videoref no ha podido ser cargado")
                else:

                    self.console_writer("WARNING",
                                        "El puerto de escucha inicial para el videoref no cumple con el formato adecuado")

            else:

                self.console_writer("WARNING", "La ip del videoref no cumple con el formato adecuado")

        except:

            self.console_writer("ERROR", "El archivo de configuración del videoref ha presentado un error")

    def save_configuration_app_engarde(self):

        config = ConfigParser.ConfigParser()

        try:

            if re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.ids.ip_engarde.text):

                if re.search("^-?[0-9]+$", self.ids.port_received_engarde.text):

                    if re.search("^-?[0-9]+$", self.ids.port_send_engarde.text):

                        filePath = os.path.relpath('app/configuration/engarde/engarde.ini')

                        if config.read([filePath]):

                            section = "ip_config"

                            file = open("app/configuration/engarde/engarde.ini", "w")

                            if config.has_section(section):

                                config.set(section, "ip_engarde", str(self.ids.ip_engarde.text))

                                config.set(section, "port_received_engarde", str(self.ids.port_received_engarde.text))

                                config.set(section, "port_send_engarde", str(self.ids.port_send_engarde.text))

                            else:

                                config.add_section(section)

                                config.set(section, "ip_engarde", str(self.ids.ip_engarde.text))

                                config.set(section, "port_received_engarde", str(self.ids.port_received_engarde.text))

                                config.set(section, "port_send_engarde", str(self.ids.port_send_engarde.text))

                            config.write(file)

                            file.close()

                            self.console_writer("INFO", "El archivo de configuración del engarde se a guardado correctamente")

                        else:

                            self.console_writer("WARNING", "El archivo de configuración del engarde no ha podido ser cargado")
                    else:

                        self.console_writer("WARNING",
                                            "El puerto de envio al engarde no cumple con el formato adecuado")

                else:

                    self.console_writer("WARNING",
                                        "El puerto de escucha para el engarde no cumple con el formato adecuado")

            else:

                self.console_writer("WARNING", "La ip del engarde no cumple con el formato adecuado")

        except:

            self.console_writer("ERROR", "El archivo de configuración del engarde ha presentado un error")

    """
        funciones de carga de configuracion de la aplicación
    """

    def load_configuration_app_screen(self):

        config = ConfigParser.ConfigParser()

        screen = "screen-" + str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1))

        filePath = os.path.relpath('app/configuration/app/app.ini')

        if config.read([ filePath ]):

            if config.has_section(screen):

                if config.has_option(screen, 'type_combat'):

                    self.change_widget_result_combat(config.get(screen, "type_combat"))

                    type_combat = config.get(screen, "type_combat")

                else:

                    self.change_widget_result_combat("couple")

                    type_combat = "couple"


                if  type_combat == "couple":

                    self.load_configuration_app_screen_couple()

                else:

                    self.load_configuration_app_screen_team()


            else:

                self.console_writer("WARNING",
                                             "El archivo de configuración de la aplicación no tiene ajustes para" +
                                             " esta resulucion de pantalla (" + str(GetSystemMetrics(0)) + "x"
                                             + str(GetSystemMetrics(1)) + ")")
        else:

            self.console_writer("WARNING",
                                         "El archivo de configuración de la aplicación no ha podido ser cargado")

    def load_configuration_app_screen_couple(self):

        config = ConfigParser.ConfigParser()

        screen = "screen-" + str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1))

        filePath = os.path.relpath('app/configuration/app/app.ini')

        if config.read([filePath]):

            if config.has_section(screen):

                if config.has_option(screen, 'encoding_title_combat'):
                    self.toggle_button_encoding(str(config.get(screen, "encoding_title_combat")))

                    self.encoding_grrid_result(str(config.get(screen, "encoding_title_combat")))

                if config.has_option(screen, 'input_title_combat'):
                    self.ids.input_title_combat.text = str(config.get(screen, "input_title_combat"))

                    self.ids.title_combat.text = str(config.get(screen, "input_title_combat"))

                if config.has_option(screen, 'width_title_bar'):
                    self.ids.width_title_bar.value = float(config.get(screen, "width_title_bar"))

                    self.ids.width_title_bar_text.text = str(config.get(screen, "width_title_bar"))

                if config.has_option(screen, 'size_title_bar'):
                    self.ids.size_title_bar.value = float(config.get(screen, "size_title_bar"))

                    self.ids.size_title_bar_text.text = str(config.get(screen, "size_title_bar"))


                if config.has_option(screen, 'font_size_name_athlete'):

                     self.ids.font_size_name_athlete.text = str(config.get(screen, "font_size_name_athlete"))

                if config.has_option(screen, 'length_name_athlete'):

                     self.ids.length_name_athlete.text = str(config.get(screen, "length_name_athlete"))

                if config.has_option(screen, 'timer_font_size'):

                     self.ids.timer_font_size.text = str(config.get(screen, "timer_font_size"))

                if config.has_option(screen, 'match_font_size'):

                     self.ids.match_font_size.text = str(config.get(screen, "match_font_size"))

                if config.has_option(screen, 'points_font_size'):

                     self.ids.points_font_size.text = str(config.get(screen, "points_font_size"))

                if config.has_option(screen, 'font_size_title_combat'):

                     self.ids.font_size_title_combat.text = str(config.get(screen, "font_size_title_combat"))

                if config.has_option(screen, 'name_athlete_left_x'):

                     self.ids.name_athlete_left_x.value = float(config.get(screen, "name_athlete_left_x"))

                     self.ids.name_athlete_left_x_text.text = str(config.get(screen, "name_athlete_left_x"))

                if config.has_option(screen, 'name_athlete_left_y'):

                      self.ids.name_athlete_left_y.value = float(config.get(screen, "name_athlete_left_y"))

                      self.ids.name_athlete_left_y_text.text = str(config.get(screen, "name_athlete_left_y"))

                if config.has_option(screen, 'country_flag_left_x'):

                      self.ids.country_flag_left_x.value = float(config.get(screen, "country_flag_left_x"))

                      self.ids.country_flag_left_x_text.text = str(config.get(screen, "country_flag_left_x"))

                if config.has_option(screen, 'country_flag_left_y'):

                      self.ids.country_flag_left_y.value = float(config.get(screen, "country_flag_left_y"))

                      self.ids.country_flag_left_y_text.text = str(config.get(screen, "country_flag_left_y"))

                if config.has_option(screen, 'light_athlete_left_x'):

                      self.ids.light_athlete_left_x.value = float(config.get(screen, "light_athlete_left_x"))

                      self.ids.light_athlete_left_x_text.text = str(config.get(screen, "light_athlete_left_x"))

                if config.has_option(screen, 'light_athlete_left_y'):

                       self.ids.light_athlete_left_y.value = float(config.get(screen, "light_athlete_left_y"))

                       self.ids.light_athlete_left_y_text.text = str(config.get(screen, "light_athlete_left_y"))

                if config.has_option(screen, 'punctuation_left_x'):

                       self.ids.punctuation_left_x.value = float(config.get(screen, "punctuation_left_x"))

                       self.ids.punctuation_left_x_text.text = str(config.get(screen, "punctuation_left_x"))

                if config.has_option(screen, 'punctuation_left_y'):

                       self.ids.punctuation_left_y.value = float(config.get(screen, "punctuation_left_y"))

                       self.ids.punctuation_left_y_text.text = str(config.get(screen, "punctuation_left_y"))

                if config.has_option(screen, 'name_athlete_right_x'):

                       self.ids.name_athlete_right_x.value = float(config.get(screen, "name_athlete_right_x"))

                       self.ids.name_athlete_right_x_text.text = str(config.get(screen, "name_athlete_right_x"))

                if config.has_option(screen, 'name_athlete_right_y'):

                        self.ids.name_athlete_right_y.value = float(config.get(screen, "name_athlete_right_y"))

                        self.ids.name_athlete_right_y_text.text = str(config.get(screen, "name_athlete_right_y"))

                if config.has_option(screen, 'country_flags_right_x'):

                        self.ids.country_flags_right_x.value = float(config.get(screen, "country_flags_right_x"))

                        self.ids.country_flags_right_x_text.text = str(config.get(screen, "country_flags_right_x"))

                if config.has_option(screen, 'country_flags_right_y'):

                        self.ids.country_flags_right_y.value = float(config.get(screen, "country_flags_right_y"))

                        self.ids.country_flags_right_y_text.text = str(config.get(screen, "country_flags_right_y"))

                if config.has_option(screen, 'light_right_x'):

                        self.ids.light_right_x.value = float(config.get(screen, "light_right_x"))

                        self.ids.light_right_x_text.text = str(config.get(screen, "light_right_x"))

                if config.has_option(screen, 'light_right_y'):

                        self.ids.light_right_y.value = float(config.get(screen, "light_right_y"))

                        self.ids.light_right_y_text.text = str(config.get(screen, "light_right_y"))

                if config.has_option(screen, 'punctuation_athlete_rift_x'):

                        self.ids.punctuation_athlete_rift_x.value = float(
                            config.get(screen, "punctuation_athlete_rift_x"))

                        self.ids.punctuation_athlete_rift_x_text.text = str(
                            config.get(screen, "punctuation_athlete_rift_x"))

                if config.has_option(screen, 'punctuation_athlete_rift_y'):

                        self.ids.punctuation_athlete_rift_y.value = float(
                            config.get(screen, "punctuation_athlete_rift_y"))

                        self.ids.punctuation_athlete_rift_y_text.text = str(
                            config.get(screen, "punctuation_athlete_rift_y"))

            else:

                self.console_writer("WARNING",
                                    "El archivo de configuración de la aplicación no tiene ajustes para" +
                                    " esta resulucion de pantalla (" + str(GetSystemMetrics(0)) + "x"
                                    + str(GetSystemMetrics(1)) + ")")
        else:

            self.console_writer("WARNING",
                                "El archivo de configuración de la aplicación no ha podido ser cargado")

    def load_configuration_app_screen_team(self):

        config = ConfigParser.ConfigParser()

        screen = "screen-" + str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1))

        filePath = os.path.relpath('app/configuration/app/app.ini')

        if config.read([filePath]):

            if config.has_section(screen):

                if config.has_option(screen, 'encoding_title_combat'):

                   self.toggle_button_encoding(str(config.get(screen, "encoding_title_combat")))

                   self.encoding_grrid_result(str(config.get(screen, "encoding_title_combat")))

                if config.has_option(screen, 'input_title_combat'):

                    self.ids.input_title_combat.text = str(config.get(screen, "input_title_combat"))

                    self.ids.title_combat.text = str(config.get(screen, "input_title_combat"))

                if config.has_option(screen, 'width_title_bar'):

                    self.ids.width_title_bar.value = float(config.get(screen, "width_title_bar"))

                    self.ids.width_title_bar_text.text = str(config.get(screen, "width_title_bar"))

                if config.has_option(screen, 'size_title_bar'):

                    self.ids.size_title_bar.value = float(config.get(screen, "size_title_bar"))

                    self.ids.size_title_bar_text.text = str(config.get(screen, "size_title_bar"))


                if config.has_option(screen, 'country_flags_left_x_team'):

                    self.ids.country_flags_left_x_team.value = float(config.get(screen, "country_flags_left_x_team"))

                    self.ids.country_flags_left_x_text_team.text = str(config.get(screen, "country_flags_left_x_team"))

                if config.has_option(screen, 'country_flags_left_y_team'):

                    self.ids.country_flags_left_y_team.value = float(config.get(screen, "country_flags_left_y_team"))

                    self.ids.country_flags_left_y_text_team.text = str(config.get(screen, "country_flags_left_y_team"))

                if config.has_option(screen, 'name_athlete_left_pos_x_team'):

                    self.ids.name_athlete_left_pos_x_team.value = float(config.get(screen, "name_athlete_left_pos_x_team"))

                    self.ids.name_athlete_left_pos_x_text_team.text = str(config.get(screen, "name_athlete_left_pos_x_team"))

                if config.has_option(screen, 'name_athlete_left_pos_y_team'):

                    self.ids.name_athlete_left_pos_y_team.value = float(config.get(screen, "name_athlete_left_pos_y_team"))

                    self.ids.name_athlete_left_pos_y_text_team.text = str(config.get(screen, "name_athlete_left_pos_y_team"))

                if config.has_option(screen, 'light_left_pos_x_team'):

                     self.ids.light_left_pos_x_team.value = float(config.get(screen, "light_left_pos_x_team"))

                     self.ids.light_left_pos_x_text_team.text = str(config.get(screen, "light_left_pos_x_team"))

                if config.has_option(screen, 'light_left_pos_y_team'):

                     self.ids.light_left_pos_y_team.value = float(config.get(screen, "light_left_pos_y_team"))

                     self.ids.light_left_pos_y_text_team.text = str(config.get(screen, "light_left_pos_y_team"))

                if config.has_option(screen, 'punctuation_left_pos_x_team'):

                     self.ids.punctuation_left_pos_x_team.value = float(config.get(screen, "punctuation_left_pos_x_team"))

                     self.ids.punctuation_left_pos_x_text_team.text = str(config.get(screen, "punctuation_left_pos_x_team"))

                if config.has_option(screen, 'punctuation_left_pos_y_team'):

                     self.ids.punctuation_left_pos_y_team.value = float(config.get(screen, "punctuation_left_pos_y_team"))

                     self.ids.punctuation_left_pos_y_text_team.text = str(config.get(screen, "punctuation_left_pos_y_team"))

                if config.has_option(screen, 'name_team_left_pos_x'):

                     self.ids.name_team_left_pos_x.value = float(config.get(screen, "name_team_left_pos_x"))

                     self.ids.name_team_left_pos_x_text.text = str(config.get(screen, "name_team_left_pos_x"))

                if config.has_option(screen, 'name_team_left_pos_y'):

                     self.ids.name_team_left_pos_y.value = float(config.get(screen, "name_team_left_pos_y"))

                     self.ids.name_team_left_pos_y_text.text = str(config.get(screen, "name_team_left_pos_y"))

                if config.has_option(screen, 'ponits_team_left_pos_x'):

                     self.ids.ponits_team_left_pos_x.value = float(config.get(screen, "ponits_team_left_pos_x"))

                     self.ids.ponits_team_left_pos_x_text.text = str(config.get(screen, "ponits_team_left_pos_x"))

                if config.has_option(screen, 'ponits_team_left_pos_y'):

                     self.ids.ponits_team_left_pos_y.value = float(config.get(screen, "ponits_team_left_pos_y"))

                     self.ids.ponits_team_left_pos_y_text.text = str(config.get(screen, "ponits_team_left_pos_y"))

                if config.has_option(screen, 'ponits_athlete_team_right_pos_x'):

                     self.ids.ponits_athlete_team_right_pos_x.value = float(config.get(screen, "ponits_athlete_team_right_pos_x"))

                     self.ids.ponits_athlete_team_right_pos_x_text.text = str(config.get(screen, "ponits_athlete_team_right_pos_x"))

                if config.has_option(screen, 'ponits_athlete_team_right_pos_y'):

                     self.ids.ponits_athlete_team_right_pos_x.value = float(config.get(screen, "ponits_athlete_team_right_pos_y"))

                     self.ids.ponits_athlete_team_right_pos_y_text.text = str(config.get(screen, "ponits_athlete_team_right_pos_y"))

                if config.has_option(screen, 'light_team_right_pos_x'):

                     self.ids.light_team_right_pos_x.value = float(config.get(screen, "light_team_right_pos_x"))

                     self.ids.light_team_right_pos_x_text.text = str(config.get(screen, "light_team_right_pos_x"))

                if config.has_option(screen, 'light_team_right_pos_y'):

                     self.ids.light_team_right_pos_y.value = float(config.get(screen, "light_team_right_pos_y"))

                     self.ids.light_team_right_pos_y_text.text = str(config.get(screen, "light_team_right_pos_y"))

                if config.has_option(screen, 'name_athlete_team_right_pos_x'):

                     self.ids.name_athlete_team_right_pos_x.value = float(config.get(screen, "name_athlete_team_right_pos_x"))

                     self.ids.name_athlete_team_right_pos_x_text.text = str(config.get(screen, "name_athlete_team_right_pos_x"))

                if config.has_option(screen, 'name_athlete_team_right_pos_y'):

                     self.ids.name_athlete_team_right_pos_y.value = float(config.get(screen, "name_athlete_team_right_pos_y"))

                     self.ids.name_athlete_team_right_pos_y_text.text = str(config.get(screen, "name_athlete_team_right_pos_y"))

                if config.has_option(screen, 'country_flags_team_right_pos_x'):

                     self.ids.country_flags_team_right_pos_x.value = float(config.get(screen, "country_flags_team_right_pos_x"))

                     self.ids.country_flags_team_right_pos_x_text.text = str(config.get(screen, "country_flags_team_right_pos_x"))

                if config.has_option(screen, 'country_flags_team_right_pos_y'):

                     self.ids.country_flags_team_right_pos_y.value = float(config.get(screen, "country_flags_team_right_pos_y"))

                     self.ids.country_flags_team_right_pos_y_text.text = str(config.get(screen, "country_flags_team_right_pos_y"))

                if config.has_option(screen, 'points_team_combat_right_pos_x'):

                     self.ids.points_team_combat_right_pos_x.value = float(config.get(screen, "points_team_combat_right_pos_x"))

                     self.ids.points_team_combat_right_pos_x_text.text = str(config.get(screen, "points_team_combat_right_pos_x"))

                if config.has_option(screen, 'points_team_combat_right_pos_y'):

                     self.ids.points_team_combat_right_pos_y.value = float(config.get(screen, "points_team_combat_right_pos_y"))

                     self.ids.points_team_combat_right_pos_y_text.text = str(config.get(screen, "points_team_combat_right_pos_y"))

                if config.has_option(screen, 'name_team_right_pos_x'):

                     self.ids.name_team_right_pos_x.value = float(config.get(screen, "name_team_right_pos_x"))

                     self.ids.name_team_right_pos_x_text.text = str(config.get(screen, "name_team_right_pos_x"))

                if config.has_option(screen, 'name_team_right_pos_y'):

                     self.ids.name_team_right_pos_y.value = float(config.get(screen, "name_team_right_pos_y"))

                     self.ids.name_team_right_pos_y_text.text = str(config.get(screen, "name_team_right_pos_y"))

                if config.has_option(screen, 'size_name_athlete_team'):

                     self.ids.size_name_athlete_team.text = str(config.get(screen, "size_name_athlete_team"))

                if config.has_option(screen, 'length_name_athlete_team'):

                     self.ids.length_name_athlete_team.text = str(config.get(screen, "length_name_athlete_team"))

                if config.has_option(screen, 'size_name_team'):
                    self.ids.size_name_team.text = str(config.get(screen, "size_name_team"))

                if config.has_option(screen, 'length_name_team'):
                    self.ids.length_name_team.text = str(config.get(screen, "length_name_team"))

                if config.has_option(screen, 'size_points_athlete_team'):
                    self.ids.size_points_athlete_team.text = str(config.get(screen, "size_points_athlete_team"))

                if config.has_option(screen, 'size_points_team'):
                    self.ids.size_points_team.text = str(config.get(screen, "size_points_team"))

                if config.has_option(screen, 'size_match_team'):
                    self.ids.size_match_team.text = str(config.get(screen, "size_match_team"))

                if config.has_option(screen, 'size_timer_team'):
                    self.ids.size_timer_team.text = str(config.get(screen, "size_timer_team"))

            else:

                self.console_writer("WARNING",
                                    "El archivo de configuración de la aplicación no tiene ajustes para" +
                                    " esta resulucion de pantalla (" + str(GetSystemMetrics(0)) + "x"
                                    + str(GetSystemMetrics(1)) + ")")
        else:

            self.console_writer("WARNING",
                                "El archivo de configuración de la aplicación no ha podido ser cargado")

    def load_configuration_app_videoref(self):

        config = ConfigParser.ConfigParser()

        section = "ip_config"

        filePath = os.path.relpath('app/configuration/videoref/videoref.ini')

        try:

            if config.read([filePath]):

                if config.has_section(section):

                    if config.has_option(section, 'ip_videoref'):

                        self.ids.ip_videoref.text = str(config.get(section, "ip_videoref"))

                    if config.has_option(section, 'port_inicial_videoref'):

                        self.ids.port_inicial_videoref.text = str(config.get(section, "port_inicial_videoref"))
            else:

                self.console_writer("WARNING",
                                    "El archivo de configuración del videoref no ha podido ser cargado")

        except:

            self.console_writer("ERROR", "El archivo de configuración del videoref ha presentado un error, por lo que "
                                + " no ha podido ser cargado en la aplicación")

    def load_configuration_app_engarde(self):

        config = ConfigParser.ConfigParser()

        section = "ip_config"

        filePath = os.path.relpath('app/configuration/engarde/engarde.ini')

        try:

            if config.read([filePath]):

                if config.has_section(section):

                    if config.has_option(section, 'ip_engarde'):

                        self.ids.ip_engarde.text = str(config.get(section, "ip_engarde"))

                    if config.has_option(section, 'port_received_engarde'):

                        self.ids.port_received_engarde.text = str(config.get(section, "port_received_engarde"))

                    if config.has_option(section, 'port_send_engarde'):

                        self.ids.port_send_engarde.text = str(config.get(section, "port_send_engarde"))
            else:

                self.console_writer("WARNING",
                                    "El archivo de configuración del engarde no ha podido ser cargado")

        except:

            self.console_writer("ERROR", "El archivo de configuración del engarde ha presentado un error, por lo que "
                                + " no ha podido ser cargado en la aplicación")

    def show_athlete_1(self):

        if self.ids.input_title_combat_1.text != "" and self.ids.input_title_combat_2.text != "":

            self.ids.athlete_name_pos_team.text = self.ids.input_title_combat_1.text
            self.ids.name_athlte_team_right_pos.text = self.ids.input_title_combat_2.text
            self.ids.nameAthleteLeft.text = self.ids.input_title_combat_1.text
            self.ids.nameAthleteRight.text = self.ids.input_title_combat_2.text

        else:

            self.console_writer("WARNING", "Introduzca el Nombre de los Esgrimistas")


    def show_team_1(self):

        if self.ids.team_nema_left_pos.text != "" and self.ids.team_name_right_pos.text != "":

            self.ids.team_nema_left_pos.text = self.ids.input_team_1.text
            self.ids.team_name_right_pos.text = self.ids.input_team_2.text

        else:

            self.console_writer("WARNING", "Introduzca el Nombre del equipo")