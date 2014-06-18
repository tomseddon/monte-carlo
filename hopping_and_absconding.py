__author__ = 'tom'
import json
import random
from decimal import Decimal
import pylab as pl
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np



def load_viewer_data():
    f = open("viewers.json")
    user_list = []
    for line in f:
        viewers = json.loads(line)
    f.close()
    p_list = []
    for key,value in viewers.items():
        decimal_p = Decimal(format(value['p'], ".2g"))
        exp = decimal_p.as_tuple().exponent
        multiplier = '1'.ljust((-exp)+1,'0')
        whole_number_p = decimal_p * Decimal(multiplier)
        user_list += int(whole_number_p) * [key]
        p_list.append(exp)
    if p_list.count(p_list[0]) <> len(p_list):
        raise Exception('Viewer list must have probabilities with same number of decimal places')
    return viewers,user_list

#sanity check
def load_ads_data():
    f = open("ads.json")
    for line in f:
        ads = json.loads(line)
    f.close()

    p_list = []
    ads_list = []
    for key,value in ads.items():
        decimal_p = Decimal(format(value['p'], ".2g"))
        exp = decimal_p.as_tuple().exponent
        multiplier = '1'.ljust((-exp)+1,'0')
        whole_number_p = decimal_p * Decimal(multiplier)
        ads_list += int(whole_number_p) * [str(key)]
        p_list.append(exp)
    #sanity check
    if p_list.count(p_list[0]) <> len(p_list):
        raise Exception('Ads list must have probabilities with same number of decimal places')
    return ads,ads_list


def run_simulation(viewers,user_list,ads,ads_list,run_count, ad_count, break_count,print_results=False):
    abscond_out = []
    ads_served_list = []
    ads_served_list2 = []
    viewer_results = {}
    ads_served_before_absconding_per_viewer = {}
    print run_count,ad_count,break_count
    i = 0
    while i < run_count:
        ads_served = 0
        abscond_check = 'S'
        rand_viewer = random.choice(user_list)
        if rand_viewer not in viewer_results:
            viewer_results[rand_viewer]=[]
        if rand_viewer not in ads_served_before_absconding_per_viewer:
            ads_served_before_absconding_per_viewer[rand_viewer]=[]

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
        if print_results:
            print "Viewer type " + str(rand_viewer) + " watching movie of " + rand_movie + " genre" + " with glue factor of " + format(movie_glue,".2g")

        abscond_p = a
        stay_p = Decimal(format(1 - abscond_p,".3g")) * movie_glue
        exp = stay_p.as_tuple().exponent
        abscond_p = 1 - stay_p
        multiplier = '1'.ljust((-exp)+1,'0')
        stayers = int(int(multiplier) * stay_p)
        absconders = int(int(multiplier) - stayers)
        abscond_list =  absconders * ['A'] + stayers * ['S']
        ad_break_count = 1
        while ad_break_count <= break_count and abscond_check == 'S':
            if print_results:
                print "     ad break " + str(ad_break_count)
            within_break_ad_count = 1
            while within_break_ad_count <= ad_count and abscond_check == 'S':
                rand_ad = random.choice(ads_list)
                ad_type = ads[rand_ad]['type']
                ads_served_list.append(ads[rand_ad]['type'])
                if print_results:
                    print "         shown random " + str(ads[rand_ad]['type']) + " ad with glue factor of " + str(viewers[rand_viewer]['adPreferences'][ad_type]['glue'])
                #apply ad glue factor to viewer's hopping propensity
                hop_p = h
                glue = Decimal(format(viewers[rand_viewer]['adPreferences'][ad_type]['glue'], ".3g"))
                stay_p = (1-hop_p) * glue
                hop_p = 1 - stay_p
                exp = stay_p.as_tuple().exponent
                multiplier = '1'.ljust((-exp)+1,'0')
                hoppers = int(int(multiplier) * (hop_p))
                stayers = int(int(multiplier) - hoppers)
                hop_list = hoppers * ['H'] + stayers * ['S']

                hop_check = random.choice(hop_list)
                if hop_check == 'H':
                    if print_results:
                        print "             viewer hopped"
                    abscond_check = random.choice(abscond_list)
                    if abscond_check == 'A':
                        if print_results:
                            print "                 viewer absconded after ad number " + str(within_break_ad_count)
                        abscond_out.append(abscond_check)
                    else:
                        ads_served += 1
                        viewer_results[rand_viewer] += [ads[rand_ad]['type']]
                else:
                    if print_results:
                        print "             viewer stayed"
                    abscond_check = 'S'
                    ads_served += 1
                    viewer_results[rand_viewer] += [ads[rand_ad]['type']]
                within_break_ad_count += 1
            ad_break_count += 1
        if abscond_check == 'S':
            abscond_out.append(abscond_check)
        i += 1
        ads_served_list2.append(ads_served)
        ads_served_before_absconding_per_viewer[rand_viewer] += [ads_served]
    return abscond_out,ads_served_list,ads_served_list2,viewer_results,ads_served_before_absconding_per_viewer

runs = 1000
ads_cnt = 2
breaks_cnt = 2

viewers,user_list = load_viewer_data()
ads,ads_list = load_ads_data()


abscond_out,ads_served_list,ads_served_list2,viewer_results,ads_served_before_absconding_per_viewer = run_simulation(viewers,user_list,
                                                                                                                     ads,ads_list,runs,
                                                                                                                     ads_cnt,
                                                                                                                     breaks_cnt)


print "absconders " + str(abscond_out.count('A')) + " stayers " + str(abscond_out.count('S')) + " ads served " + str(sum(ads_served_list2))
print ads_served_list2
