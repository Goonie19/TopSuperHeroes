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

def marvel():
	return marvel

def dc():
	return dc

heroes = ['#CapitanAmerica', '#IronMan', '#Thor', '#Hulk', '#BlackWidow', '#SpiderMan',
'#Falcon', '#WinterSoldier', '#CapitanaMarvel', '#BlackPanther', '#AntMan', '#Valkiria', 
'#Batman', '#SuperMan', '#AquaMan', '#PoisonIvy', '#Shazam', '#WonderWoman', '#GreenLantern', 
'#Flash', '#NightWind', '#GreenArrow', '#CatWoman', '#DrFate', '#Raven', 'HawkMan']

inputs = {'Marvel': marvel(), 'dc': dc()}

def contarTweets(consulta, array):
	resultados = api.search(consulta)
	cont = 0
	for lista in resultados:
		cont += 1
	contadores[consulta] = cont


def llamadaMarvel():
	i = 0
	for n in heroes:
		if(i < 12):
			contarTweets(heroes[i])

def llamadaDC():
	i = 0
	for n in heroes:
		if(i >= 12):
			contarTweets(heroes[i])

def callBack(ch, method, properties, body):
	if(body == 'Marvel'):
		print(" Recogiendo información sobre la popularidad de los heroes de Marvel")
		
