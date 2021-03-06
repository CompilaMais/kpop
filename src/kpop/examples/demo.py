from collections import Counter
from kpop import *

popA = Population.random(50, 50, id='Africa', min_prob=0.2)
popB = popA.genetic_drift(10, 50, id='Brasil', sample_size=25)
popC = popB.genetic_drift(10, 50, id='Colombia', sample_size=25)
popC.fill(50)
pop = popA + popB + popC
ind = popB.random_individual().breed(popC.random_individual())
print(pop.classify(popC[0]), pop.prob_classify(popC[0]))
print(pop.classify(ind), pop.prob_classify(ind))
print(pop.admixture(ind, method='maxlike'))
#print(pop.admixture(ind, method='bayes'))
pop.plot.pca(colors=['black', 'yellow', 'red'])
