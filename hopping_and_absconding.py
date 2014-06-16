__author__ = 'tom'
import json
import random
from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt

run_count = 10000
ad_count = 3
break_count = 5
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
p_list = []
for key,value in viewers.items():
    decimal_p = Decimal(format(value['p'], ".2g"))
    exp = decimal_p.as_tuple().exponent
    multiplier = '1'.ljust((-exp)+1,'0')
    whole_number_p = decimal_p * Decimal(multiplier)
    user_list += int(whole_number_p) * [key]

    p_list.append(exp)
#print user_list
#sanity check
if p_list.count(p_list[0]) <> len(p_list):
 #   print decimal_p
    raise Exception('Viewer list must have probabilities with same number of decimal places')

p_list = []
for key,value in ads.items():
    decimal_p = Decimal(format(value['p'], ".2g"))
    exp = decimal_p.as_tuple().exponent
    multiplier = '1'.ljust((-exp)+1,'0')
    whole_number_p = decimal_p * Decimal(multiplier)
    ads_list += int(whole_number_p) * [key]
    p_list.append(exp)

print p_list

#sanity check
if p_list.count(p_list[0]) <> len(p_list):

    raise Exception('Ads list must have probabilities with same number of decimal places')
ads_served_list = []
ads_served_list2 = []
while i < run_count:
    ads_served = 0
    abscond_check = 'S'
    rand_viewer = random.choice(user_list)

    # get properties for random viewer
    h = Decimal(format(viewers[rand_viewer]['hopping'], ".3g"))
    a = Decimal(format(viewers[rand_viewer]['absconding'], ".3g"))
    movie_list = []
    for key,value in viewers[rand_viewer]['moviePreferences'].items():

        size = Decimal(format(viewers[rand_viewer]['moviePreferences'][key]['p'],".3g"))

        movie_exp = size.as_tuple().exponent
        movie_multiplier = '1'.ljust((-movie_exp)+1,'0')

        movie_section = int(int(movie_multiplier) * size)
        movie_list += movie_section * [key]

    rand_movie = random.choice(movie_list)

    movie_glue = Decimal(format(viewers[rand_viewer]['moviePreferences'][rand_movie]['glue'],".3g"))
    print "Viewer type " + str(rand_viewer) + " watching movie of " + rand_movie + " genre" + " with glue factor of " + format(movie_glue,".2g")

    abscond_p = a
    stay_p = Decimal(format(1 - abscond_p,".3g")) * movie_glue

    #stay_p = Decimal(format(stay_p,".3g"))



    exp = stay_p.as_tuple().exponent
    abscond_p = 1 - stay_p

    multiplier = '1'.ljust((-exp)+1,'0')

    stayers = int(int(multiplier) * stay_p)
    absconders = int(int(multiplier) - stayers)
    abscond_list =  absconders * ['A'] + stayers * ['S']

    ad_break_count = 1
    while ad_break_count <= break_count and abscond_check == 'S':
        print "     ad break " + str(ad_break_count)
        within_break_ad_count = 1
        while within_break_ad_count <= ad_count and abscond_check == 'S':
            rand_ad = random.choice(ads_list)
            ads_served_list.append(ads[rand_ad]['type'])
            print "         shown random " + str(ads[rand_ad]['type']) + " ad with glue factor of " + str(ads[rand_ad]['glue'])
            #apply ad glue factor to viewer's hopping propensity
            hop_p = h
            glue = Decimal(format(ads[rand_ad]['glue'], ".3g"))
            hop_p = (1-hop_p) * glue
            exp = hop_p.as_tuple().exponent
            multiplier = '1'.ljust((-exp)+1,'0')
            hoppers = int(int(multiplier) * (1-hop_p))
            stayers = int(int(multiplier) - hoppers)
            hop_list = hoppers * ['H'] + stayers * ['S']

            hop_check = random.choice(hop_list)
            if hop_check == 'H':
                print "             viewer hopped"
                abscond_check = random.choice(abscond_list)
                if abscond_check == 'A':
                    print "                 viewer absconded after ad number " + str(within_break_ad_count)
                    abscond_out.append(abscond_check)
                else:
                    ads_served += 1
            else:
                print "             viewer stayed"
                abscond_check = 'S'
                ads_served += 1
            within_break_ad_count += 1
        ad_break_count += 1
    if abscond_check == 'S':
        abscond_out.append(abscond_check)
    i += 1
    ads_served_list2.append(ads_served)
#print abscond_out
print "absconders " + str(abscond_out.count('A')) + " stayers " + str(abscond_out.count('S'))
#print "ads served " + str(len(ads_served_list))
print ads_served_list2
print str(sum(ads_served_list2)) + " of " + str(run_count * ad_count * break_count) + " ads seen"

bins, edges = np.histogram(ads_served_list2, 50, normed=1)
left,right = edges[:-1],edges[1:]
X = np.array([left,right]).T.flatten()
Y = np.array([bins,bins]).T.flatten()

plt.plot(X,Y)
plt.show()
