
"""
netParams.py

Influence if slow potassium and Ca channels in bistable firing patterns using NetPyNE

Contributors: protachevicz@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne import specs
import pickle, json
import os

netParams = specs.NetParams()   # object of class NetParams to store the network parameters


try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = cfg.scale # Scale factor for number of cells
netParams.sizeX = cfg.sizeX # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.sizeZ # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume
   
layer = {'1':[0.0, 1.0], '2': [1.0,2.0]}  # normalized layer boundaries

#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
netParams.defaultDelay = 0.1 # default conn delay (ms) 
netParams.propVelocity = 300.0 #  300 μm/ms (Stuart et al., 1997)

#------------------------------------------------------------------------------
# Cell parameters  
#------------------------------------------------------------------------------

netParams.popParams['PYR'] = {'cellType': 'PYR', 'numCells': cfg.cellNumber} # add dict with params for this pop

## PYR cell properties
PYRcell = {'secs': {}} # cell rule dict
PYRcell['secs']['soma'] = {'geom': {}, 'mechs': {}} # soma params dict
PYRcell['secs']['soma']['geom'] = {'diam': 96.0, 'L': 96.0, 'Ra': 100.0} # soma geometry
PYRcell['secs']['soma']['mechs']['hh'] = {'gnabar': 0.0, 'gkbar': 0.0, 'gl': 0.00001, 'el': -85} # soma hh mechanism
PYRcell['secs']['soma']['mechs']['hh2'] = {'gnabar': 0.05, 'gkbar': 0.005, 'vtraub':-55} # soma hh mechanism
PYRcell['secs']['soma']['mechs']['im'] = {'gkbar': 0.00003, 'taumax': 1000.0} # M current - specific to LTS pyr cell
PYRcell['secs']['soma']['mechs']['cad'] = {'depth': 1, 'taur': = 5, 'cainf':2.4e-4, 'kt': 0} #calcium decay - no pump
PYRcell['secs']['soma']['mechs']['ical'] = {'gcabar': 2.2e-4} #IL current (Reuveni et al. model, Nernst)
PYRcell['secs']['soma']['mechs']['it'] = {'gcabar':0.0004} #IT current - specific to LTS pyr cell
PYRcell['secs']['soma']['vinit'] = -71 # set initial membrane potential
netParams.cellParams['PYR'] = PYRcell # add dict to list of cell params

#------------------------------------------------------------------------------
# Network parameters  
#------------------------------------------------------------------------------
# Synaptic mechanism parameters
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0}

# Connectivity parameters
netParams.connParams['PYR->PYR'] = {
    'preConds': {'pop': 'PYR'}, 'postConds': {'pop': 'PYR'},
    'weight': cfg.EEGain*0.001,                    # weight of each connection
    'probability': 0.1,
    'synMech': 'AMPA',
    'synsPerConn': int(1.0),
    # 'delay': 'defaultDelay+dist_3D/propVelocity'
    'delay': 0.1}


#------------------------------------------------------------------------------
# Stimulation parameters bkg
#------------------------------------------------------------------------------
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5, 'start': 0}
netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'pop': 'PYR'}, 'weight': 0.1, 'delay': 'uniform(1,5)'}

#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
netParams.stimSourceParams['ICl1'] = {'type': 'IClamp', 'delay': 100, 'dur': 10000, 'amp': cfg.IClamp1, 'sec': 'soma','loc': 0.5}
netParams.stimTargetParams['ICl1->PYR'] =  {'source': 'ICl1', 'conds': {'pop': 'PYR'}}

#------------------------------------------------------------------------------
# Description
#------------------------------------------------------------------------------
netParams.description = """ 
- Code based: https://senselab.med.yale.edu/ModelDB/ShowModel?model=123623
- Pospischil M, Toledo-Rodriguez M, Monier C, Piwkowska Z, Bal T, Frégnac Y, Markram H, Destexhe A (2008) 
- Minimal Hodgkin-Huxley type models for different classes of cortical and thalamic neurons. Biol Cybern 99:427-41
- v0 - import to NetPyNe
"""
