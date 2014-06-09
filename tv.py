__author__ = 'tom'
import random

run_count = 100000
viewer_group = ['A','A','A','B','B','B','B','C','C','D','D','D','D','D']
ad_group = [('1',0.2),('1',0.2),('2',0.8),('2',0.8),('2',0.8),('3',0.9),('3',0.9),('3',0.9),('3',0.9),('3',0.9),('3',0.9)]

group_a_hopping = ['H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S']

group_b_hopping = ['H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H''H','H','H','H','H',
                   'H','H','H','H','H','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S']

group_c_hopping = ['H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S']


group_d_hopping = ['H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','H','H','H','H','H','H','H','H','H',
                   'H','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S',
                   'S','S','S','S','S','S','S','S','S','S']


group_a_absconding = ['A','A','A','A','A','S','S','S','S','S']

group_b_absconding = ['A','A','A','S','S','S','S','S','S','S']

group_c_absconding = ['A','A','A','A','A','A','S','S','S','S']

group_d_absconding = ['A','A','A','S','S','S','S','S','S','S']

a_list = []
b_list = []
c_list = []
d_list = []


def overall_absconding_propensity(item):
    if item == 'A':
            hop = ''
            abscond = ''
            hop = random.choice(group_a_hopping)
            if hop == 'H':
                abscond  = random.choice(group_a_absconding)
                if abscond == 'A':
                    a_list.append(abscond)
            else:
                a_list.append('S')
    elif item == 'B':
            hop = ''
            abscond = ''
            hop = random.choice(group_b_hopping)
            if hop == 'H':
                abscond  = random.choice(group_b_absconding)
                if abscond == 'A':
                    b_list.append(abscond)
            else:
                b_list.append('S')

    elif item == 'C':
            hop = ''
            abscond = ''
            hop = random.choice(group_c_hopping)
            if hop == 'H':
                abscond  = random.choice(group_c_absconding)
                if abscond == 'A':
                    c_list.append(abscond)
            else:
                c_list.append('S')

    elif item == 'D':
            hop = ''
            abscond = ''
            hop = random.choice(group_d_hopping)
            if hop == 'H':
                abscond  = random.choice(group_d_absconding)
                if abscond == 'A':
                    d_list.append(abscond)
            else:
                d_list.append('S')




    #result = out[len(out)-1]
j = 0
while j < run_count:
    x = random.choice(viewer_group)
    y = random.choice(ad_group)
    overall_absconding_propensity(x)
    j += 1


print 'Group A probability ' + str(round(viewer_group.count('A')/float(len(viewer_group)),2)), 'Initial chance of staying ' + str(group_a_hopping.count('S')/float(len(group_a_hopping))), 'Chance of returning after hop ' + str(group_a_absconding.count('S')/float(len(group_a_absconding))), 'Overall chance of viewer staying ' +  str(a_list.count('S')/float(len(a_list))*100)
print 'Group B probability ' + str(round(viewer_group.count('B')/float(len(viewer_group)),2)), 'Initial chance of staying ' + str(group_b_hopping.count('S')/float(len(group_b_hopping))), 'Chance of returning after hop ' + str(group_b_absconding.count('S')/float(len(group_b_absconding))), 'Overall chance of viewer staying ' +  str(b_list.count('S')/float(len(b_list))*100)