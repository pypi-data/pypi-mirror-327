import warnings
import brainpy.math as bm
import jax
import numpy as np
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel_lb1 import EINet
from bpusdk.BrainpyLib.lb1_SNN import ASIC_SNN
import random

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
bm.set_dt(0.5)

def test(gen_net = True):
    if gen_net is True:
        download_dir = rf"../../tmp96_dt0.5_test"
        print(rf'download_dir: {download_dir}')

        # Scope paramter
        scope = 16
        nNeuron = scope*1024
        nExc = int(nNeuron/2)
        nInh = int(nNeuron/2)
        nNeuron = nExc+nInh
        connect_prob = 5 / nNeuron
        # connect_prob = np.load("W:\int8\Gdiist-BPU-Toolkit\conn_info.npy") #of shape 2x nConn =[pre;post]

        net = EINet(nExc, nInh,connect_prob,method = "euler", allow_multi_conn= False)

        # Simulation parameter
        nStep = 100
        inpE = 20.                                       # Constant current stimuli injected to all neurons during all steps
        inpS = np.zeros((nStep, nNeuron))
        spk_ranges = 1.6
        key = jax.random.PRNGKey(1)
        x = bm.where(jax.random.normal(key, shape=(
            min(16384, nNeuron),)) >= spk_ranges, 1, 0)
        #inpS[0][:16384] = x
        inpS = inpS.astype(bool)
                                                         # Spike stimuli
        # net.dump(download_dir,inpS,inpE,nStep)           # Dump sw data under download/soft_data

        # test = BrainpyBase(net, inpE)
        # conn_matrix = test.get_connection_matrix()
        # cv = test.cv

        config_dir = './HardwareConfig/Config_lb1_ASIC.yaml'
        bpuset = ASIC_SNN(net, inpS, inpE, config_file=config_dir)
        bpuset.gen_bin_data(download_dir)

    #download_dir, upload_dir = gen_v2(base=scope, scale=neuronScale, para_max=36, cp_max=4)
    # m = ModelRun(tile_num=6*24, row=6, col=24, step_num=T, loadPath=download_dir, uploadPath=upload_dir)
    # m.deploy()
    # m.simu()

if __name__ == "__main__":
    test()
