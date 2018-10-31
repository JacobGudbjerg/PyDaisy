import pandas as pd
import numpy as np

class vanGenuchten(object):
    def __init__(self, alpha = 0.79, n =2, Ks = 1.08, neta =0.5, thetaR= 0.153, thetaS = 0.35):
        self.pars={}
        self.pars['thetaR']=thetaR
        self.pars['thetaS']=thetaS
        self.pars['alpha']=alpha
        self.pars['n']=n
        self.pars['m']=1-1/self.pars['n']
        self.pars['Ks']=Ks
        self.pars['neta']=neta
        self.pars['Ss']=0.000001

    def thetaFun(self, psi):
        Se=(1+abs(psi*self.pars['alpha'])**self.pars['n'])**(-self.pars['m'])
        Se[psi>=0]=1.
        return self.pars['thetaR']+(self.pars['thetaS']-self.pars['thetaR'])*Se

    def CFun(self, psi):
      Se=(1+abs(psi*self.pars['alpha'])**self.pars['n'])**(-self.pars['m'])
      Se[psi>=0]=1.
      dSedh=self.pars['alpha']*self.pars['m']/(1-self.pars['m'])*Se**(1/self.pars['m'])*(1-Se**(1/self.pars['m']))**self.pars['m']
      # dSedh(psi>=0)=0;
      return Se*pars['Ss']+(self.pars['thetaS']-self.pars['thetaR'])*dSedh
  
    def KFun(self, psi):
      Se=(1+abs(psi*self.pars['alpha'])**self.pars['n'])**(-self.pars['m'])
      Se[psi>=0]=1.
      return self.pars['Ks']*Se**self.pars['neta']*(1-(1-Se**(1/self.pars['m']))**self.pars['m'])**2

    def default(self, head_end =-10):
        psi = np.linspace(head_end, 0, 101);
        return pd.DataFrame(self.thetaFun(psi) , index = psi, columns=['Theta'])

