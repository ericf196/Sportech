#!/usr/bin/env python
#-*- coding: utf-8 -*-

import string
import datetime
import sys
import re

from kivy.app import App
if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor']
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol

from app.bin.request_to_server_sportech import RequestToServer # Módulo de interacción con el servidor Sportech37

sportechServer = RequestToServer.RequestToServer()

UDP_PORT_RECEIVED = 0 #50103
server_received = None
socket_received = None
UDP_SEND_PORT = 0 # 50100
UDP_SEND_IP = "" # 192.168.0.102
formatted_data = {
                'competicion': '',
                'mensaje': '',
                'atleta_1': {'id': '', 'nombre': '', 'pais': '',
                             'puntuacion': '', 'status': '', 'amarilla': '',
                             'roja': '', 'luz': '', 'luzblanca': '',
                             'intervencion': '', 'respaldo': ''},
                'atleta_2': {'id': '', 'nombre': '', 'pais': '',
                             'puntuacion': '', 'status': '', 'amarilla': '',
                             'roja': '', 'luz': '', 'luzblanca': '',
                             'intervencion': '', 'respaldo': ''},
                'tiempo': '',
                'evento': {'protocolo': '', 'pista': '', 'fase': '',
                           'poul_tab': '', 'match': '', 'ronda': '',
                           'tiempo_ini': '', 'tipo': '', 'arma': '',
                           'prioridad': '', 'estado': ''},
                'arbitro': {'id_arbitro': '', 'nombre_arbitro': '',
                            'pais_arbitro': ''}
            }

class ClientThreadFactory(protocol.DatagramProtocol):

    def __init__(self, app):
        self.app = app

    def startProtocol(self):

        global socket_received

        global UDP_PORT_RECEIVED

        socket_received = self

        App.get_running_app().mainForm.console_writer("INFO", "El puerto de comunicacion con el engarde " +
                                                      str(UDP_PORT_RECEIVED) + " se encuentra activo")

    def datagramReceived(self,  datagram, (host, port)):

        global UDP_PORT_RECEIVED

        App.get_running_app().mainForm.console_writer("INFO", "Datagrama recibido del engarde por el puerto de comunicacion " +
                                                      str(UDP_PORT_RECEIVED) + ",  de la ip "
                                                      + str(host) + ":" + str(port) + "\n"
                                                      + str(datagram))
        self.app.engarde_data(datagram)

