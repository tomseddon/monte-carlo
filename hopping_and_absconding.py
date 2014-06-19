__author__ = 'tom'
import json
import random
from decimal import Decimal
import pylab as pl
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from matplotlib import pyplot as plt,rcParams
import pymc as pm
import prettyplotlib as ppl
rcParams['axes.linewidth'] = 0.1

def group_hist(key,list1,bins):

    data = list1
    x = np.array(data)
    hist, bins = np.histogram(x, bins=bins)
    hist = hist/float(sum(hist))
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width,color='green',linewidth=0.1)
    plt.xlabel('Number of ads seen', fontsize=8)
    plt.ylabel('p', fontsize=8)
    plt.tick_params(labelsize=8)
    fig = plt.gcf()
    fig.set_size_inches(7,4)
    plt.grid(True)
    plt.title('Viewer Group ' + str(key) + " Ad Impression Probability", fontsize=10)
    plt.savefig('/home/tom/monte-carlo/' + str(key) + '.png', dpi=300, bbox_inches='tight')


def compare_groups(list1,list2):

    data = list1 + list2
    count_data = np.array(data)
    n_count_data = len(count_data)
    plt.bar(np.arange(n_count_data), count_data, color="#348ABD")
    plt.xlabel("Time (days)")
    plt.ylabel("count of text-msgs received")
    plt.title("Did the viewers' ad viewing increase with the number of ads shown?")
    plt.xlim(0, n_count_data)
    #plt.show()

    alpha = 1.0 / count_data.mean()  # Recall count_data is the
                                   # variable that holds our txt counts
    print alpha
    lambda_1 = pm.Exponential("lambda_1", alpha)
    lambda_2 = pm.Exponential("lambda_2", alpha)

    tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data)

    @pm.deterministic
    def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
        out = np.zeros(n_count_data)
        out[:tau] = lambda_1  # lambda before tau is lambda1
        out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
        return out

    observation = pm.Poisson("obs", lambda_, value=count_data, observed=True)

    model = pm.Model([observation, lambda_1, lambda_2, tau])

    mcmc = pm.MCMC(model)
    mcmc.sample(40000, 10000, 1)

    lambda_1_samples = mcmc.trace('lambda_1')[:]
    lambda_2_samples = mcmc.trace('lambda_2')[:]
    tau_samples = mcmc.trace('tau')[:]

    print tau_samples
    # histogram of the samples:

    ax = plt.subplot(311)
    ax.set_autoscaley_on(False)

    plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of $\lambda_1$", color="#A60628", normed=True)
    plt.legend(loc="upper left")
    plt.title(r"""Posterior distributions of the variables
        $\lambda_1,\;\lambda_2,\;\tau$""")
    plt.xlim([0, 6])
    plt.ylim([0, 7])
    plt.xlabel("$\lambda_1$ value")

    ax = plt.subplot(312)
    ax.set_autoscaley_on(False)
    plt.hist(lambda_2_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of $\lambda_2$", color="#7A68A6", normed=True)
    plt.legend(loc="upper left")
    plt.xlim([0, 6])
    plt.ylim([0, 7])
    plt.xlabel("$\lambda_2$ value")

    plt.subplot(313)
    w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)
    plt.hist(tau_samples, bins=n_count_data, alpha=1,
             label=r"posterior of $\tau$",
             color="#467821", weights=w, rwidth=2.)
    plt.xticks(np.arange(n_count_data))

    plt.legend(loc="upper left")
    plt.ylim([0, .75])
    plt.xlim([0,len(count_data)])
    plt.xlabel(r"$\tau$ (iterations)")
    plt.ylabel("probability");

    plt.show()


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
    viewer_results = {}
    ads_served_before_absconding_per_viewer = {}

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
                #ads_served_list.append(ads[rand_ad]['type'])
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
                        viewer_results[rand_viewer] += [0]
                    else:
                        ads_served += 1

                else:
                    if print_results:
                        print "             viewer stayed"
                    abscond_check = 'S'
                    ads_served += 1
                    #viewer_results[rand_viewer] += [1]
                within_break_ad_count += 1
            ad_break_count += 1
        if abscond_check == 'S':
            abscond_out.append(abscond_check)
            viewer_results[rand_viewer] += [1]
        i += 1
        ads_served_list.append(ads_served)
        ads_served_before_absconding_per_viewer[rand_viewer] += [ads_served]

    return abscond_out,ads_served_list,viewer_results,ads_served_before_absconding_per_viewer


viewers,user_list = load_viewer_data()
ads,ads_list = load_ads_data()

ads_per_break = 5
breaks_per_film = 10
abscond_out,ads_served_list1,viewer_results,ads_served_before_absconding_per_viewer = run_simulation(viewers,user_list,
                                                                                                                     ads,ads_list,
                                                                                                                     1000,
                                                                                                                     ads_per_break,
                                                                                                                     breaks_per_film,False)



print "absconders " + str(abscond_out.count('A')) + " stayers " + str(abscond_out.count('S')) + " ads served " + str(sum(ads_served_list1))
#print ads_served_before_absconding_per_viewer
#group_hist(ads_served_list1)
"""
for key,value in ads_served_before_absconding_per_viewer.items():
    print key + ": " + str(sum(value)/Decimal(len(value)))
    print max(value)
    group_hist(key,value,ads_per_break*breaks_per_film)
"""

for key,value in viewer_results.items():
    print key + " : " + str(sum(value))


    # y <- glm (x ~ exp) exp = category
    # family = "binomial")
    #summary y