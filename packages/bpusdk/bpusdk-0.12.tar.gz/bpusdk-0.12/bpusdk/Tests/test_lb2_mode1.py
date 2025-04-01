import time
import warnings
import brainpy.math as bm
import numpy as np
import random
import math
from itertools import product
from tqdm import tqdm
import os
import shutil
from pathlib import Path
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
bm.set_dt(1.0)

def determinePopolationPos(iPopulation,X_TileNum,Y_TileNum):
    # 0: other, 1: right coloum, 2: bottom right
    if iPopulation == X_TileNum*Y_TileNum*16-1:
        return 2
    if (iPopulation % (X_TileNum*16)) == X_TileNum*16-1:
        return 1
    else:
        return 0

# 0: other, 1: right coloum, 2: bottom right 3: bottom top, 4:left colum
def determineTilePos(iTile,X_TileNum,Y_TileNum):
    if (iTile % (X_TileNum)) == 0:
        return 4
    
    if iTile == X_TileNum-1:
        return 3
    
    if iTile == (X_TileNum*Y_TileNum)-1:
        return 2
        
    if (iTile % (X_TileNum)) == X_TileNum-1:
        return 1
    
    else:
        return 0

# needed to nIntra or nInter > 1
def createConn_legend(nNeuron, X_TileNum, Y_TileNum):
    population_size = 1024
    nPopulation = math.ceil(nNeuron/population_size)
    res = []
    for iPopulation in tqdm(range(nPopulation)):
        case = determinePopolationPos(iPopulation,X_TileNum,Y_TileNum)
        nIntra = 4 if case == 2 else 2
        local_list = range(iPopulation*population_size, (iPopulation+1)*population_size)
        all_pairs = list(product(local_list, local_list))
        sampled_pairs = random.sample(all_pairs, nIntra * population_size)
        res.extend(sampled_pairs)

        nInter = 0 if case == 2 else 2
        match case:
            case 0:
                nInter = 2
                neighbor_list = range((iPopulation+1)*population_size,(iPopulation+2)*population_size)
                all_pairs = list(product(local_list, neighbor_list))
                sampled_pairs = random.sample(all_pairs, nInter * population_size)
                res.extend(sampled_pairs)
            case 1:
                nInter = 2
                neighbor_list = range((iPopulation+96)*population_size,(iPopulation+97)*population_size)
                all_pairs = list(product(local_list, neighbor_list))
                sampled_pairs = random.sample(all_pairs, nInter * population_size)
                res.extend(sampled_pairs)                    
    return np.array(res)

def trans_line(x):
    result = []
    for item in range(len(x), 0, -8):
        tmp = []
        var = x[item-8:item]
        tmp.extend([var[6:8], var[4:6], var[2:4], var[0:2]])
        tmp = list(map(lambda x: int(x, 16), tmp))
        result.extend(tmp)
    return result

# more efficient but only work if nIntra == nInter == 1
def createConn(nNeuron, X_TileNum, Y_TileNum):
    population_size = 1024
    nPopulation = math.ceil(nNeuron/population_size)
    res = []
    for iPopulation in range(nPopulation):
        #create intra-population connections for all populations
        local_idx = np.arange(iPopulation*population_size, (iPopulation+1)*population_size)
        #intra_pairs = np.stack((np.random.permutation(local_idx), np.random.permutation(local_idx)), axis=0)
        intra_pairs = np.stack((local_idx, np.roll(local_idx, -1)), axis=0)
        res.append(intra_pairs)

        #no inter-population connections for last population
        case = determinePopolationPos(iPopulation,X_TileNum,Y_TileNum)
        match case:
            case 0:
                iNeibor = iPopulation+1
                neighbor_idx = np.arange(iNeibor*population_size,(iNeibor+1)*population_size)
                #inter_pairs = np.stack((np.random.permutation(local_idx), np.random.permutation(neighbor_idx)), axis=0)
                inter_pairs = np.stack((local_idx, neighbor_idx), axis=0)
                
                res.append(inter_pairs)  
            case 1:
                iNeibor = iPopulation+96
                neighbor_idx = np.arange(iNeibor*population_size,(iNeibor+1)*population_size)
                #inter_pairs = np.stack((np.random.permutation(local_idx), np.random.permutation(neighbor_idx)), axis=0)
                inter_pairs = np.stack((local_idx, neighbor_idx), axis=0)
                res.append(inter_pairs)  
    
    res = np.hstack(res)
    return res

#return 4 char = 16b
def gethexString(rid,end):
    binary_r = format(rid, '010b')  
    binary_string = f"1{binary_r}{end}"
    hex_string = format(int(binary_string, 2), '04x') 
    return hex_string

