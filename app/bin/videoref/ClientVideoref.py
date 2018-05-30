#!/usr/bin/env python
#-*- coding: utf-8 -*-

import string
import datetime
import sys
import time

from kivy.app import App
if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor']

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import  reactor, protocol
from app.bin.engarde.ClientEngarde import ClientEngarde

engarde = ClientEngarde()

send_of_port = 0
UDP_SEND_IP = ""                      #IP DEL VIDEOREF 192.168.0.102
UDP_SEND_IP_ENGARDE = "127.0.0.1"     #IP DE LA MAQUINA DONDE ESTE CORRIENDO EL ENGARDE
UDP_PORT_LISTEN_VIDEOREF = 0          #PUERTO DE ESCUCHA INICIAL PARA EL VIDEOREF 50111
UDP_PORT_LISTEN_SEND_VIDEOREF = 60510
UDP_PORT_LISTEN_END_VIDEOREF = 60511  #PUERTO DE ESCUCHA DE RASPBERRY PARA RECIBIR DEL VIDEOREF
UDP_SEND_PORT_ENGARDE = 50100         #PUERTO DE ESCUCHA DEL ENGARDE
UDP_PORT_SEND_VIDEOREF = 0
listen_video_ref = None
socket_listen_videoref = None
socket_send_videoref = None
socket_listen_end_videoref = None
data_active = 0

class ClientListenFactory(protocol.DatagramProtocol):

    def __init__(self, app):
        self.app = app

    def startProtocol(self):

        global socket_listen_videoref

        global UDP_PORT_LISTEN_VIDEOREF

        socket_listen_videoref = self

        App.get_running_app().mainForm.console_writer("INFO", "El puerto de comunicacion con el videoref " +
                                                      str(UDP_PORT_LISTEN_VIDEOREF)  + "  esta activo")

    def datagramReceived(self,  datagram, (host, port)):

        global UDP_PORT_LISTEN_VIDEOREF

        App.get_running_app().mainForm.console_writer("INFO", "Datagrama recibido del videoref por el puerto de comunicacion " +
                                                      str(UDP_PORT_LISTEN_VIDEOREF) + ",  de la ip "
                                                      + str(host)  + ":" + str(port) + "\n"
                                                     + str(datagram))

        self.app.initial_reception(datagram, host, port)

class ClientSendFactory(protocol.DatagramProtocol):

    def __init__(self, app):
        self.app = app

    def startProtocol(self):

        global socket_send_videoref

        global UDP_PORT_LISTEN_SEND_VIDEOREF

        socket_send_videoref = self

        App.get_running_app().mainForm.console_writer("INFO", "El puerto de comunicacion con el videoref " +
                                                      str(UDP_PORT_LISTEN_SEND_VIDEOREF) + " esta activo")

    def datagramReceived(self,  datagram, (host, port)):

        global UDP_PORT_LISTEN_SEND_VIDEOREF

        App.get_running_app().mainForm.console_writer("INFO", "Datagrama recibido del videoref por el puerto de comunicacion " +
                                                      str(UDP_PORT_LISTEN_SEND_VIDEOREF) + ", de la ip " +
                                                      str(host) + ":" + str(port) + "\n" + str(datagram))

        def connectionRefused(self):

            App.get_running_app().mainForm.hide_grid_result()

class ClientListenEndFactory(protocol.DatagramProtocol):

    def __init__(self, app):
        self.app = app

    def startProtocol(self):

        global socket_listen_end_videoref

        global UDP_PORT_LISTEN_END_VIDEOREF

        socket_listen_end_videoref = self

        App.get_running_app().mainForm.console_writer("INFO", "El puerto de comunicacion con el videoref " +
                                                      str(UDP_PORT_LISTEN_END_VIDEOREF) + "  esta activo")

    def datagramReceived(self, datagram, (host, port)):

        global UDP_PORT_LISTEN_END_VIDEOREF

        global data_active

        data_active = 1

        App.get_running_app().mainForm.console_writer("INFO", "Datagrama recibido del videoref puerto de comunicacion " +
                                                      str(UDP_PORT_LISTEN_END_VIDEOREF) + "  de la ip " +
                                                      str(host) + ":" + str(port) + "\n" + str(datagram))

        if not App.get_running_app().mainForm.is_hide_result_grid:

           App.get_running_app().mainForm.display_result_grid()



        self.app.receive_info_videoref(datagram, host, port)

