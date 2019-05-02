#!/usr/bin/python2

import zmq
import os
import tweepy
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import tkinter
import pickle
import time
import paginas_drive.classy as gs

proyecto_sd = gs.drive() # instacia para abstraer el drive, necesaria para comunicarse con drive

hoja = proyecto_sd.nueva_hoja("Heroes") # creamos la hoja donde iremos actualizando las páginas
proyecto_sd.nueva_pagina("Heroes","Marvel") #completar
proyecto_sd.nueva_pagina("Heroes","dc") #completar

def server():
  context = zmq.Context(1)
    sock = context.socket(zmq.REP) # REP
    sock.bind('tcp://*:4545')

    # Conection with worker
    worker = context.socket(zmq.REQ) # PUSH
    worker.bind("tcp://*:4546")
  
    # Start the server loop
    while True:
        msg = sock.recv()
        msg = msg.decode("utf-8")
        print("Campo de estudio: " , msg)
        if(msg == "marvel" or msg == "dc"):
            worker.send_string(msg)
            url = worker.recv() 
            url = url.decode("utf-8")
            print("url: " + url)
 
        else:
            url = "Error."

        # We share the path and we end comunications
        sock.send_string(url, zmq.SNDMORE)
        sock.send_string("fin")
            

if __name__ == '__main__':
    print("Servidor preparado")
    server()
