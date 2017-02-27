import StringIO
import json
import logging
import random
import urllib
import urllib2
from io import BytesIO
import os

# for sending images
from PIL import Image
import multipart
#import webapp2
# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from nlp import nlpfunc

from flask import request
from flask_restful import Resource, reqparse


TOKEN = '337043335:AAHqJRmmNkhcic3kh_jJkGhr4r3mu6Pa8JA'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(Resource):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        return json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe')))


class GetUpdatesHandler(Resource):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        return json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates')))


class SetWebhookHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url')
        args = parser.parse_args()
        logging.debug(args)
        urlfetch.set_default_fetch_deadline(60)

        if args['url']:
            return json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': args['url']}))))

class DelWebhookHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url')
        args = parser.parse_args()
        logging.debug(args)
        urlfetch.set_default_fetch_deadline(60)

        if args['url']:
            return json.dumps(json.load(urllib2.urlopen(BASE_URL + 'deleteWebhook')))
        
def reply(chat_id=None, message_id=None, msg=None, img=None):
    if img:
        resp = urllib2.urlopen(BASE_URL + 'sendPhoto', urllib.urlencode({
        'chat_id': str(chat_id),
#       'reply_to_message_id': str(message_id),
        'caption': msg,
        'photo': img,
        })).read()
        logging.debug(resp)
    elif msg:
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
        'chat_id': str(chat_id),
        'parse_mode': 'html',
        'text': msg,
#       'reply_to_message_id': str(message_id),
        })).read()
        logging.debug(resp)
    else:
        logging.error('no msg or img specified')
        resp = None

    logging.info('send response:')      
    logging.info(resp)
        
class WebhookHandler(Resource):
    def post(self):
        cu = nlpfunc.Checkup()
        parser = reqparse.RequestParser()
        parser.add_argument('request body:')
        parser.add_argument('body')
        args = request.get_json()
        logging.debug(args)
        update_id = args['update_id']
        try:
            message = args['message']
        except:
            message = args['edited_message']
        message_id = message['message_id']
        date = message['date']
        text = message['text']
        fr = message['from']
        u_name = fr['username']
        f_name = fr['first_name']
        chat = message['chat']
        chat_id = chat['id']
        
        if not text:
            logging.debug('no text')
            return

        if text.startswith('/'):
            if text == '/start':
                reply(chat_id, message_id, 'Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply(chat_id, message_id, 'Bot disabled')
                setEnabled(chat_id, False)
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'PNG')
                reply(chat_id, message_id, msg=None, img=output.getvalue())
            elif text == '/utw':
                reply(chat_id, None, 
                      'Under The Weather',
                      'https://jjmdev-a.appspot.com/client/utw_160px.png')
            elif text == '/welcome':
                reply(chat_id, None, 
                      'Under The Weather Bot - proof of concept by jjmDev 2017',
                      'https://jjmdev-a.appspot.com/client/welcome_poc.png')
            else:
                reply(chat_id, message_id, 'What command?')

        # so not a command
        # so start basic regex based NLP Functionality 
        utw_reply = cu.classify(text)
        if not utw_reply:
            reply(chat_id, None, 
                  'I am sorry, "%s" there is no response for that statement in my lexicon! This is a proof of concept bot. Try asking general medical questions as per HSE website www.undertheweather.ie thankyou' % f_name,
                  'https://jjmdev-a.appspot.com/client/icon_sad_160.png') 
        else:
            reply(chat_id, None, 
            'test',
            )
            
#        else:
#            if getEnabled(chat_id):
#                reply(chat_id, None, 
#                    'I am sorry, "%s" there is no response for that statement in my lexicon! This is a proof of concept bot. Try asking general medical questions as per HSE website www.undertheweather.ie thankyou' % f_name,
#                    'https://jjmdev-a.appspot.com/client/icon_sad_800.png')
#                else:
#                logging.debug('not enabled for chat_id {}'.format(chat_id))