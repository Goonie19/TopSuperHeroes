#!/usr/bin/python2

import pika
import os
import sys
import tweepy
import time
import paginas_drive.classy as gs
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import 

proyecto_sd = gs.drive() # instacia para abstraer el drive, necesaria para comunicarse con drive

hoja = proyecto_sd.nueva_hoja("Heroes") # creamos la hoja donde iremos actualizando las páginas
proyecto_sd.nueva_pagina("Heroes","Marvel") #completar
proyecto_sd.nueva_pagina("Heroes","dc") #completar

con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = con.channel()

gauth = GoogleAuth()
gauth.LoadCredentialsFile("client_id.json")
drive = GoogleDrive(gauth)

marvel = []
dc = []
contadores = []

CONSUMER_KEY = '9MgHe4rbqjnKi3Kn5YSAtl6Kv'

CONSUMER_SECRET = 'kI9PzNX7MvMjYXFfGfsZLrvcKzIRW9ZosTc5rMUBmwEqgP1T9U'

ACCESS_KEY = '1123125102898495488-ATNY3FO9pKAWqUdPU3escdwKW45M0y'

ACCESS_SECRET = 'It281zL407ccZLhjRAi3twaOXuZze79s06nqhXqVo4fgv'

twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(twitter)

def marvel():
	return marvel

def dc():
	return dc

heroes = ['#CapitanAmerica', '#IronMan', '#Thor', '#Hulk', '#BlackWidow', '#SpiderMan',
'#Falcon', '#WinterSoldier', '#CapitanaMarvel', '#HawkEye', '#AntMan', '#Valkiria', 
'#Batman', '#SuperMan', '#AquaMan', '#PoisonIvy', '#Shazam', '#WonderWoman', '#GreenLantern', 
'#Flash', '#NightWind', '#GreenArrow', '#CatWoman', '#DrFate', '#Raven', 'HawkMan']

inputs = {'Marvel': marvel(), 'dc': dc()}

def contarTweets(consulta, array):
	resultados = api.search(consulta)
	cont = 0
	for lista in resultados:
		cont += lista.favorite_count
	marvel[consulta] = cont


#Arreglar para que coja el top 5 con lista.pop(indice)
def topSuperHeroesMarvel():
	array = []
	i = 0
	c = 0
	max = 0
	max2 = 9999999
	cadena = ""
	while c < 4:
		while i < 12:
			if (marvel[heroes[i]] > max):
				max = marvel[heroes[i]]
				cadena = heroes[i]
				i += 1
			else
				i += 1
		i = 0
		c += 1
		max = 0
		array.append(cadena)




def llamadaMarvel():
	i = 0
	for n in heroes:
		if(i < 12):
			contarTweets(heroes[i], marvel)
		i += 1

def llamadaDC():
	i = 0
	for n in heroes:
		if(i >= 12):
			contarTweets(heroes[i], dc)
		i += 1

def topSuperHeroesDC():


def callBack(ch, method, properties, body):
	if(body == 'Marvel' or body == '@top_heroes Marvel'):
		print(" Recogiendo información sobre la popularidad de los heroes de Marvel")
		llamadaMarvel()
		top = topSuperHeroes()
		cadena = "Este es el top de popularidad de los heroes de Marvel.\nTop 1: " + top[0] + "\nTop 2: " + top[1] + 
		"\nTop 3: " + top[2] + "\nTop 4: " + top[3] + "\nTop 5:" + top[4]
		#añadir creacion de fichero y subida a drive
	else if(body == 'DC' or body == '@top_heroes DC'):
		print(" Recogiendo información sobre la popularidad de los heroes de DC")
		llamadaDC()
		top = topSuperHeroes()
		cadena = "Este es el top de popularidad de los heroes de Marvel.\nTop 1: " + top[0] + "\nTop 2: " + top[1] + 
		"\nTop 3: " + top[2] + "\nTop 4: " + top[3] + "\nTop 5:" + top[4]


		
