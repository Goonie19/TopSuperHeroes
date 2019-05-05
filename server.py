#!/usr/bin/python
#coding=utf-8

import pika
import os
import tweepy
import time
import sys
import requests


def server():
    con = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    canal = con.channel()
    canal.queue_declare(queue = 'topCola', durable = True)

    CONSUMER_KEY = ''

    CONSUMER_SECRET = ''

    ACCESS_KEY = ''

    ACCESS_SECRET = ''

    twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(twitter)

    while True:
        try:
            twitter = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            twitter.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(twitter)
            f = open("last_id.txt")
            readFromFile=f.read()
            f.close()
            md = api.mentions_timeline()
            for msg in md:
                if(str(msg.id) not in readFromFile):
                    f = open("last_id.txt", "a")
                    f.write(str(msg.id)+"\n")
                    f.close()
                    if(msg.text == '@top_heroes Marvel' or msg.text =='@top_heroes DC' or msg.text == 'Marvel' or msg.text == 'DC' ):
                        canal.basic_publish(exchange = '',
                        routing_key = 'topCola',
                        body = msg.text+"|"+str(msg.id)+"|"+msg.user.screen_name,
                        properties = None)
                    else:
                        api.update_status("@"+msg.user.screen_name+" Debe contestar con Marvel o DC.", in_reply_to_status_id = msg.id)
        except tweepy.error.TweepError:
            pass
        time.sleep(40)
            
    con.close()

if __name__ == '__main__':
    print("Servidor preparado")
    server()
