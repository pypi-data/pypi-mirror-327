
import math
import numpy as np  
from decimal import Decimal

DEBUG_MODE = 0
DEBUG_MODE = 1


def factorial(n, debug=DEBUG_MODE):
    re = 1
    for i in range(2, n+1):
        re *= i
    
    if debug:
        print('factorial', end='\t')
        check = math.factorial(n)
        print(f"{re}\t{check}\t{Decimal(check) == Decimal(re)}")
    return re


def combination(n, k, debug=DEBUG_MODE):
    if n < k:
        re = 0
    else:
        re = factorial(n)/(factorial(n-k)*factorial(k))
    
    if debug:
        print('combination', end='\t')
        check = math.comb(n, k)
        print(f"{re}\t{check}\t{Decimal(check) == Decimal(re)}")
    return re


def binomial_distribution(p=None, n=None, k=None, mode=0, help=False, debug=DEBUG_MODE):
    h = """
    syntax:
    binomial_distribution(p=None, n=None, k=None, mode=0, help=False)
    
    mode:
    0: exactly k
    1: at most k
    2: at least k
    
    if n >= 20 and p <= 0.05: Poisson
    """
    
    if help:
        print(h)
        exit()

    if n >= 20 and p <= 0.05:
        print("WARNING: turn to Poisson distribution")
    if not mode:
        re = combination(n, k)*(p**k)*((1-p)**(n-k))
    elif mode == 1:
        re = 0
        for i in range(k+1):
            re += binomial_distribution(p, n, i)
    elif mode == 2:
        subre = 0
        for i in range(k):
            subre += binomial_distribution(p, n, i)
        re = 1 - subre
    else:
        print("binomial distribution: unvalid mode")
        exit()
    
    if debug:
        print(re)
    return re
    

def geometric_distribution(p=None, k=None, type=0, mode=0, help=False, debug=DEBUG_MODE):
    h = """
    syntax:
    geometric_distribution(p=None, k=None, type=0, mode=0, help=False)
    
    type:
    0: k as number of attempts - 1, 2, 3, ...
    1: k as number of failures - 0, 1, 2, ...
    
    mode:
    0: exactly k times
    1: no later than k times
    2: later than k times
    """
    
    if help:
        print(h)
        exit()
    
    if not type:
        subre = ((1-p)**(k-1))*p
    elif type:
        subre = ((1-p)**k)*p
    
    if not mode:
        re = subre
    elif mode == 1:
        re = 0
        for i in range(1, k+1):
            re += geometric_distribution(p, i, type=type)
    elif mode == 2:
        subre2 = 0
        for i in range(1, k+1):
            subre2 += geometric_distribution(p, i, type=type)
        re = 1 - subre2
    else:
        print("geometric distribution: unvalid mode")
        exit()
            
    if debug:
        print(re)
    return re


def poisson_distribution(lam=None, p=None, n=None, k=None, mode=0, help=False, debug=DEBUG_MODE):
    h = """
    syntax:
    poisson_distribution(lam=None, n=None, p=None, k=None, mode=0, help=False)
    
    if lam == None:
        lam = n*p
 
    mode:
    0: exactly k times
    1: no later than k times
    2: later than k times
    """
    
    if help:
        print(h)
        exit()
    
    if not lam:
        lam = n*p
    
    subre = (lam**k)*(np.e**(-lam))/factorial(k)

    if not mode:
        re = subre
    elif mode == 1:
        re = 0
        for i in range(k+1):
            re += poisson_distribution(lam, p, n, i)
    elif mode == 2:
        subre2 = 0
        for i in range(k):
            subre2 += poisson_distribution(lam, p, n, i)
        re = 1 - subre2
    else:
        print("poisson distribution: unvalid mode")
        exit()
            
    if debug:
        print(re)
    return re
    




# S8E1
# binomial_distribution(0.01, 200, 3)xs
# binomial_distribution(0.01, 200, 2, 1)
# binomial_distribution(0.01, 200, 3, 2)
# binomial_distribution(help=True)

# S8E2
# geometric_distribution(0.01, 5)
# geometric_distribution(0.01, 3, mode=1)
# geometric_distribution(0.01, 9, mode=2)
# geometric_distribution(help=True)

# S8E3
# poisson_distribution(p=0.01, n=1000, k=82)




