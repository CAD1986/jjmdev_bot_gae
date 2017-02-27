# copyright@ jjmdev 2017
# simple regex based question/reply bot
# proof of concept

import logging, datetime, re, os
import json




#r'((?=.*my)|(?=.*i))(?=.*cold)'




class Checkup(object):
    def __init__(self):
        mediComp = (
        (r'((?=.*my)|(?=.*i))(?=.*throat)',0),
        (r'((?=.*my)|(?=.*i))(?=.*nose)(?=.*blocked)',1),
        (r'((?=.*my)|(?=.*i))(?=.*ear)(?=.*blocked)',2),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))((?=.*ear)(?=.*blocked))|(?=.*hear)',3),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*vomit)',4),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*flu)',5),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*rash)',6),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*diarrhoea)|(?=.*diarr)|(?=.*hoea)|(?=.*diorre)|(?=.*rhea)',7),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))((?=.*ear)(?=.*ache))',8),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*temperature)',9),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*throat)',10),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))((?=.*rash)(?=.*weeks))',11),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))((?=.*discharge)(?=.*ear))',12),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*cough)((?=.*more than 3 weeks)|(?=.*repeat))',13),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*cough)(?=.*less than 2 weeks)',14),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*cough)((?=.*inhaler)|(?=.*asthma))',15),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*cough)',16),
        (r'((?=.*son)|(?=.*daughter)|(?=.*child))(?=.*cold)',17),
        (r'((?=.*my)|(?=.*i))(?=.*sneez)',18),
        (r'((?=.*my)|(?=.*i))(?=.*flu)',19),
        (r'((?=.*my)|(?=.*i))(?=.*rash)',20),
        (r'((?=.*my)|(?=.*i))(?=.*ear ache)',21),
        (r'((?=.*my)|(?=.*i))(?=.*diarrhoea)|(?=.*diarr)|(?=.*hoea)|(?=.*diorre)|(?=.*rhea)',22),
        (r'((?=.*my)|(?=.*i))(?=.*tickly)(?=.*cough)',23),
        (r'((?=.*my)|(?=.*i))(?=.*temperature)',24),
        (r'((?=.*my)|(?=.*i))(?=.*sore)(?=.*throat)',25),
        (r'((?=.*my)|(?=.*i))(?=.*ringing)(?=.*ear)',26),
        (r'((?=.*my)|(?=.*i))(?=.*rash)(?=.*2 weeks)',27),
        (r'((?=.*my)|(?=.*i))(?=.*discharge)(?=.*ear)',28),
        (r'((?=.*my)|(?=.*i))(?=.*cough)((?=.*inhaler)|(?=.*asthma))',29),
        (r'((?=.*my)|(?=.*i))(?=.*cough)(?=.*smoker)',30),
        (r'((?=.*my)|(?=.*i))(?=.*cough)',31),
        (r'((?=.*my)|(?=.*i))(?=.*cold)',32),
        (r'((?=.*my)|(?=.*i))(?=.*chesty)(?=.*cough)',33),
        (r'((?=.*my)|(?=.*i))(?=.*vomit)',34),
        (r'(?=.*pharmacist)',35))
        self._mediComp = [(re.compile(x, re.IGNORECASE),y) for (x,y) in mediComp]
        with open('utw_scrapy_bot.json') as json_data:
            self._mediAdvice = json.load(json_data)
            
    def classify(self, str):
        # check each pattern
        for (pattern, keyval) in self._mediComp:
            match = pattern.match(str)
            # did the pattern match?
            if match:
                Whats_up = self._mediAdvice[keyval]['Whats_up'][0]    # echo title of medical complaint
                What_to_look_for = self._mediAdvice[keyval]['What_to_look_for'][0] 
                What_you_can_do = self._mediAdvice[keyval]['What_you_can_do'][0] 
                When_to_seek_help = self._mediAdvice[keyval]['When_to_seek_help'][0] 
                return [Whats_up, What_to_look_for, What_you_can_do, When_to_seek_help]
            #else:
            #    return 'no match'
