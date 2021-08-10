"""
adex - adaptive exponential integrate-and-fire model

Python wrappers for the different celltypes of adex neuron.
Equations and parameter values taken from
  Borges, FS (2017). "Synchronised firing patterns in a random network of adaptive
  exponential integrate-and-fire neuron model" Neural Networks 90 (2017) 1–7
  http://dx.doi.org/10.1016/j.neunet.2017.03.005
  Corresponding author.
	fernandodasilvaborges@gmail.com
  

Cell types from 1 to 5 are based on Borges, FS (2017) Fig. 1:
    a. Adaptation
    b. Tonic spiking
    c. Initial burst
    d. Regular bursting
    e. Irregular
"""

import collections
from neuron import h
dummy = h.Section()
type2017 = collections.OrderedDict([
  #                                 Vr         b 
 ('Adaptation'               , (-68.0 ,   60.0)) ,
 ('Tonic spiking'                  , (-65.0 ,   5.0)) ,
 ('Initial burst'               , (-48.8 ,   35.0)) ,
 ('Regular bursting'               , (-45.0 ,   40.0)) ,
 ('Irregular' , (-47.4 ,  -41.2))])

# class of basic Izhikevich neuron based on parameters in type2003
class AdExCell ():
  '''Create an adex cell based on izhi2003b.mod (https://senselab.med.yale.edu/ModelDB/ShowModel?model=39948)
  Note: Capacitance 'C' differs from sec.cm which will be 1
'''

  def __init__ (self, type='Adaptation', cellid=-1):
    self.type=type
    self.sec=h.Section(name='izhi2003'+type+str(cellid))
    self.sec.L, self.sec.diam = 6.3, 5 # empirically tuned 
    self.izh = h.Izhi2003b(0.5, sec=self.sec)

    self.izh.Vr,self.izh.b = type2017[type]
    self.izh.Iin = 509.7

  def init (self): self.sec(0.5).v = self.vinit

  def reparam (self, type='Adaptation', cellid=-1):
    self.type=type
    self.izh.Vr,self.izh.b = type2017[type]
