__author__ = 'tom'
import json
import random
from decimal import Decimal
from fractions import Fraction
run_count = 10000

def LCM(a,b):
    if a * b == 0:
        return 0
    c = a
    while (c % b) != 0:
        c += a
    return c


viewers = json.loads('{"1" : {"p" : 0.1, "hopping" : 0.25, "absconding" : 0.34}, "2" : {"p" : 0.9, "hopping" : 0.756, "absconding" : 0.9}}')

ads = json.loads('{"A" : {"p" : 0.26, "glue" : 0.7},"B" : {"p" : 0.45, "glue" : 0.2},"C" : {"p" : 0.29, "glue" : 0.2} }')
user_list = []
ads_list = []
p_list = []
for key,value in viewers.items():
    decimal_p = Decimal(format(value['p'], ".2g"))
    exp = decimal_p.as_tuple().exponent
    multiplier = '1'.ljust((-exp)+1,'0')
    whole_number_p = decimal_p * Decimal(multiplier)
    user_list += int(whole_number_p) * [key]
    p_list.append(exp)

#sanity check
if p_list.count(p_list[0]) <> len(p_list):
    raise Exception('User list must have probabilities of same denominator')



    #user_list += (Fraction(p)._numerator * [key])
p_list = []
for key,value in ads.items():
    decimal_p = Decimal(format(value['p'], ".2g"))
    exp = decimal_p.as_tuple().exponent
    multiplier = '1'.ljust((-exp)+1,'0')
    whole_number_p = decimal_p * Decimal(multiplier)
    ads_list += int(whole_number_p) * [key]
    p_list.append(exp)

#sanity check
if p_list.count(p_list[0]) <> len(p_list):
    raise Exception('Ads list must have probabilities of same denominator')





abscond_check = []
i = 0
#while i < run_count:
#TODO cycle through user and ad dicts, creating dynamic lists based on their probability of being picked
rand_viewer = random.choice(user_list)

# get properties for random viewer
h = Decimal(format(viewers[rand_viewer]['hopping'], ".3g"))
a = Decimal(format(viewers[rand_viewer]['absconding'], ".3g"))

#get a random ad
rand_ad = random.choice(ads_list)
print rand_viewer,h,rand_ad,a
#apply ad glue factor to viewer's hopping propensity
h = h * Decimal(format(ads[rand_ad]['glue'], ".3g"))
print h
exp = h.as_tuple().exponent
multiplier = '1'.ljust((-exp)+1,'0')
print multiplier
hoppers = int(int(multiplier) * h)
hoppers
stayers = int(int(multiplier) - hoppers)
print stayers,hoppers

hop_list = hoppers * ['H'] + stayers * ['S']
hop_check = random.choice(hop_list)

if hop_check == 'H':
    abscond_list =  Fraction(a)._numerator * ['A'] + Fraction(a)._denominator * ['S']
    abscond_check.append(random.choice(abscond_list))

else:
    abscond_check.append('S')
i += 1

#print abscond_check.count('A')/float(len(abscond_check))

