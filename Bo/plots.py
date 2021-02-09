import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

mu = 0
sigma = 1
x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.xlabel('$\sigma$')
plt.ylabel('frequency')
plt.suptitle('Normal distribution $\mu$ = 0, $\sigma$ = 1')
plt.vlines(x=[-1.96, 1.96],
           ymin=0,
           ymax=stats.norm.pdf(1.96, mu, sigma),
           colors='r')
plt.savefig('plots/hypothesis.png')