class ClientEngarde:

    def __init__(self):
        def __init__(self, **kwargs):
            super(ClientEngarde, self).__init__(**kwargs)

    """
        INICIA EL SOCKET DE COMUNICACIÓN CON EL ENGARDE

    """

    def run(self, ip_engarde, port_received_engarde, port_send_engarde):

        global UDP_PORT_RECEIVED

        global UDP_SEND_PORT

        global UDP_SEND_IP

        global server_received

        if server_received == None:

            try:

                UDP_PORT_RECEIVED = port_received_engarde

                UDP_SEND_PORT = port_send_engarde

                UDP_SEND_IP = ip_engarde

                if re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", UDP_SEND_IP):

                    if re.search("^-?[0-9]+$", str(UDP_PORT_RECEIVED)):

                        if re.search("^-?[0-9]+$", str(UDP_SEND_PORT)):

                            server_received = reactor.listenUDP(UDP_PORT_RECEIVED, ClientThreadFactory(self))

                        else:

                            App.get_running_app().mainForm.console_writer("WARNING",
                                                                          "El puerto de envio al engarde no cumple con" +
                                                                          " el formato adecuado")
                    else:

                        App.get_running_app().mainForm.console_writer("WARNING",
                                                                      "El puerto de escucha para el engarde no cumple" +
                                                                      " con el formato adecuado")
                else:

                    App.get_running_app().mainForm.console_writer("WARNING",
                                                                  "La ip del engrde no cumple con el formato adecuado")
            except:

                App.get_running_app().mainForm.console_writer("ERROR", "Los puertos de comunicacion con el engarde no se "
                                                              + "pudieron iniciar correctamente." +
                                                              ", datos del error:\n" + str(sys.exc_info()[0]))
        else:

            App.get_running_app().mainForm.console_writer("WARNING", "La conexión con el engarde ya se encuentra establecida")

    """
        CIERRA EL SOCKET DE COMUNICACIÓN CON EL ENGARDE

    """

    def disconnect_connection(self):

        global server_received

        global socket_received

        try:

            if server_received != None:

                server_received.stopListening()

                server_received = None

                socket_received = None

                self.clear_result_in_panel()

                App.get_running_app().mainForm.console_writer("WARNING",
                                                              "La conexion con el engarde se ha cerrado")
            else:

                App.get_running_app().mainForm.console_writer("WARNING",
                                                              "La conexion con el engarde no se encuentra establecida")
        except:

            App.get_running_app().mainForm.console_writer("ERROR", "Los puertos de comunicacion con el engarde " +
                                                          "no se han podido cerrar correctamente." +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))

    "Retorna el estado del servidor (activo/inactivo)"

    def return_status_run(self):

        global server_received

        return server_received

    """
        RRECIBE INFORMACION DEL ENGARDE Y LA IMPRIME EN PANTALLA, MANDA ESTA INFORMACION A LA URL DE LIVE-RESULT

    """
    def engarde_data(self, data):

        global formatted_data

        global sportechServer

        receives_data = string.split(data, '|')

        message = receives_data[2]

        if message == 'INFO' or message == 'DISP':
            formatted_data = {
                'competicion': receives_data[4],
                'mensaje': receives_data[2],
                'atleta_1': {'id': receives_data[19], 'nombre': receives_data[20], 'pais': receives_data[21],
                             'puntuacion': receives_data[22], 'status': receives_data[23], 'amarilla': receives_data[24],
                             'roja': receives_data[25], 'luz': receives_data[26], 'luzblanca': receives_data[27],
                             'intervencion': receives_data[28], 'respaldo': receives_data[29]},
                'atleta_2': {'id': receives_data[31], 'nombre': receives_data[32], 'pais': receives_data[33],
                             'puntuacion': receives_data[34], 'status': receives_data[35], 'amarilla': receives_data[36],
                             'roja': receives_data[37], 'luz': receives_data[38], 'luzblanca': receives_data[39],
                             'intervencion': receives_data[40], 'respaldo': receives_data[41]},
                'tiempo': receives_data[10],
                'evento': {'protocolo': receives_data[1], 'pista': receives_data[3], 'fase': receives_data[5],
                           'poul_tab': receives_data[6], 'match': receives_data[7], 'ronda': receives_data[8],
                           'tiempo_ini': receives_data[9], 'tipo': receives_data[11], 'arma': receives_data[12],
                           'prioridad': receives_data[13], 'estado': receives_data[14]},
                'arbitro': {'id_arbitro': receives_data[15], 'nombre_arbitro': receives_data[16],
                            'pais_arbitro': receives_data[17]}
            }

            self.result_to_panel(formatted_data)

            sportechServer.save_information(formatted_data)

    def result_to_panel(self, data):

        App.get_running_app().mainForm.ids.nameAthleteLeft.text = str(data['atleta_1']['nombre']) + "  " + str(data['atleta_1']['pais'])
        App.get_running_app().mainForm.ids.countryLeft.source = "resources/flags/flags_inclined/" + str(data['atleta_1']['pais']) + "-izquierda.png"
        App.get_running_app().mainForm.ids.countryLeft.reload()
        App.get_running_app().mainForm.ids.pointsLeft.text = "    " + str(formatted_data['atleta_1']['puntuacion'])
        App.get_running_app().mainForm.ids.nameAthleteRight.text = str(formatted_data['atleta_2']['nombre']) + "  " + str(formatted_data['atleta_2']['pais'])
        App.get_running_app().mainForm.ids.countryRight.source = "resources/flags/flags_inclined/" + str(formatted_data['atleta_2']['pais']) + "-derecha.png"
        App.get_running_app().mainForm.ids.countryRight.reload()
        App.get_running_app().mainForm.ids.pointsRight.text = str(formatted_data['atleta_2']['puntuacion']) + "    "
        App.get_running_app().mainForm.ids.timer.text = str(formatted_data['tiempo'])
        App.get_running_app().mainForm.ids.match.text = str(formatted_data['evento']['match'])

    def data_transfer_instance(self):

        global formatted_data

        return formatted_data

    """
        Limpia el panel de resultado

    """

    def clear_result_in_panel(self):

        App.get_running_app().mainForm.ids.nameAthleteRight.text = ""
        App.get_running_app().mainForm.ids.countryRight.source = ""
        App.get_running_app().mainForm.ids.countryRight.reload()
        App.get_running_app().mainForm.ids.pointsRight.text = ""
        App.get_running_app().mainForm.ids.nameAthleteLeft.text = ""
        App.get_running_app().mainForm.ids.countryLeft.source = ""
        App.get_running_app().mainForm.ids.countryLeft.reload()
        App.get_running_app().mainForm.ids.pointsLeft.text = ""
        App.get_running_app().mainForm.ids.timer.text = "00:00"
        App.get_running_app().mainForm.ids.match.text = "0"

    """
        CAMBIAR COMBATES DEL ENGARDE --- NUEVO

    """

    def next_combat(self):

        return "|EFP1|NEXT|1|fm-eq|%|"

    def previous_combat(self):

        return "|EFP1|PREV|1|fm-eq|%|"

    def submit_cyrano(self, message, option):

         try:

            global UDP_SEND_PORT

            global UDP_SEND_IP

            global socket_received

            if re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", str(UDP_SEND_IP)):

                if re.search("^-?[0-9]+$", str(UDP_SEND_PORT)):

                    socket_received.transport.write(message, (UDP_SEND_IP, UDP_SEND_PORT))

                    if option == 1:

                        App.get_running_app().mainForm.console_writer("INFO",
                                                                      "Se a pasado al siguiente combate del  engarde")
                    else:

                        App.get_running_app().mainForm.console_writer("INFO",
                                                                      "Se a pasado al combate anterior del engarde")
                else:

                    App.get_running_app().mainForm.console_writer("ERROR",
                                                                  "La ip de envio al engarde no cumple con el formato adecuado")
            else:

                App.get_running_app().mainForm.console_writer("ERROR",
                                                              "El puerto de envio al engarde no cumple con el formato adecuado")
         except:

             App.get_running_app().mainForm.console_writer("ERROR",
                                                           "El mensaje " + message + ", de cambio de combate no pudo ser enviado "
                                                           + "a la Ip " + str(UDP_SEND_IP) + ":" + str(UDP_SEND_PORT) +
                                                           ", datos del error\n" + str(sys.exc_info()[0]))

    def change_combat_engarde(self, option):

        if server_received != None:

            if option == 1:
                cyrano = self.next_combat()
                self.submit_cyrano(cyrano, 1)

            if option == 2:
                cyrano = self.previous_combat()
                self.submit_cyrano(cyrano, 2)
        else:

            App.get_running_app().mainForm.console_writer("WARNING",
                                                          "La conexion con el engarde no se encuentra establecida")

