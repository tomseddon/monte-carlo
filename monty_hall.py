__author__ = 'tom'
import random
from decimal import Decimal
run_count = 100000


choice_swap = []
choice_stay = []
i=0

while i < run_count:
    doors = [(1,"goat"),(2,"car"),(3,"goat")]
    # user chooses a door
    first_choice = random.choice(doors)
    doors.pop(doors.index(first_choice))
    # monty picks a door that is not where the car is
    monty_choice = random.choice([x for x in doors if x[1] <> "car"])
    doors.pop(doors.index(monty_choice))
    # build list of users who stick with their original choice
    choice_stay.append(first_choice[1])
    # build list of users who change their choice
    choice_swap.append(doors[0][1])
    i += 1

print "Probability of winning car if staying with original choice = " + str(choice_stay.count("car")/Decimal(len(choice_stay)) )
print "Probability of winning car if swapping choice = " + str(choice_swap.count("car")/Decimal(len(choice_swap)) )