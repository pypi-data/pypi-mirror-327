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

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
bm.set_dt(2.0)

def createConn(nNeuron,fanOut,groupSize):
    iNeuron_list = list(np.arange(nNeuron))
    nGroup = int(np.ceil(nNeuron/groupSize)) #last group may have a different size
    group_pre_list = list(np.arange(nGroup))
    group_pre_list = [item for item in group_pre_list for _ in range(fanOut)]
    if fanOut < groupSize:
        # with no replacement -> act as pre once/never
        # risk for self connection
        group_post_list = random.sample(iNeuron_list, k=len(group_pre_list))
    else:
        group_post_list = random.choice(iNeuron_list, k=len(group_pre_list))
        #TODO: check multiple connection here
    pre_list = []
    post_list = []
    for pre,post in zip(group_pre_list,group_post_list):
        if pre == nGroup:
            tmp_pre = np.arange(pre*groupSize,nNeuron)
            tmp_post = [post]*len(tmp_pre)
        else:
            tmp_pre = np.arange(pre*groupSize,pre*groupSize+groupSize)
            tmp_post = [post]*groupSize
        pre_list.extend(tmp_pre)
        post_list.extend(tmp_post)
    return pre_list,post_list

def gen_net(nExc,nInh):
    t0 = time.time()
    nNeuron = nExc+nInh
    data = np.array(createConn(nNeuron,fanOut=1,groupSize=4))  
    conn = ["customized",data] 
    #conn = ['FixedPostNum', 1] 
    # conn = ['FixedPreNum', 5] 
    # conn = ['FixedTotalNum', 5] 
    # conn = ['FixedProb', 5/nNeuron] 
    # conn = ["prob", 5/nNeuron] 

    net = EINet(nExc, nInh, conn=conn, method = "euler")
    t1 = time.time()
    print(f"{nNeuron//1024}k network generated in {t1-t0:.2f} seconds")
    return net

if __name__ == "__main__":
    download_dir = "../../data5/28nm2304k_b2s2_int8"
    upload_dir = "../../upload5/Res28nm2304k_b2s2_int8"
    config_path = './HardwareConfig/Config_lb2_b2s2_int8.yaml'
    nExc = 115*1024
    nInh = 115*1024
    nStep = 20

    # # Gendata
    net = gen_net(nExc,nInh)
    inpE = 100.                                       
    inpS = np.zeros((nStep, nExc+nInh))
    inpS = inpS.astype(bool)    
    bpuset = lb2_SNN(net, inpS, inpE, config_file=config_path)
    net.dump(download_dir,inpS,inpE,nStep,save=True,jit=True)     
    bpuset.gen_bin_data(download_dir)
    bpuset.gen_hex_data(download_dir)

    # Deploy
    # sender_path = "/home/gdiist/work/LBII/LBII/build/LBII"
    # sender_rst_path = "/home/gdiist/work/git_lbii/gdiist_host/pcie_hot_reset.sh"
    # pwd = "gdiist@123"
    # Xilinx_id = "16:00.0"

    sender_path = "/home/gdiist/work/git/LBII_timetest/build/LBII"
    sender_rst_path = "/home/gdiist/work/git/pcie_hot_reset.sh"
    pwd = "123456789"
    Xilinx_id = "01:00.0"

    # deploy = lb2_deploy(download_dir,upload_dir,sender_path,sender_rst_path,pwd,Xilinx_id)
    # deploy.run(step=nStep,reset=False,xdma_id=0)

    # # Compare results or convert bin to npy
    check = lb2_checkRes(download_dir, upload_dir, nStep)
    check.binVSnpy(v_check=True)
    #check.bin2npy()
    #check.npyVSnpy()