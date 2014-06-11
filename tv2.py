__author__ = 'tom'
import json
import random
from decimal import Decimal
from fractions import Fraction
run_count = 10000




viewers = json.loads("""{
    "1": {
        "p": 0.1,
        "hopping": 0.25,
        "absconding": 0.34
    },
    "2": {
        "p": 0.1,
        "hopping": 0.5,
        "absconding": 0.3
    },
    "3": {
        "p": 0.1,
        "hopping": 0.5,
        "absconding": 0.7
    },
    "4": {
        "p": 0.1,
        "hopping": 0.7,
        "absconding": 0.3
    },
    "5": {
        "p": 0.1,
        "hopping": 0.3,
        "absconding": 0.2
    },
    "6": {
        "p": 0.1,
        "hopping": 0.5,
        "absconding": 0.6
    },
    "7": {
        "p": 0.1,
        "hopping": 0.4,
        "absconding": 0.4
    },
    "8": {
        "p": 0.1,
        "hopping": 0.3,
        "absconding": 0.4
    },
    "9": {
        "p": 0.1,
        "hopping": 0.3,
        "absconding": 0.2
    },
    "10": {
        "p": 0.1,
        "hopping": 0.2,
        "absconding": 0.2
    }
}""")

ads = json.loads("""{
    "A": {
        "p": 0.26,
        "glue": 0.3
    },
    "B": {
        "p": 0.45,
        "glue": 0.2
    },
    "C": {
        "p": 0.29,
        "glue": 0.2
    }
}""")
user_list = []
ads_list = []
abscond_check = []
i = 0
while i < run_count:
    p_list = []
    for key,value in viewers.items():
        decimal_p = Decimal(format(value['p'], ".2g"))
        exp = decimal_p.as_tuple().exponent
        multiplier = '1'.ljust((-exp)+1,'0')
        whole_number_p = decimal_p * Decimal(multiplier)
        #print "adding " + str(whole_number_p)  + " of type " + key + " viewers"
        user_list += int(whole_number_p) * [key]
        p_list.append(exp)
    #print str(user_list.count('1')) + ":" + str(user_list.count('2'))
    #sanity check
    #print p_list
    if p_list.count(p_list[0]) <> len(p_list):
     #   print decimal_p
        raise Exception('Viewer list must have probabilities with same number of decimal places')


        #user_list += (Fraction(p)._numerator * [key])
    p_list = []
    for key,value in ads.items():
        decimal_p = Decimal(format(value['p'], ".2g"))
        exp = decimal_p.as_tuple().exponent
        multiplier = '1'.ljust((-exp)+1,'0')
        whole_number_p = decimal_p * Decimal(multiplier)
        #print "adding " + str(whole_number_p)  + " of type " + key + " ads"
        ads_list += int(whole_number_p) * [key]
        p_list.append(exp)
    #print str(ads_list.count('A')) + ":" + str(ads_list.count('B')) + ":" + str(ads_list.count('C'))
    #sanity check
    if p_list.count(p_list[0]) <> len(p_list):
        raise Exception('Ads list must have probabilities with same number of decimal places')

    #while i < run_count:
    rand_viewer = random.choice(user_list)

    # get properties for random viewer
    h = Decimal(format(viewers[rand_viewer]['hopping'], ".3g"))
    a = Decimal(format(viewers[rand_viewer]['absconding'], ".3g"))
    #print "random viewer " + rand_viewer + " picked with hopping propensity of " + str(h) + " (staying p of " + str(1-h) + "), and absconding p of " + str(a)
    #get a random ad
    rand_ad = random.choice(ads_list)
    #apply ad glue factor to viewer's hopping propensity
    glue = Decimal(format(ads[rand_ad]['glue'], ".3g"))
    h = (1-h) * glue
    #print "random ad " + rand_ad + " picked with glue factor of " + str(Decimal(format(ads[rand_ad]['glue'], ".3g")))
    #print "new chance of staying is " + str(h)
    exp = h.as_tuple().exponent
    multiplier = '1'.ljust((-exp)+1,'0')

    hoppers = int(int(multiplier) * (1-h))

    stayers = int(int(multiplier) - hoppers)

    hop_list = hoppers * ['H'] + stayers * ['S']
    #print "hoppers " + str(hop_list.count('H')) + " stayers " + str(hop_list.count('S'))

    hop_check = random.choice(hop_list)

    if hop_check == 'H':
        #print "viewer hopped"
        abscond_p = a
        exp = a.as_tuple().exponent
        stay_p = 1 - a
        multiplier = '1'.ljust((-exp)+1,'0')
        #print stay_p
        absconders = int(int(multiplier) * a)
        stayers = int(int(multiplier) - absconders)
        abscond_list =  absconders * ['A'] + stayers * ['S']

        #print "absconders " + str(abscond_list.count('A')) + " stayers " + str(abscond_list.count('S'))
        abscond_check.append(random.choice(abscond_list))

    else:
        #print "viewer stayed"
        abscond_check.append('S')
    i += 1


print "absconders " + str(abscond_check.count('A')) + " stayers " + str(abscond_check.count('S'))

