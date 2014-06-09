__author__ = 'tom'
import json
import random
from decimal import Decimal
from fractions import Fraction

viewers = json.loads('{"1" : {"hopping" : 0.25, "absconding" : 0.34}, "2" : {"hopping" : 0.756, "absconding" : 0.9}}')

ads = json.loads('{"A" : {"p" : 0.2, "glue" : 0.7} }')

rand_viewer =  random.choice(viewers.keys())

h = Decimal(format(viewers[rand_viewer]['hopping'], ".2g"))
a = Decimal(format(viewers[rand_viewer]['absconding'], ".2g"))

hop_list = Fraction(h)._numerator * ['H'] + Fraction(h)._denominator * ['S']
hop_check = random.choice(hop_list)
if hop_check == 'H':
    abscond_list =  Fraction(a)._numerator * ['A'] + Fraction(a)._denominator * ['S']
    abscond_check = random.choice(abscond_list)
else:

