"""
cfg.py 

Simulation configuration for S1 model (using NetPyNE)
This file has sim configs as well as specification for parameterized values in netParams.py 

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne import specs
import pickle
import os

cfg = specs.SimConfig()     # object of class SimConfig to store the simulation configuration

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 2*1e3 # Duration of the simulation, in ms
cfg.dt = 0.025 # Internal integration timestep to use
cfg.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
cfg.verbose = False  # show detailed messages
# cfg.hParams = {'celsius': 36, 'v_init': -71.0}
cfg.hParams = {'v_init': -71.0}
cfg.printRunTime = 0.1
cfg.printPopAvgRates = True

#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------
cfg.popNumber = 1 
cfg.allpops = ['PYR']
cfg.cellNumber = 10

#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
cfg.cellsrec = 2
printNumber = 5
if cfg.cellsrec == 0:  cfg.recordCells = cfg.allpops # record all cells
elif cfg.cellsrec == 1: cfg.recordCells = [(pop,0) for pop in cfg.allpops] # record one cell of each pop
elif cfg.cellsrec == 2: # record 'printNumber' cells of each pop
    cfg.recordCells = []
    for cellNumberLabel in range(0,cfg.cellNumber, int(cfg.cellNumber/printNumber)):
        cfg.recordCells.append((cfg.allpops[0],cellNumberLabel))

cfg.recordTraces = {'Vsoma': {'sec': 'soma','loc': 0.5,'var': 'v'}}
cfg.recordStim = True  # record spikes of cell stims		
cfg.recordTime = False  	
cfg.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'v0_batch0'
cfg.saveFolder = '../data/'+cfg.simLabel
# cfg.filename =                	## Set file output name
cfg.savePickle = False         	## Save pkl file
cfg.saveJson = True	           	## Save json file
cfg.saveDataInclude = ['simData'] ## 'simData' , 'simConfig', 'netParams'
cfg.backupCfgFile = None 		##  
cfg.gatherOnlySimData = False	##  
cfg.saveCellSecs = False			
cfg.saveCellConns = True	

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
# cfg.analysis['plotRaster'] = {'saveData': 'raster_data.json', 'saveFig': True, 'showFig': True} # Plot raster
# cfg.analysis['plotTraces'] = {'include': [2], 'saveFig': True, 'showFig': True} # Plot cell traces
# cfg.analysis['plot2Dnet'] = {'saveFig': True, 'showFig': True} # Plot 2D cells and connections


# cfg.analysis['plotTraces'] = {'include': cfg.recordCells, 'timeRange': [0,cfg.duration], 'overlay': True, 'oneFigPer': 'trace', 'figSize': (10,4), 'saveFig': True, 'showFig': False} 


#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
cfg.analysis['plotRaster'] = {'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'orderInverse': True, 
							'timeRange': [0,cfg.duration], 'figSize': (18,10), 'labels': 'legend', 'popRates': True, 'fontSize':9, 'lw': 2, 'markerSize':4, 'marker': '.', 'dpi': 300} 
cfg.analysis['plotTraces'] = {'include': cfg.recordCells, 'timeRange': [0,cfg.duration], 'oneFigPer': 'trace', 'overlay': False, 'ylim': [-100,40], 'saveFig': True, 'showFig': False, 'figSize':(18,10)}
#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
cfg.scale = 1.0 
cfg.sizeY = 100.0
cfg.sizeX = 100.0 # radius in um
cfg.sizeZ = 100.0

#------------------------------------------------------------------------------
# Connectivity
#------------------------------------------------------------------------------
cfg.addConn = 1
cfg.EEGain = 0.0
cfg.wgkbar = 0.0002
#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
cfg.IClamp1 = 0.001 # amp  in uA or nA ?