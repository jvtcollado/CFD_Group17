"""
Calculates the required first wall cell height required for y+ = 1 at M=0.8 and M=1.2
"""
from importlib import import_module
import numpy as np
_coolprop = import_module("CoolProp.CoolProp")
CP = _coolprop
PropsSI = CP.PropsSI

Twall = 300  # [K]
Ml = 0.8  # [-]
Mu = 1.2  # [-]
R = 287 # [J/kgK]
gamma = 1.41  # [-]
a = np.sqrt(R*Twall*gamma)

mu_l = PropsSI('v', 'T', Twall, 'A', a, )
mu_u
rho_l
rho_u
nu_l
nu_u

