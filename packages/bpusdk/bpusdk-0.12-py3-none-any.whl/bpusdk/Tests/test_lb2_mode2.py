import time
import warnings
import brainpy.math as bm
import numpy as np
import random
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel_lb2 import EINet
from bpusdk.BrainpyLib.lb2_SNN import lb2_SNN
from bpusdk.BrainpyLib.lb2_checkRes import lb2_checkRes
from bpusdk.BrainpyLib.lb2_deploy import lb2_deploy

def gen_net(nExc,nInh):
    nNeuron = nExc+nInh

    t0 = time.time()
    arr = np.arange(nExc+nInh)
    shuffled_arr = np.random.permutation(arr)
    #conn = ["customized",np.vstack((arr,np.roll(arr,-1)))] 
    conn = ["customized",np.vstack((arr,shuffled_arr))] 
    #conn = ['FixedPostNum', 1] 
    # conn = ['FixedPreNum', 5] 
    # conn = ['FixedTotalNum', 5] 
    # conn = ['FixedProb', 5/nNeuron] 
    # conn = ["prob", 5/nNeuron] 

    net = EINet(nExc, nInh, conn=conn, method = "euler")
    t1 = time.time()
    print(f"{nNeuron//1024}k network generated in {t1-t0:.2f} seconds")
    return net

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(1864)
bm.set_dt(1.0)

if __name__ == "__main__":
    #Gendata
    download_dir = "../../data5/28nm64k_mode2"
    upload_dir = "../upload5/Res28nm64k_mode2"
    
    config_path = './HardwareConfig/Config_lb2.yaml'
    nExc = 32*1024
    nInh = 32*1024
    nStep = 20
    net = gen_net(nExc,nInh)
    inpE = 100.                                       
    inpS = np.zeros((nStep, nExc+nInh))
    inpS = inpS.astype(bool)    
    bpuset = lb2_SNN(net, inpS, inpE, config_file=config_path,mode=2)
    net.dump(download_dir,inpS,inpE,nStep,save=True,jit=True,txt=True)     
    bpuset.gen_bin_data(download_dir)
    #bpuset.gen_hex_data(download_dir)

    #Compare results or convert bin to npy
    check = lb2_checkRes(download_dir, upload_dir, 20, mode=2)
    check.binVSnpy()
    # check.bin2npy()
    # check.npyVSnpy()