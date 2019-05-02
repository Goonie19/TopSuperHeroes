#!/usr/bin/python2

import pika
import os
import tweepy
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import tkinter
import pickle
import time
import paginas_drive.classy as gs


def server():
    con = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    canal = con.channel()
    canal.queue_declare(queue = 'topCola', durable = True)

    CONSUMER_KEY = '9MgHe4rbqjnKi3Kn5YSAtl6Kv'

    CONSUMER_SECRET = 'kI9PzNX7MvMjYXFfGfsZLrvcKzIRW9ZosTc5rMUBmwEqgP1T9U'

    ACCESS_KEY = '1123125102898495488-ATNY3FO9pKAWqUdPU3escdwKW45M0y'

    ACCESS_SECRET = 'It281zL407ccZLhjRAi3twaOXuZze79s06nqhXqVo4fgv'

    twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.api(tw)

    proyecto_sd = gs.drive() # instacia para abstraer el drive, necesaria para comunicarse con drive

    hoja = proyecto_sd.nueva_hoja("Heroes") # creamos la hoja donde iremos actualizando las páginas
    proyecto_sd.nueva_pagina("Heroes","Marvel") #completar
    proyecto_sd.nueva_pagina("Heroes","dc") #completar


    while True:
        md = api.direct_messages()
        print(md[0].text)
        for msg in md:
            if(msg.text == 'Marvel' or msg.text =='DC'):
                canal.basic_publish(exchange = '',
                    routing_key = 'topCola',
                    body = msg.text,
                    properties = None)
            else:
                print "Debe introducir Marvel o DC."

        time.sleep(1000)
            
    con.close()

if __name__ == '__main__':
    print("Servidor preparado")
    server()
