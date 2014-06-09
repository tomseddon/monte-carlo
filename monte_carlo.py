import random

x = ['P','P','D','P','N','P','P','P','N','P']

j = 0
run_count = 100000
sample_size = 100
print 'Average NPS for ' + str(run_count) + ' groups of ' + str(sample_size)

nps_list = []
while j <= run_count:
	i = 0
	sim = []
	while i <= sample_size:
		i += 1
		sim.append(random.choice(x))
		
	detractors = sim.count('D')
	promoters = sim.count('P')
	detractor_pct = (detractors/float(len(sim)))*100
	promoter_pct = (promoters/float(len(sim)))*100	
	nps = promoter_pct - detractor_pct
	nps_list.append(nps)
	j += 1
	
print nps_list
print 'Average score ' + str(sum(nps_list) / float(len(nps_list)))