class ClientVideoref:


    def __init__(self):
        def __init__(self, **kwargs):
            super(ClientVideoref, self).__init__(**kwargs)

    """
        INICIA LOS SOCKET DE COMUNICACIÓN CON EL VIDEOREF
    """

    def run(self, ip_videoref, port_inicial_videoref):

        try:

            global listen_video_ref

            global UDP_PORT_LISTEN_VIDEOREF

            global UDP_PORT_LISTEN_SEND_VIDEOREF

            global UDP_PORT_LISTEN_END_VIDEOREF

            global UDP_SEND_IP

            UDP_SEND_IP = ip_videoref

            UDP_PORT_LISTEN_VIDEOREF = port_inicial_videoref

            if listen_video_ref == None:

                listen_video_ref = reactor.listenUDP(UDP_PORT_LISTEN_VIDEOREF, ClientListenFactory(self))

                listen_video_ref = reactor.listenUDP(UDP_PORT_LISTEN_SEND_VIDEOREF, ClientSendFactory(self))

                listen_video_ref = reactor.listenUDP(UDP_PORT_LISTEN_END_VIDEOREF, ClientListenEndFactory(self))

                App.get_running_app().mainForm.star_sloop_send_hello_videoref()

            else:

                App.get_running_app().mainForm.console_writer("WARNING",
                                                              "Ya se ha iniciado una comunicacion con el videoref")
        except:

            App.get_running_app().mainForm.console_writer("ERROR", "Los puertos de comunicacion con el videoref " +
                                                          "no se han podido iniciar correctamente." +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))

    """
        Retorna el estado del servidor (activo/inactivo)

    """

    def return_status_run(self):

        global listen_video_ref

        return listen_video_ref

    """
       CIERRA EL SOCKET DE COMUNICACIÓN CON EL VIDEOREF
    """

    def disconnect_connection(self):

        try:

            global listen_video_ref

            if listen_video_ref != None:

                reactor.disconnectAll()

                listen_video_ref = None

                App.get_running_app().mainForm.stop_sloop_send_hello_videoref()

                App.get_running_app().mainForm.display_result_grid()

                App.get_running_app().mainForm.console_writer("WARNING",
                                                              "La comunicacion con el videoref se ha cerrado correctamente.")
            else:

                App.get_running_app().mainForm.console_writer("WARNING",
                                                              "No se ha iniciado una comunicacion con el videoref.")


        except:

            App.get_running_app().mainForm.console_writer("ERROR", "Los puertos de comunicacion con el videoref " +
                                                          "no se han podido cerrar correctamente" +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))

    """
        RECEPCIÓN INICIAL DEL VIDEOREF (NOW YOU HAVE MY COORDINATES)
    """

    def initial_reception(self, data, udp_host_sen, udp_port_send):

       global UDP_PORT_SEND_VIDEOREF

       UDP_PORT_SEND_VIDEOREF = udp_port_send

       self.respond_coordinates_videoref()

       self.respond_hello_videoref()

    def respond_coordinates_videoref(self):

        global UDP_SEND_IP

        global UDP_PORT_SEND_VIDEOREF

        UDP_SEND_PORT = int(UDP_PORT_SEND_VIDEOREF) + 1

        message = "Now you have my coordinates"

        try:

            if (UDP_SEND_IP != "") and (int(UDP_PORT_SEND_VIDEOREF) != 0):

                socket_send_videoref.transport.write(message, (UDP_SEND_IP, UDP_SEND_PORT))

                App.get_running_app().mainForm.console_writer("INFO","El Mensaje " + message +
                                                              " se envio al videoref por la Ip " +
                                                              str(UDP_SEND_IP) + ":" + str(UDP_SEND_PORT))
        except:

            App.get_running_app().mainForm.console_writer("ERROR", "El Mensaje " + message +
                                                          " no pudo ser enviado al videoref por la Ip " +
                                                          str(UDP_SEND_IP) + ":" + str(UDP_SEND_PORT)  +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))

    def respond_hello_videoref(self):

        global UDP_SEND_IP

        global UDP_PORT_SEND_VIDEOREF

        UDP_SEND_PORT = int(UDP_PORT_SEND_VIDEOREF) + 1

        message = "|EFP1|HELLO|||||||||||||||%|"

        try:

            if (UDP_SEND_IP != "") and (int(UDP_PORT_SEND_VIDEOREF) != 0):

                socket_send_videoref.transport.write(message, (UDP_SEND_IP, UDP_SEND_PORT))

                App.get_running_app().mainForm.console_writer("INFO", "El Mensaje " + message +
                                                              " se envio al videoref por la Ip " +
                                                              str(UDP_SEND_IP) + ":" + str(UDP_SEND_PORT))

        except:

            App.get_running_app().mainForm.console_writer("ERROR", "El Mensaje " + message +
                                                          " no pudo ser enviado al videoref por la Ip " +
                                                          str(UDP_SEND_IP) + ":" + str(UDP_SEND_PORT) +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))

    """
        RECIBE INFO DEL VIDEOREF, RESPONDE DISP CON LA INFORMACION DEL ENGARDE, CAMBIA PUNTUACION CON INFORMACION
        DEL VIDEOREF Y ENVIA LA PUNTUACION AL ENGARDE.
    """

    def receive_info_videoref(self, data, udp_host_sen, udp_port_send):

        global UDP_PORT_SEND_VIDEOREF

        global data_active

        formatted_data_engarde = engarde.data_transfer_instance()

        update_engarde = App.get_running_app().mainForm.return_value_update_data_engarde_to_videoref()

        UDP_PORT_SEND_VIDEOREF = udp_port_send

        receive_data = string.split(data, '|')

        message = receive_data[2]

        today = datetime.datetime.now()

        formatted_data = {

            'competicion': receive_data[4],
            'mensaje': receive_data[2],
            'atleta_1': {'id': receive_data[19], 'nombre': receive_data[20], 'pais': receive_data[21],
                         'puntuacion': receive_data[22], 'status': receive_data[23], 'amarilla': receive_data[24],
                         'roja': receive_data[25], 'luz': receive_data[26], 'luzblanca': receive_data[27],
                         'intervencion': receive_data[28], 'respaldo': receive_data[29]},
            'atleta_2': {'id': receive_data[31], 'nombre': receive_data[32], 'pais': receive_data[33],
                         'puntuacion': receive_data[34], 'status': receive_data[35], 'amarilla': receive_data[36],
                         'roja': receive_data[37], 'luz': receive_data[38], 'luzblanca': receive_data[39],
                         'intervencion': receive_data[40], 'respaldo': receive_data[41]},
            'tiempo': receive_data[10],
            'evento': {'protocolo': receive_data[1], 'pista': receive_data[3], 'fase': receive_data[5],
                       'poul_tab': receive_data[6], 'match': receive_data[7], 'ronda': receive_data[8],
                       'tiempo_ini': receive_data[9], 'tipo': receive_data[11], 'arma': receive_data[12],
                       'prioridad': receive_data[13], 'estado': receive_data[14]},
            'arbitro': {'id_arbitro': receive_data[15], 'nombre_arbitro': receive_data[16],
                        'pais_arbitro': receive_data[17]}
        }


        cyrano = self.change_score(formatted_data_engarde, formatted_data)

        if update_engarde:

            self.send_cyrano_engarde(cyrano)

        data_active = 0

    def return_data_active(self):

        global data_active

        return int(data_active)

    def respond_disp_videoref(self, formatted_data_engarde, udp_host_sen, udp_port_send):

        global UDP_SEND_IP

        UDP_SEND_PORT = int(udp_port_send) + 1

        message = "|EFP1|DISP||||||||||" + formatted_data_engarde['evento']['arma'] + "||||||%||" + \
                  formatted_data_engarde['atleta_1']['nombre'] + "|" + formatted_data_engarde['atleta_1']['pais'] +\
                  "|||||||||%||" + formatted_data_engarde['atleta_2']['nombre'] + "|" + \
                  formatted_data_engarde['atleta_2']['pais'] + "|||||||||%|"

        try:

            socket_send_videoref.transport.write(message, (UDP_SEND_IP, UDP_SEND_PORT))

            App.get_running_app().mainForm.console_writer("INFO", "El Mensaje " + message +
                                                          " se envio al videoref por la Ip " +
                                                          str(udp_host_sen) + ":" + str(UDP_SEND_PORT))
        except:

            App.get_running_app().mainForm.console_writer("ERROR", "El Mensaje " + message +
                                                          " no pudo ser enviado al videoref por la Ip " +
                                                          str(udp_host_sen) + ":" + str(UDP_SEND_PORT) +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))

    @staticmethod
    def change_score(formatted_data_engarde, formatted_data):

        #athlete left

        name_athlte_left = str(formatted_data['atleta_2']['nombre'])

        if int(App.get_running_app().mainForm.ids.length_name_athlete) > 0:

            name_athlte_left = name_athlte_left[0:int(App.get_running_app().mainForm.ids.length_name_athlete)]

        App.get_running_app().mainForm.ids.timer.text = str(formatted_data['tiempo'])

        App.get_running_app().mainForm.ids.match.text = str(formatted_data['evento']['ronda'])

        App.get_running_app().mainForm.ids.nameAthleteLeft.text = str(
            formatted_data['atleta_2']['pais']) + "  " + name_athlte_left

        if int(formatted_data['atleta_2']['luz']) == 1:

            App.get_running_app().mainForm.ids.light_left.source = "resources/background/luz_roja.png"

            App.get_running_app().mainForm.ids.light_left.reload()

        elif int(formatted_data['atleta_2']['luzblanca']) == 1:

            App.get_running_app().mainForm.ids.light_left.source = "resources/background/luz-blanca.png"

            App.get_running_app().mainForm.ids.light_left.reload()

        elif int(formatted_data['atleta_2']['luz']) == 0 and int(formatted_data['atleta_2']['luzblanca']) == 0:

             App.get_running_app().mainForm.ids.light_left.source = "resources/background/luz_neutra.png"

             App.get_running_app().mainForm.ids.light_left.reload()

        App.get_running_app().mainForm.ids.pointsLeft.text = str(formatted_data['atleta_2']['puntuacion'])

        App.get_running_app().mainForm.ids.countryLeft.source = "resources/flags/flags_inclined/" + str(
             formatted_data['atleta_2']['pais']) + "-izquierda.png"

        App.get_running_app().mainForm.ids.countryLeft.reload()

        #athlete Right

        name_athlte_right = str(formatted_data['atleta_1']['nombre'])

        if int(App.get_running_app().mainForm.ids.length_name_athlete) > 0:
            name_athlte_right = name_athlte_right[0:int(App.get_running_app().mainForm.ids.length_name_athlete)]

        App.get_running_app().mainForm.ids.nameAthleteRight.text = name_athlte_right +\
                                                                   "  " + str(formatted_data['atleta_1']['pais'])

        if int(formatted_data['atleta_1']['luz']) == 1:

            App.get_running_app().mainForm.ids.light_right.source = "resources/background/luz_verde.png"

            App.get_running_app().mainForm.ids.light_right.reload()

        elif int(formatted_data['atleta_1']['luzblanca']) == 1:

            App.get_running_app().mainForm.ids.light_right.source = "resources/background/luz-blanca.png"

            App.get_running_app().mainForm.ids.light_right.reload()

        elif int(formatted_data['atleta_1']['luz']) == 0 and int(formatted_data['atleta_1']['luzblanca']) == 0:

             App.get_running_app().mainForm.ids.light_right.source = "resources/background/luz_neutra.png"

             App.get_running_app().mainForm.ids.light_right.reload()

        App.get_running_app().mainForm.ids.pointsRight.text = str(formatted_data['atleta_1']['puntuacion'])

        App.get_running_app().mainForm.ids.countryRight.source = "resources/flags/flags_inclined/" + str(
             formatted_data['atleta_1']['pais']) + "-derecha.png"

        App.get_running_app().mainForm.ids.countryRight.reload()

        return "|" + \
               formatted_data_engarde['evento']['protocolo'] + \
               "|INFO|" + \
               formatted_data_engarde['evento']['pista'] + "|" + \
               formatted_data_engarde['competicion'] + "|" + \
               formatted_data_engarde['evento']['fase'] + "|" + \
               formatted_data_engarde['evento']['poul_tab'] + "|" + \
               formatted_data_engarde['evento']['match'] + "|" + \
               formatted_data_engarde['evento']['ronda'] + "|" + \
               formatted_data_engarde['evento']['tiempo_ini'] + "|" + \
               formatted_data_engarde['tiempo'] + "|" + \
               formatted_data_engarde['evento']['tipo'] + "|" + \
               formatted_data_engarde['evento']['arma'] + "|" + \
               formatted_data_engarde['evento']['prioridad'] + "|" + \
               formatted_data_engarde['evento']['estado'] + "|" + \
               formatted_data_engarde['arbitro']['id_arbitro'] + "|" + \
               formatted_data_engarde['arbitro']['nombre_arbitro'] + "|" + \
               formatted_data_engarde['arbitro']['pais_arbitro'] + \
               "|%|" + \
               formatted_data_engarde['atleta_1']['id'] + "|" + \
               formatted_data_engarde['atleta_1']['nombre'] + "|" + \
               formatted_data_engarde['atleta_1']['pais'] + "|" + \
               formatted_data['atleta_1']['puntuacion'] + "|" + \
               formatted_data_engarde['atleta_1']['status'] + "|" + \
               formatted_data_engarde['atleta_1']['amarilla'] + "|" + \
               formatted_data_engarde['atleta_1']['roja'] + "|" + \
               formatted_data_engarde['atleta_1']['luz'] + "|" + \
               formatted_data_engarde['atleta_1']['luzblanca'] + "|" + \
               formatted_data_engarde['atleta_1']['intervencion'] + "|" + \
               formatted_data_engarde['atleta_1']['respaldo'] + "|%|" + \
               formatted_data_engarde['atleta_2']['id'] + "|" + \
               formatted_data_engarde['atleta_2']['nombre'] + "|" + \
               formatted_data_engarde['atleta_2']['pais'] + "|" + \
               formatted_data['atleta_2']['puntuacion'] + "|" + \
               formatted_data_engarde['atleta_2']['status'] + "|" + \
               formatted_data_engarde['atleta_2']['amarilla'] + "|" + \
               formatted_data_engarde['atleta_2']['roja'] + "|" + \
               formatted_data_engarde['atleta_2']['luz'] + "|" + \
               formatted_data_engarde['atleta_2']['luzblanca'] + "|" + \
               formatted_data_engarde['atleta_2']['intervencion'] + "|" + \
               formatted_data_engarde['atleta_2']['respaldo'] + "|%|"

    def send_cyrano_engarde(self, cyrano):

        global UDP_SEND_IP_ENGARDE

        global UDP_SEND_PORT_ENGARDE

        global socket_listen_end_videoref

        try:

            socket_listen_end_videoref.transport.write(cyrano, (UDP_SEND_IP_ENGARDE, UDP_SEND_PORT_ENGARDE))

            App.get_running_app().mainForm.console_writer("INFO", "El Mensaje " + str(cyrano) +
                                                          " se envio al engarde por la Ip " +
                                                          str(UDP_SEND_IP_ENGARDE) + ":" + str(UDP_SEND_PORT_ENGARDE))
        except:

            App.get_running_app().mainForm.console_writer("ERROR", "El Mensaje " + cyrano +
                                                          " no pudo ser enviado al engarde por la Ip " +
                                                          str(UDP_SEND_IP_ENGARDE) + ":" + str(UDP_SEND_PORT_ENGARDE) +
                                                          ", datos del error:\n" + str(sys.exc_info()[0]))
