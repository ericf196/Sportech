#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Importación de módulos propios de python.

"""
import string
import datetime
import json
import requests


class RequestToServer:

    def __init__(self):
        def __init__(self, **kwargs):
            super(RequestToServer, self).__init__(**kwargs)

    def save_information(self, formatted_data):
        # data = {"data": json.dumps(formatted_data)}
        # resp = requests.post('http://live-result.sportech37.com/api/data', params=data)
        # print resp.text
        print "Data enviada al servidor"