import json
import logging
import util
import config
import urllib
from nlp import nlpfunc

from google.appengine.api import urlfetch

from flask import request
from flask_restful import Resource, reqparse

payload_image = {
    'url': ''
}
payload_template = {
    'template_type': '',
    'elements': [
        {
            'title': '',
            'item_url': '',
            'image_url': '',
            'subtitle': '',
            'buttons': [
                {
                    'type': '',
                    'title': '',
                    'url': '',
                    'payload': ''
                }
            ]
        }
    ]
}
send_message = {
    'recipient': {
        'phone_number': '',
        'id': '',
    },
    'message': {
        'text': '',
        'attachment': {
            'type': '',
            'payload': {},
        }
    },
    'notification_type': ''
}


def set_welcome_message(fb_page_id):
    url = 'https://graph.facebook.com/v2.6/' + fb_page_id + '/thread_settings?access_token=' + config.FACEBOOK_PAGE_ACCESS_TOKEN
    if config.PRODUCTION:
        content = {
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [
                {
                    'message': {
                        'text': 'Hello there!',
                        'attachment': {
                            'type': 'template',
                            'payload': {
                                'template_type': 'generic',
                                'elements': [
                                    {
                                        'title': 'Welcome to %s' % config.FACEBOOK_BOT_NAME,
                                        'item_url': 'https://gilacoolbot.appspot.com',
                                        'image_url': 'http://messengerdemo.parseapp.com/img/rift.png',
                                        'subtitle': 'This is a subtitle',
                                        'buttons': [
                                            {
                                                'type': 'web_url',
                                                'title': 'View website',
                                                'url': 'https://gilacoolbot.appspot.com'
                                            },
                                            {
                                                'type': 'postback',
                                                'title': 'Start chatting',
                                                'payload': 'DEVELOPER_DEFINED_PAYLOAD',
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(content)
        req = urlfetch.fetch(
            url,
            payload,
            urlfetch.POST,
            headers
        )
        logging.debug(req.content)


def send_attachment_message(sender, attachment_type, payload):
    fb_sender_id = sender['id']
    content = {
        'recipient': {
            'id': fb_sender_id
        },
        'message': {
            'attachment': {
                'type': attachment_type,
                'payload': payload
            }
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps(content)
    logging.debug(payload)
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + config.FACEBOOK_PAGE_ACCESS_TOKEN
    if config.PRODUCTION:
        req = urlfetch.fetch(
            url,
            payload,
            urlfetch.POST,
            headers
        )
        logging.debug(req.content)
        
#def postback_test():
    


def send_fb_message(payload):
    if config.PRODUCTION:
        try:
            req = urlfetch.fetch(
                'https://graph.facebook.com/v2.6/me/messages?access_token=' + config.FACEBOOK_PAGE_ACCESS_TOKEN,
                payload,
                urlfetch.POST,
                {'Content-Type': 'application/json'}
            )
            logging.debug(req.content)
        except urlfetch.Error as e:
            logging.error(e.message)


def example_message_text(sender, text):
    content = {
        'recipient': {
            'id': sender['id']
        },
        'message': {
            'text': text
        }
    }

    logging.debug('"%s" "%s" "%s"' % (
        'outgoing',
        sender['id'],
        content,
    ))

    payload = json.dumps(content)
    send_fb_message(payload)


def example_message_image(sender, url):
    content = {
        'recipient': {
            'id': sender['id']
        },
        'message': {
            'attachment': {
                'type': 'image',
                'payload': {
                    'url': url
                }
            }
        }
    }

    logging.debug('"%s" "%s" "%s"' % (
        'outgoing',
        sender['id'],
        content,
    ))

    payload = json.dumps(content)
    send_fb_message(payload)
    
def example_message_video(sender, url):
    content = {
        'recipient': {
            'id': sender['id']
        },
        'message': {
            'attachment': {
                'type': 'video',
                'payload': {
                    'url': url
                }
            }
        }
    }

    logging.debug('"%s" "%s" "%s"' % (
        'outgoing',
        sender['id'],
        content,
    ))

    payload = json.dumps(content)
    send_fb_message(payload)
    
def example_message_button(sender, text1, text2, USER_DEFINED_PAYLOAD):    
    content = {
        'recipient': {
            'id': sender['id']
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': text1,
                    'buttons':[
                          {
                            'type': 'postback',
                            'title': text2,
                            'payload': USER_DEFINED_PAYLOAD,
                          }
                        ]
                    }
            }
        }
    }
    
    logging.debug('"%s" "%s" "%s"' % (
        'outgoing',
        sender['id'],
        content,
    ))

    payload = json.dumps(content)
    send_fb_message(payload)

class MainHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hub.mode')
        parser.add_argument('hub.challenge')
        parser.add_argument('hub.verify_token')

        args = parser.parse_args()
        logging.debug(args)

        if args['hub.mode'] == 'subscribe':
            if args['hub.verify_token'] == config.FACEBOOK_WEBHOOK_VERIFY_TOKEN:
                return int(args['hub.challenge'])
        result = {}
        return util.jsonpify(result)

    def post(self):
        cu = nlpfunc.Checkup()
        
        obj = request.get_json()
        if obj:
            for entry in obj['entry']:
                fb_messaging = entry['messaging']
                fb_page_id = entry['id']
                for fb_obj in fb_messaging:
                    fb_sender = fb_obj['sender']
                    fb_recipient = fb_obj['recipient']

                    if 'message' in fb_obj:
                        fb_content = fb_obj['message']
                        logging.debug(fb_content['text'])
                        #logging.debug(fb_sender['id'])
                        fb_timestamp = fb_obj['timestamp']
                        fb_mid = fb_content['mid']
                        fb_seq = fb_content['seq']
                        if'attachments' in fb_content:
                            for attachment in fb_content['attachments']:
                                atype = attachment['type']
                                if atype is 'image' or atype is 'video' or atype is 'audio':
                                    logging.debug(
                                        '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
                                            'incoming',
                                            fb_timestamp,
                                            fb_page_id,
                                            fb_sender['id'],
                                            fb_recipient['id'],
                                            attachment['type'],
                                            attachment['payload']['url'],
                                            fb_seq,
                                            fb_mid
                                        )
                                    )
                                elif atype is 'location':
                                    logging.debug(
                                        '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
                                            'incoming',
                                            fb_timestamp,
                                            fb_page_id,
                                            fb_sender['id'],
                                            fb_recipient['id'],
                                            attachment['type'],
                                            attachment['payload'],
                                            fb_seq,
                                            fb_mid
                                        )
                                    )
                                else:
                                    logging.debug(
                                        '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
                                            'incoming',
                                            fb_timestamp,
                                            fb_page_id,
                                            fb_sender['id'],
                                            fb_recipient['id'],
                                            attachment['type'],
                                            attachment['payload'],
                                            fb_seq,
                                            fb_mid
                                        )
                                    )
                        elif 'text' in fb_content:
                            logging.debug(
                                '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
                                    'Facebook incoming message',
                                    fb_timestamp,
                                    fb_page_id,
                                    fb_sender['id'],
                                    fb_recipient['id'],
                                    'text',
                                    fb_content['text'],
                                    fb_seq,
                                    fb_mid
                                )
                            )
                            # connect to fb graph api to get details of message sender
                            url="https://graph.facebook.com/v2.6/" + str(fb_sender['id']) + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + config.FACEBOOK_PAGE_ACCESS_TOKEN
                            response = urllib.urlopen(url)
                            fb_data = json.loads(response.read())
                            fn ='<fn>'
                            ln ='<ln>'
                            if 'first_name' in fb_data:
                                fn = fb_data["first_name"]
                                ln = fb_data["last_name"]
                                
                            processed = 0 #to check if a sample text code triggered
                            
                            if 'show example text' in fb_content['text']:
                                processed = 1 # yes sample text code triggered
                                example_message_text(
                                    fb_sender,
                                    'This is an example of a message with text only.'
                                )
                                example_message_text(
                                    fb_sender,
                                    'The last thing you said was: "%s"' % fb_content['text']
                                )
                            if 'button' in fb_content['text']:
                                processed = 1
                                example_message_button(
                                    fb_sender,
                                    "It looks like you said: I have a tooth ache",
                                    "Is that correct?",
                                    "I have tooth ache"
                                )
                            if 'show example image' in fb_content['text']:
                                processed = 1
                                example_message_text(
                                    fb_sender,
                                    'This is an example of a message with an image only.'
                                )
                                example_message_image(
                                    fb_sender,
                                    'https://jjmdev-a.appspot.com/client/small_utw.png'
                                )
                            if 'show video' in fb_content['text']:
                                processed = 1
                                example_message_text(
                                    fb_sender,
                                    'This is an example of a message with a HSE video.'
                                )
                                example_message_video(
                                    fb_sender,
                                    '<div style="position:relative;height:0;padding-bottom:56.25%"><iframe src="https://www.youtube.com/embed/Kn7I-Vp-TJI?ecver=2" style="position:absolute;width:100%;height:100%;left:0" width="640" height="360" frameborder="0" allowfullscreen></iframe></div>'
                                )
                                
                            logging.debug(fb_content['text'])
                            utw_reply = cu.classify(fb_content['text'])
                            if processed == 0: # no sample text code triggered, ok proceed to use nlp functions
                                if not utw_reply:
                                    example_message_image(
                                            fb_sender,
                                            'https://jjmdev-a.appspot.com/client/small_icon_sad.png'
                                        )
                                    example_message_text(
                                        fb_sender,
                                        'I am sorry, "%s" there is no response for that statement in my lexicon! This is a proof of concept bot. Try asking general medical questions as per HSE website www.undertheweather.ie thankyou' % fn
                                    )
                                else:
                                    example_message_image(
                                            fb_sender,
                                            'https://jjmdev-a.appspot.com/client/small_utw.png'
                                        )
                                    example_message_text(
                                        fb_sender,
                                        'Hi "%s", so you said: "%s"' % (fn, utw_reply[0])
                                    )
                                    example_message_image(
                                            fb_sender,
                                            'https://jjmdev-a.appspot.com/client/small_icon_scope.png'
                                        )
                                    example_message_text(
                                            fb_sender,
                                            utw_reply[1]
                                    )
                                    example_message_image(
                                            fb_sender,
                                            'https://jjmdev-a.appspot.com/client/small_icon_pill.png'
                                        )
                                    example_message_text(
                                            fb_sender,
                                            utw_reply[2]
                                    )

                    elif 'delivery' in fb_obj:
                        fb_delivery = fb_obj['delivery']
                        fb_watermark = fb_delivery['watermark']
                        fb_seq = fb_delivery['seq']
                        if 'mids' in fb_delivery and len(fb_delivery['mids']) > 0:
                            for fb_mid in fb_delivery['mids']:
                                logging.debug(
                                    '"%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
                                        'delivery',
                                        fb_page_id,
                                        fb_sender['id'],
                                        fb_recipient['id'],
                                        fb_watermark,
                                        fb_seq,
                                        fb_mid
                                    )
                                )
                        else:
                            logging.debug(
                                '"%s" "%s" "%s" "%s" "%s" "%s"' % (
                                    'delivery',
                                    fb_page_id,
                                    fb_sender['id'],
                                    fb_recipient['id'],
                                    fb_watermark,
                                    fb_seq
                                )
                            )
                    else:
                        logging.debug(
                            '"%s" "%s" "%s" "%s" "%s"' % (
                                'incoming',
                                fb_page_id,
                                fb_sender['id'],
                                fb_recipient['id'],
                                fb_obj,
                            )
                        )
        result = {}
        return util.jsonpify(result)
