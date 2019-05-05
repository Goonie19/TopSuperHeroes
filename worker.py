#!/usr/bin/python2
#coding=utf-8
import pika
import os
import sys
import tweepy
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = con.channel()

gauth = GoogleAuth()
if not os.path.exists("client_secrets.json"):
	gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

marvel = []
dc = []

contadoresmarvel = []
contadoresdc = []

CONSUMER_KEY = ''

CONSUMER_SECRET = ''

ACCESS_KEY = ''

ACCESS_SECRET = ''

twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(twitter)

heroesMarvel = ['Capitan America', 'IronMan', 'Thor', 'Hulk', 'Black Widow', ' Spider-Man', 'Falcon', 'Winter Soldier', 'Capitana Marvel', 'HawkEye', 'AntMan', 'Valkiria']
heroesDC = ['Batman', 'SuperMan', 'AquaMan', 'PoisonIvy', 'Shazam', 'WonderWoman', 'GreenLantern', 'Flash', 'NightWind', 'GreenArrow', 'CatWoman', 'DrFate', 'Raven', 'HawkMan']

file1 = drive.CreateFile({'title': 'heroesMarvel.txt'})
file2 = drive.CreateFile({'title': 'heroesDC.txt'})

def contarTweets(consulta):
	resultados = api.search(consulta, count=2000)
	cont = len(resultados)
	return cont


#Arreglar para que coja el top 5 con lista.pop(indice)
def topSuperHeroesMarvel():
	listMarvel = []
	i = 0
	c = 0
	cadena = ""
	max = 0
	max2 = 999999999999
	while c < 5:
		while i < len(marvel) and i < len(heroesMarvel):
			if(marvel[i] > max and marvel[i] < max2):
				max = marvel[i]
				cadena = heroesMarvel[i]
			i += 1
		contadoresmarvel.insert(c, max)
		c += 1
		max2 = max
		max = 0
		i=0
		listMarvel.insert(c, cadena)
	return listMarvel

def llamadaMarvel():
	i = 0
	for n in heroesMarvel:
		marvel.append(contarTweets(n))
		i += 1

def llamadaDC():
	i = 0
	for n in heroesDC:
		dc.insert(i, contarTweets(n))
		i += 1

def topSuperHeroesDC():
	listDC = []
	i = 0
	c = 0
	cadena = ""
	max = 0
	max2 = 999999999999
	while c < 5:
		while i < len(dc) and i< len(heroesDC):
			if(dc[i] > max and dc[i] < max2):
				max = dc[i]
				cadena = heroesDC[i]
			i += 1
		contadoresdc.insert(c, max)
		c += 1
		max2 = max
		max = 0
		i=0
		listDC.insert(c, cadena)
	return listDC


def callBack(ch, method, properties, body):
	text = body.split("|")
	if(text[0] == 'Marvel' or text[0] == '@top_heroes Marvel'):
		print("Recogiendo información sobre la popularidad de los heroes de Marvel")
		llamadaMarvel()
		topmarvel = topSuperHeroesMarvel()
		cadena = "Este es el top de popularidad de los heroes de Marvel.\nTop 1: " + topmarvel[0] + "\nTop 2: " + topmarvel[1] + "\nTop 3: " + topmarvel[2] + "\nTop 4: " + topmarvel[3] + "\nTop 5: " + topmarvel[4]
		cadena2 = "Este es el top de popularidad de los heroes de Marvel.\nTop 1: " + topmarvel[0]+ " Con " + str(contadoresmarvel[0]) + " tweets" + "\nTop 2: " + topmarvel[1] + " Con " + str(contadoresmarvel[1]) + " tweets" + "\nTop 3: " + topmarvel[2] + " Con " + str(contadoresmarvel[2]) + " tweets" + "\nTop 4: " + topmarvel[3] + " Con " + str(contadoresmarvel[3]) + " tweets" + "\nTop 5: " + topmarvel[4] + " Con " + str(contadoresmarvel[4]) + " tweets" 

		#añadir creacion de fichero y subida a drive
		file1.SetContentString(cadena2)
		file1.Upload() # Files.insert()
		api.update_status("@"+text[2]+" " + cadena, int(text[1]))
		time.sleep(body.count(b'.'))
	elif(text[0] == 'DC' or text[0] == '@top_heroes DC'):
		print("Recogiendo información sobre la popularidad de los heroes de DC")
		llamadaDC()
		top = topSuperHeroesDC()
		cadena = "Este es el top de popularidad de los heroes de DC.\nTop 1: " + top[0] + "\nTop 2: " + top[1] + "\nTop 3: " + top[2] + "\nTop 4: " + top[3] + "\nTop 5: " + top[4]
		cadena2 = "Este es el top de popularidad de los heroes de DC.\nTop 1: " + top[0]+ " Con " + str(contadoresdc[0]) + " tweets" + "\nTop 2: " + top[1] + " Con " + str(contadoresdc[1]) + " tweets" + "\nTop 3: " + top[2] + " Con " + str(contadoresdc[2]) + " tweets" + "\nTop 4: " + top[3] + " Con " + str(contadoresdc[3]) + " tweets" + "\nTop 5: " + top[4] + " Con " + str(contadoresdc[4]) + " tweets" 
		#creacion de fichero y subida drive
		file2.SetContentString(cadena2)
		file2.Upload() # Files.insert()
		api.update_status("@"+text[2]+" " + cadena, int(text[1]))
		time.sleep(body.count(b'.'))


channel.basic_qos(prefetch_count = 0)
channel.basic_consume(queue='topCola', on_message_callback=callBack, auto_ack = True)
channel.start_consuming()
