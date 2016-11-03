# Think Bayes
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

# dir containing this file + book function file
os.chdir('C:/Users/cloud/Dropbox/Projects/bayesbook/')

#===========#
# Chapter 1 #
#===========#

# Conjoint probability
# ====================
# p(A and B) = p(A) * p(B|A) = p(B) * p(B|A)
#
# for independent events, p(B|A) = p(B)

# Diachronic interpretation
# =========================
#
# p(H|D) = p(H) * p(D|H) / p(D)
#
# posterior = prior * likelihood / normalizing constant

# "Suite": a MECE set of hypotheses

#===========#
# Chapter 2 #
#===========#

from thinkbayes import Pmf  # requires print statement fixes

# build a 6-sided die:
die = Pmf()
for x in range(1,7):
    die.Set(x, 1/6.)

# solve the cookie problem
cookies = Pmf()
# set our prior distribution
cookies.Set('Bowl 1', 0.5)
cookies.Set('Bowl 2', 0.5)
# update the distribution based on evidence of a vanilla cookie
cookies.Mult('Bowl 1', 0.75)
cookies.Mult('Bowl 2', 0.5)
# renormalize
cookies.Normalize()
# posterior probability
print(cookies.Prob('Bowl 1'))

# more general tooling for the cookie problem:
class Cookie(Pmf):
    def __init__(self, hypos):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()

    def Update(self, data):
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()

    # dict to use in Likelihood method
    mixes = {
        'Bowl 1': dict(vanilla = 0.75, chocolate = 0.25),
        'Bowl 2': dict(vanilla = 0.5, chocolate = 0.5)
    }

    def Likelihood(self, data, hypo):
        mix = self.mixes[hypo]
        like = mix[data]
        return(like)

# using the above class:
hypos = ['Bowl 1', 'Bowl 2']
cookies2 = Cookie(hypos)
cookies2.Update('vanilla')
for hypo, prob in cookies2.Items():
    print(hypo, prob)

# using the above class for an example with replacement
dataset = ['vanilla', 'chocolate', 'vanilla']
for data in dataset:
    cookies2.Update(data)
