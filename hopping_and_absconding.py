__author__ = 'tom'
import json
import random
from decimal import Decimal
import time
from fractions import Fraction
run_count = 1000
ad_count = 3
break_count = 3
f = open("viewers.json")

for line in f:
    viewers = json.loads(line)
f.close()
f = open("ads.json")
for line in f:
    ads = json.loads(line)
f.close()


user_list = []
ads_list = []
abscond_out = []
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


    abscond_check = 'S'

    rand_viewer = random.choice(user_list)
    print "Viewer " + str(rand_viewer)
    # get properties for random viewer
    h = Decimal(format(viewers[rand_viewer]['hopping'], ".3g"))
    a = Decimal(format(viewers[rand_viewer]['absconding'], ".3g"))
    #print "random viewer " + rand_viewer + " picked with hopping propensity of " + str(h) + " (staying p of " + str(1-h) + "), and absconding p of " + str(a)
    #get a random ad
    ad_break_count = 1
    while ad_break_count <= break_count and abscond_check == 'S':
        print "     ad break " + str(ad_break_count)
        within_break_ad_count = 1
        while within_break_ad_count <= ad_count and abscond_check == 'S':
            rand_ad = random.choice(ads_list)
            print "         shown random ad " + str(rand_ad)
            #apply ad glue factor to viewer's hopping propensity
            glue = Decimal(format(ads[rand_ad]['glue'], ".3g"))
            hop_p = h
            hop_p = (1-hop_p) * glue
            #print "random ad " + rand_ad + " picked with glue factor of " + str(Decimal(format(ads[rand_ad]['glue'], ".3g")))
            #print "new chance of staying is " + str(h)
            exp = hop_p.as_tuple().exponent
            multiplier = '1'.ljust((-exp)+1,'0')

            hoppers = int(int(multiplier) * (1-hop_p))

            stayers = int(int(multiplier) - hoppers)
            hop_list = hoppers * ['H'] + stayers * ['S']

            #print "hoppers " + str(hop_list.count('H')) + " stayers " + str(hop_list.count('S'))

            hop_check = random.choice(hop_list)

            if hop_check == 'H':
                print "             viewer hopped"
                abscond_p = a
                exp = abscond_p.as_tuple().exponent
                stay_p = 1 - abscond_p
                multiplier = '1'.ljust((-exp)+1,'0')
                #print stay_p
                absconders = int(int(multiplier) * abscond_p)
                stayers = int(int(multiplier) - absconders)
                abscond_list =  absconders * ['A'] + stayers * ['S']
                print abscond_list
                #print "absconders " + str(abscond_list.count('A')) + " stayers " + str(abscond_list.count('S'))
                abscond_check = random.choice(abscond_list)
                if abscond_check == 'A':
                    print "                 viewer absconded after ad number " + str(within_break_ad_count)
                    abscond_out.append(abscond_check)

            else:
                print "             viewer stayed"
                abscond_check = 'S'
            within_break_ad_count += 1

        ad_break_count += 1
    if abscond_check == 'S':
        abscond_out.append(abscond_check)
    i += 1
print abscond_out
print "absconders " + str(abscond_out.count('A')) + " stayers " + str(abscond_out.count('S'))

