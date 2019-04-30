#!/usr/bin/python2

import pika
import os
import sys
import tweepy
import time

con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = con.channel()

CONSUMER_KEY = '9MgHe4rbqjnKi3Kn5YSAtl6Kv'

CONSUMER_SECRET = 'kI9PzNX7MvMjYXFfGfsZLrvcKzIRW9ZosTc5rMUBmwEqgP1T9U'

ACCESS_KEY = '1123125102898495488-ATNY3FO9pKAWqUdPU3escdwKW45M0y'

ACCESS_SECRET = 'It281zL407ccZLhjRAi3twaOXuZze79s06nqhXqVo4fgv'

twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.api(tw)

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
	resultados = api.serch(consulta)
	cont = 0
	for lista in resultados:
		++cont
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
