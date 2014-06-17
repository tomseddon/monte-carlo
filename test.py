import json
from decimal import Decimal

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

viewers, user_list = load_viewer_data()
print "user#","p","absconding","hopping","computing","deodorant"
for key,value in viewers.items():

    print key,value['p'],value['absconding'],value['hopping'],value['adPreferences']['computing']['glue'],value['adPreferences']['deodorant']['glue']#,value