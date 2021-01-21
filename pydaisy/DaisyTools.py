import numpy as np
import matplotlib.pyplot as plt


class vanGenuchten(object):
    def __init__(self, alpha = 0.79, n = 2, Ks = 1, l = 0.5, thetaR= 0.15, thetaS = 0.35):
        self.pars={}
        self.pars['thetaR']=thetaR
        self.pars['thetaS']=thetaS
        self.pars['alpha']=alpha
        self.pars['n']=n
        self.pars['m']=1-1/self.pars['n']
        self.pars['Ks']=Ks
        self.pars['l']=l

    def thetaFun(self, psi):
        Se=(1+abs(psi*self.pars['alpha'])**self.pars['n'])**(-self.pars['m'])
#        Se[psi>=0]=1.
        return self.pars['thetaR']+(self.pars['thetaS']-self.pars['thetaR'])*Se
  
    def KFun(self, psi):
        Se=(1+abs(psi*self.pars['alpha'])**self.pars['n'])**(-self.pars['m'])
        Se[psi>=0]=1.
        return self.pars['Ks']*Se**self.pars['l']*(1-(1-Se**(1/self.pars['m']))**self.pars['m'])**2

    def plotH(self, head_end =-1000):
        psi = np.linspace(head_end, 0, 101)
        return plt.plot(self.thetaFun(psi),-psi)

    def plotK(self, head_end =-1000):
        psi = np.linspace(head_end, 0, 101)
        return plt.plot(self.thetaFun(psi),-psi)

