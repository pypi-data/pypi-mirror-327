try:
    
    from .session_8 import factorial, combination, binomial_distribution, geometric_distribution, poisson_distribution
    print("mode: global - deploy")
except:
    from session_8 import factorial, combination, binomial_distribution, geometric_distribution, poisson_distribution
    print('mode: local - debug')
import numpy as np

DEBUG_MODE = 0
DEBUG_MODE = 1

# S8Q1
# binomial_distribution(0.02, 300, 8)
# binomial_distribution(0.02, 300, 4, mode=1)
# binomial_distribution(0.02, 300, 3, mode=2)

# S8Q2
# geometric_distribution(help=True)
# geometric_distribution(0.04, 9)
# geometric_distribution(0.04, 2, mode=1)
# geometric_distribution(0.04, 5, type=0, mode=2)

x = [1,2,3,4,5,6]
p = [1/6,1/6,1/6,1/6,1/6,1/6]



class EVS:
    def __init__(self, debug=DEBUG_MODE):
        self.debug = debug
    
    def multi_x_multi_p(self, xs, ps):
        if len(xs) != len(ps):
            print('EV: unvalid data')
            exit()
        # xs = [Decimal(x) for x in xs]
        # ps = [Decimal(p) for p in ps]
        # ev = sum(np.convolve(np.array(xs), np.array(ps), mode='valid'))
        # var = sum(np.convolve(np.array(xs)**2, np.array(ps), mode='valid')) - ev**2
        ev = sum([xs[i]*ps[i] for i in range(len(xs))])
        var = sum([(xs[i]**2)*ps[i] for i in range(len(xs))]) - ev**2
        std = np.sqrt(var)
        
        if self.debug:
            print(ev, var, std)
        return ev, var, std
    
    def multi_x_single_p(self, xs, p):
        xs = np.array(xs)
        ps = np.ones(np.array(xs).shape)*p
        ev = sum(np.convolve(xs, ps, mode='valid'))
        var = sum(np.convolve(xs**2, ps, mode='valid')) - ev**2
        std = np.sqrt(var)
        
        if self.debug:
            print(ev, var, std)
        return ev, var, std
    
    
class BinomialDistribution:
    def __init__(self, p, n, k, debug=DEBUG_MODE):
        self.debug = debug
        self.p = p
        self.n = n
        self.k = k
        
    def P(self, m=0, h=False):
        return binomial_distribution(p=self.p, n=self.n, k=self.k, mode=m, help=h, debug=self.debug)
    
    def get_ev(self):
        return self.n*self.p
    
    def get_var(self):
        return self.n*self.p*(1-self.p)
    
    def get_std(self):
        return np.sqrt(self.n*self.p*(1-self.p))
    

class GeometricDistribution:
    def __init__(self, p, k, debug=DEBUG_MODE):
        self.debug = debug
        self.p = p
        self.k = k
        
    def P(self, t=0, m=0, h=False):
        return geometric_distribution(p=self.p, k=self.k, type=t, mode=m, help=h, debug=self.debug)
    
    def get_ev(self, type=0):
        if not type:
            ev = 1/self.p
        else:
            ev = (1-self.p)/self.p
        return ev
    
    def get_var(self):
            return (1-self.p)/(self.p**2)
        
    def get_std(self):
        return np.sqrt((1-self.p)/(self.p**2))


class PoissonDistribution:
    def __init__(self, k, lam=None, p=None, n=None, debug=DEBUG_MODE):
        self.debug = debug
        self.lam = lam
        self.k = k
        self.p = p
        self.n = n
        
        if self.lam:
            self.base_lam = self.lam
        else:
            self.base_lam = self.n*self.p
        
    def P(self, m=0, h=False):
        return poisson_distribution(lam=self.lam, p=self.p, n=self.n, k=self.k, mode=m, help=h, debug=self.debug)

    def get_ev(self):
        return self.base_lam
    
    def get_var(self):
        return self.base_lam
    
    def get_std(self):
        return np.sqrt(self.base_lam)
    
        
# bd = BinomialDistribution(0.01, 200, 3)
# gd =GeometricDistribution(0.01, 5)
pd = PoissonDistribution(k=8, p=0.01, n=1000)
print(pd.get_ev(), pd.get_var(), pd.get_std())
# evs = EVS()
# print(evs.multi_x_single_p(x, 1/6))

# a = [15,10,7,5,2,1.5,1,0]
# b = [0.052734,
#      0.015625,
#      0.001953,
#      0.001953,
#      0.000072,
#      0.000072,
#      0.000072,
#      0.927517]

# evs = EVS()
# print(evs.multi_x_single_p(a,1/10))