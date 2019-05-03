#!/usr/bin/python2

import pika
import os
import sys
import tweepy
import time

con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = con.channel()

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

def topSuperHeroes():


def callBack(ch, method, properties, body):
	if(body == 'Marvel' or '"top_heroes Marvel'):
		print(" Recogiendo información sobre la popularidad de los heroes de Marvel")
		llamadaMarvel()
		top = topSuperHeroes()
		cadena = "Este es el top de popularidad de los heroes de Marvel.\nTop 1: " + top[0] + "\nTop 2: " + top[1] + 
		"\nTop 3: " + top[2] + "\nTop 4: " + top[3] + "\nTop 5:" + top[4]


		
