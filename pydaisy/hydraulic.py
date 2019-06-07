#! /usr/bin/env python3

import math
import numpy as np

def pF2h (pF):
  return -pow (10, pF)

def h2pF (h):
  return log10 (-h)

# The HYPRES pedotranspher functions find parameters for
# Mualem-van Genuchten rentention and conductivity curves based
# on texture, organic content, and dry bulk density.
#
# texture_class must be 'USDA3', signifying 2, 50, and 2000 um upper limits
# for clay, silt and sand respectively.
# clay, silt, sand and humus must be in % and add up to 100
# rho_b is the dry bulk density in g/cm^3
# top_soil is True for the plowing layer.
#
# The return value is a dict containing M-vG parameters.
# Theta_sat []
# Theta_res []
# alpha [cm^-1]
# n []
# l []
# K_sat [cm/h]

def HYPRES (*, texture_class, clay, silt, sand, humus, rho_b, top_soil):
    # Check arguments.
    assert texture_class == 'USDA3'
    assert math.isclose (clay + silt + sand + humus, 100.0)
    assert clay > 0 and clay < 100
    assert silt > 0 and silt < 100
    assert sand > 0 and sand < 100
    assert humus > 0 and humus < 100
    assert rho_b > 0.0

    # Calculate Theta_sat
    Theta_sat = (0.7919 + 0.001691 * clay - 0.29619 * rho_b
                 - 0.000001491 * silt * silt
                 + 0.0000821 * humus * humus + 0.02427 / clay + 0.01113 / silt
                 + 0.01472 * math.log (silt) - 0.0000733 * humus * clay
                 - 0.000619 * rho_b * clay
                 - 0.001183 * rho_b * humus)
    if top_soil:
        Theta_sat -= 0.0001664 * silt
    assert Theta_sat > 0.0 and Theta_sat < 1.0

    # Calculate alpha
    alpha_star = (-14.96 + 0.03135 * clay  + 0.0351 * silt + 0.646 * humus
                  + 15.29 * rho_b - 4.671 * rho_b * rho_b
                  - 0.000781 * clay * clay - 0.00687 * humus * humus
                  + 0.0449 / humus + 0.0663 * math.log (silt)
                  + 0.1482 * math.log (humus)
                  - 0.04546 * rho_b * silt - 0.4852 * rho_b * humus)
    if top_soil:
        alpha_star -= 0.192
        alpha_star += 0.00673 * clay
    alpha = math.exp (alpha_star)

    # calculate n
    n_star = (-25.23 - 0.02195 * clay + 0.0074 * silt - 0.1940 * humus
              + 45.5 * rho_b
              - 7.24 * rho_b * rho_b + 0.0003658 * clay * clay
              + 0.002885 * humus * humus
              - 12.81 / rho_b - 0.1524 / silt - 0.01958 / humus
              - 0.2876 * math.log (silt)
              - 0.0709 * math.log (humus) - 44.6 * math.log (rho_b)
              - 0.02264 * rho_b * clay
              + 0.0896 * rho_b * humus)
    if top_soil:
        n_star += 0.00718 * clay
    n = math.exp (n_star) + 1.0

    # Calculate l
    l_star = (0.0202 + 0.0006193 * clay * clay - 0.001136 * humus * humus
              - 0.2316 * math.log (humus) - 0.03544 * rho_b * clay
              + 0.00283 * rho_b * silt
              + 0.0488 * rho_b * humus)
    l = (10.0 * math.exp (l_star) - 10.0) / (1.0 + math.exp (l_star))

    # Calculate K_sat
    K_sat_star = (7.755 + 0.0352 * silt - 0.967 * rho_b * rho_b 
	                 - 0.000484 * clay * clay 
	                 - 0.000322 * silt * silt + 0.001 / silt - 0.0748 / humus
	                 - 0.643 * math.log (silt) - 0.01398 * rho_b * clay
                         - 0.1673 * rho_b * humus)
    if top_soil:
        K_sat_star += 0.93
        K_sat_star += 0.02986 * clay
        K_sat_star -= 0.03305 * silt
    K_sat = math.exp (K_sat_star) / 24.0

    return { 'Theta_sat' : Theta_sat,
             'Theta_res' : 0.01,
             'alpha' : alpha,
             'n' : n,
             'l' : l,
             'K_sat' : K_sat }
             
class M_vG:
    def __init__ (self, *, Theta_sat, Theta_res=0.01, alpha, n, l=0.5, K_sat):
        self.Theta_sat = Theta_sat
        self.Theta_res = Theta_res
        self.alpha = alpha
        self.n = n
        self.l = l
        self.K_sat = K_sat
        self.m = 1-1/n
        self.a = -alpha

    # Relative water content [0-1], h is [cm].
    def Se (self, h):
        if h >= 0:
            return 1
        a=self.a
        n=self.n
        m=self.m
        return pow (1.0 / (1.0 + pow (a * h, n)), m)
        
    def Theta (self, h):
        Theta_sat=self.Theta_sat
        Theta_res=self.Theta_res
        Se=self.Se(h)
        return Se * (Theta_sat - Theta_res) + Theta_res
  
    def K (self, h):
        K_sat=self.K_sat
        l=self.l
        m=self.m
        Se=self.Se(h)
        return (K_sat * pow (Se, l)
                * pow (1.0 - pow (1.0 - pow (Se, 1.0/m), m), 2.0))

def hydraulic_test ():
    
    pars = HYPRES (texture_class='USDA3', clay=5, silt=25, sand=69, humus=1,
                   rho_b=1.6, top_soil=False)
    print (pars)
    fun = M_vG (**pars)
    print ("pF\th\tTheta\tK\n")
    print ("pF\tcm\t\tcm/h\n")
    for pF in (np.arange (0, 5, 0.1)):
        h = pF2h (pF)
        Theta = fun.Theta (h)
        K = fun.K (h)
        print (pF, h, Theta, K, sep="\t")
        

