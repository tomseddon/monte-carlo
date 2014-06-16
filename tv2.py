import random as ran
from decimal import Decimal

x = [0.016, 0.011, 0.018, 0.014, 0.011, 0.017, 0.018, 0.004, 0.004, 0.004, 0.003, 0.016, 0.016, 0.001, 0.003, 0.013, 0.011, 0.017, 0.003, 0.013, 0.005, 0.002, 0.007, 0.018, 0.009, 0.001, 0.015, 0.008, 0.015, 0.004, 0.008, 0.016, 0.013, 0.007, 0.003, 0.011, 0.015, 0.016, 0.019, 0.001, 0.015, 0.015, 0.019, 0.003, 0.007, 0.008, 0.002, 0.015, 0.006, 0.004, 0.017, 0.001, 0.009, 0.007, 0.017, 0.004, 0.009, 0.006, 0.012, 0.003, 0.018, 0.015, 0.018, 0.004, 0.015, 0.008, 0.019, 0.002, 0.008, 0.015, 0.006, 0.016, 0.008, 0.008, 0.006, 0.003, 0.013, 0.002, 0.011, 0.012, 0.018, 0.017, 0.013, 0.012, 0.016, 0.009, 0.005, 0.003, 0.013, 0.019, 0.001, 0.007, 0.006, 0.002, 0.013, 0.018, 0.011, 0.001, 0.009, 0.009, 0.003,0.003]
y = ['automobile','toothpaste','smartphone','insurance','supermarket','sports drink','deodorant','hair product','makeup','airline','confectionery','computing','search engine','film','newspaper','toothbrush','clothing','handbag','television','toaster','refrigerator','tablet','gun','cigarette','alcoholic drink','headphone','banking','pen','book','fast food','train','utility company']

ads = {}
i=0
j=1
for item in x:
    ad = {}
    ad['p']=item
    ad['type']=y[i]
    ad['glue']=float(ran.randint(5,10)/Decimal(10))
    ads[str(j)]=ad
    if y[i]==y[-1]:
        i = 0
    else:
        i += 1
    j += 1

print len(ads)
print
i=0
for key,value in ads.items():
   # print value['p']
    i += value['p']
print i

print ads