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
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

marvel = []
dc = []

CONSUMER_KEY = '9MgHe4rbqjnKi3Kn5YSAtl6Kv'

CONSUMER_SECRET = 'kI9PzNX7MvMjYXFfGfsZLrvcKzIRW9ZosTc5rMUBmwEqgP1T9U'

ACCESS_KEY = '1123125102898495488-ATNY3FO9pKAWqUdPU3escdwKW45M0y'

ACCESS_SECRET = 'It281zL407ccZLhjRAi3twaOXuZze79s06nqhXqVo4fgv'

twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(twitter)

heroesMarvel = ['Capitan America', 'IronMan', 'Thor', 'Hulk', 'Black Widow', ' Spider-Man', 'Falcon', 'Winter Soldier', 'Capitana Marvel', 'HawkEye', 'AntMan', 'Valkiria']
heroesDC = ['Batman', 'SuperMan', 'AquaMan', 'PoisonIvy', 'Shazam', 'WonderWoman', 'GreenLantern', 'Flash', 'NightWind', 'GreenArrow', 'CatWoman', 'DrFate', 'Raven', 'HawkMan']

file1 = drive.CreateFile({'title': 'heroesMarvel.txt'})
file2 = drive.CreateFile({'title': 'heroesDC.txt'})

def contarTweets(consulta):
	resultados = api.search(consulta)
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
		c += 1
		max2 = max
		max = 0
		i=0
		listDC.insert(c, cadena)
	return listDC


def callBack(ch, method, properties, body):
	if(body == 'Marvel' or body == '@top_heroes Marvel'):
		print(" Recogiendo información sobre la popularidad de los heroes de Marvel")
		llamadaMarvel()
		topmarvel = topSuperHeroesMarvel()
		cadena = "Este es el top de popularidad de los heroes de Marvel.\nTop 1: " + topmarvel[0] + "\nTop 2: " + topmarvel[1] + "\nTop 3: " + topmarvel[2] + "\nTop 4: " + topmarvel[3] + "\nTop 5:" + topmarvel[4]
		#añadir creacion de fichero y subida a drive
		f = open ('heroes.txt','w')
		f.write(cadena) #escribir la cadena
		f.close()
		file1.SetContentString(cadena)
		file1.Upload() # Files.insert()
		url = 'https://drive.google.com/file/d/' + file1['id']
		time.sleep(body.count(b'.'))
	elif(body == 'DC' or body == '@top_heroes DC'):
		print(" Recogiendo información sobre la popularidad de los heroes de DC")
		llamadaDC()
		top = topSuperHeroesDC()
		cadena = "Este es el top de popularidad de los heroes de DC.\nTop 1: " + top[0] + "\nTop 2: " + top[1] + "\nTop 3: " + top[2] + "\nTop 4: " + top[3] + "\nTop 5: " + top[4]
		#creacion de fichero y subida drive
		f = open ('heroes.txt','w')
		f.write(cadena) #escribir la cadena
		f.close()
		file2.SetContentString(cadena)
		file2.Upload() # Files.insert()
		time.sleep(body.count(b'.'))
		url = 'https://drive.google.com/file/d/' + file2['id']


channel.basic_qos(prefetch_count = 0)
channel.basic_consume(queue='topCola', on_message_callback=callBack, auto_ack = True)
channel.start_consuming()