#assume only one tile apart
def createRouter(download_dir, nTile, X_TileNum, Y_TileNum,hex=False):
    new_dir = Path(download_dir) / "route_info" if not hex else Path(download_dir)/ "hex" / "route_info" 
    if new_dir.exists():
        shutil.rmtree(new_dir)
    
    os.makedirs(new_dir, exist_ok=True)
    zeroPadding_4 = '0000' #16b
    changeRow = '\n' if hex else ''
    for rid in range(nTile):
        file_name = f"/route_info_{rid}.bin" if not hex else f"/route_info_{rid}.hex"
        outfile_path = download_dir+"/route_info"+ file_name if not hex else download_dir+ "/hex/route_info"+file_name
        case = determineTilePos(rid,X_TileNum,Y_TileNum)
        match case:
            case 0:
                element_hex = gethexString(rid, '10000')
                row_hex = zeroPadding_4*3 + element_hex+changeRow
                data = row_hex*15

                element_hex0 = gethexString(rid, '10001')
                element_hex1 = gethexString(rid-1, '10000')
                row_hex = zeroPadding_4*2 + element_hex1 + element_hex0 +changeRow
                data = row_hex + data    
            case 1:
                element_hex = gethexString(rid, '10000')
                row_hex = zeroPadding_4*3 + element_hex+changeRow
                data = row_hex*15

                element_hex0 = gethexString(rid, '10100')
                element_hex1 = gethexString(rid-1, '10000')
                element_hex2 = gethexString(rid-6, '10000')
                row_hex = zeroPadding_4 + element_hex2 +element_hex1 + element_hex0 +changeRow
                data = row_hex + data   
            case 2:
                element_hex = gethexString(rid, '10000')
                row_hex = zeroPadding_4*3 + element_hex+changeRow
                data = row_hex*15

                element_hex0 = gethexString(rid, '10000')
                element_hex1 = gethexString(rid-1, '10000')
                element_hex2 = gethexString(rid-6, '10000')
                row_hex = zeroPadding_4 + element_hex2 +element_hex1 + element_hex0 +changeRow
                data = row_hex + data    
            case 3:
                element_hex = gethexString(rid, '10000')
                row_hex = zeroPadding_4*3 + element_hex+changeRow
                data = row_hex*15

                element_hex0 = gethexString(rid, '10100')
                element_hex1 = gethexString(rid-1, '10000')
                row_hex = zeroPadding_4*2 +element_hex1 + element_hex0 +changeRow
                data = row_hex + data   
            case 4:
                element_hex = gethexString(rid, '10000')
                row_hex = zeroPadding_4*3 + element_hex +changeRow
                data = row_hex*15

                element_hex0 = gethexString(rid, '10001')
                row_hex = zeroPadding_4*3 + element_hex0 +changeRow
                data = row_hex + data          
         
        if hex:
            lines = data.split('\n')
            lines.reverse()
            with open(outfile_path, 'a') as f_in:
                for line in lines:
                    if len(line) > 0:
                        f_in.write(line+'\n')
        else:
            data = bytearray(trans_line(data))
            with open(outfile_path, 'wb') as f_in:
                f_in.write(data)


warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
bm.set_dt(1.0)

def gen_net(nExc,nInh):
    nNeuron = nExc+nInh

    t0 = time.time()
    connect_prob = createConn(576*1024,6,6)
    #arr = np.arange(nExc+nInh)
    #shuffled_arr = np.random.permutation(arr)
    conn = ["customized",connect_prob] 
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
        download_dir = "../../data5/28nm576k_new"
        upload_dir = "../../upload5/Res28nm576k_new"
        config_path = './HardwareConfig/Config_lb2.yaml'
        nExc = 288*1024
        nInh = 288*1024
        nStep = 10

        #Gendata
        net = gen_net(nExc,nInh)
        inpE = 100.                                       
        inpS = np.zeros((nStep, nExc+nInh))
        inpS = inpS.astype(bool)    
        bpuset = lb2_SNN(net, inpS, inpE, config_file=config_path)
        net.dump(download_dir,inpS,inpE,nStep,save=True,jit=True)     
        bpuset.gen_bin_data(download_dir,mode=1)
        res = createRouter(download_dir,36, 6, 6, hex=False)

        # Deploy
        # sender_path = "/home/gdiist/work/LBII/LBII/build/LBII"
        # sender_rst_path = "/home/gdiist/work/git_lbii/gdiist_host/pcie_hot_reset.sh"
        # pwd = "gdiist@123"
        # Xilinx_id = "16:00.0"

        sender_path = "/home/gdiist/work/git/LBII_timetest/LBII/build/LBII"
        sender_rst_path = "/home/gdiist/work/git/LBII/pcie_hot_reset.sh"
        pwd = "123456789"
        Xilinx_id = "01:00.0"

        deploy = lb2_deploy(download_dir,upload_dir,sender_path,sender_rst_path,pwd,Xilinx_id)
        deploy.run(step=nStep,reset=False,xdma_id=0)

        # # Compare results or convert bin to npy
        check = lb2_checkRes(download_dir, upload_dir, nStep)
        check.binVSnpy()
        # #check.npyVSnpy()