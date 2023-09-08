"""
batch.py 

Influence if slow potassium and Ca channels in bistable firing patterns using NetPyNE

Contributors: protachevicz@gmail.com, fernandodasilvaborges@gmail.com
"""
from netpyne.batch import Batch
from netpyne import specs
import numpy as np
import sys

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg


# ----------------------------------------------------------------------------------------------
# Custom
# ----------------------------------------------------------------------------------------------
def custom():
    params = specs.ODict()
    
    # params[('seeds', 'conn')] =  [1] 
    # params[('gex')] = [0.0005, 0.0010, 0.0015, 0.0020]
    params[('gex')] = [float(sys.argv[3])]

    # params[('IClamp0', 'amp')] = [0.08, 0.10, 0.12] 
    arg_currents = [value.replace('[','').replace(']','').replace(',','').replace("'",'') for value in sys.argv[4:]]
    currents = np.array([float(value) for value in arg_currents if value != '']).astype('float64')
    params[('IClamp0', 'amp')] = currents # list of currents

    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg.py')

    return b

# ----------------------------------------------------------------------------------------------
# Run configurations
# ----------------------------------------------------------------------------------------------
def setRunCfg(b, type='mpi_bulletin'):
    if type=='mpi_bulletin' or type=='mpi':
        b.runCfg = {'type': 'mpi_bulletin', 
            'script': 'init.py', 
            'skip': True}

    elif type=='mpi_direct':
        b.runCfg = {'type': 'mpi_direct',
            'cores': 2,
            'script': 'init.py',
            'mpiCommand': 'mpiexec', # i7  --use-hwthread-cpus
            'skip': True}

    elif type=='mpi_direct2':
        b.runCfg = {'type': 'mpi_direct',
            'mpiCommand': 'mpirun -n 12 ./x86_64/special -mpi -python init.py', # --use-hwthread-cpus
            'skip': True}

    elif type=='hpc_slurm_gcp':
        b.runCfg = {'type': 'hpc_slurm',
            'allocation': 'default',
            'walltime': '24:00:00',
            'nodes': 1,
            'coresPerNode': 80,
            'email': 'fernandodasilvaborges@gmail.com',
            'folder': '/home/ext_fernandodasilvaborges_gmail_/S1_mouse/sim/',
            'script': 'init.py',
            'mpiCommand': 'mpirun',
            'skipCustom': '_raster.png'}

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------
if __name__ == '__main__': 
    b = custom() #

    # b.batchLabel = 'v0_batch0'  
    # b.saveFolder = '../data/'+b.batchLabel
    version_number = sys.argv[1]
    batch_number = sys.argv[2]
    batch_number = batch_number.zfill(4) # fill string with zeros.

    b.batchLabel = f'v{version_number}_batch{batch_number}' #cfg.simLabel  # default: 'v0_batch0'
        
    cfg.simLabel = b.batchLabel
    b.saveFolder = '../data/'+b.batchLabel
    b.method = 'grid'
    setRunCfg(b, 'mpi_direct')     # setRunCfg(b, 'mpi_bulletin')
    b.run() # run batch