import math
from addict import Dict as AttrDict
import numpy as np
import brainpy as bp
import brainpy.math as bm
from brainpy._src.integrators import JointEq
from brainpy._src.dyn.neurons.base import GradNeuDyn, NeuDyn    
from .flow.smt_64_compiler import SMT64Compiler
from .backend.smt_64_op import OPType, RD_OPType, RS_OPType, ALU_OPType
from .backend.smt_64_op import SMT_ASSIGN_I, SMT_RW, SMT_RC, SMT_IC
from .common.smt_64_reg import RegisterCollection, Register64
from .common.asm_IEEE754 import IEEE754, IBinary
from BrainpyLib.BrainpyBase import BrainpyBase
from .backend.smt_64_stmt import SMT64

def get_const_list(params):
    
    # region
    const = AttrDict()
    const.W_decay1  = 00.
    const.W_decay2  = 00.
    const.RC_decay  = 00.
    const.vu4 = 00.
    const.gu1 = 00.
    const.gu2 = 00.
    const.gu3 = 00.
    const.gu4 = 00.       
    const.e1 = 00.
    const.e2 = 00.
    const.e3 = 00.
    const.e4 = 00.
    const.E1 = 00.
    const.E2 = 00.
    const.vrst = params["c"] if "c" in params else params["V_reset"]
    const.trst = params["tau_ref"]
    # endregion
    const_list = []
    for _, value in const.items():
        const_list.append(value)
        
    return const_list


def get_predefined_regs(base, split, netbase: BrainpyBase):
    
    # base1 
    if base == 1 and split == 1:
        predefined_regs = {
            "V": "R2",
            "g1": "R3",
            "g2": "R5",
            'LIF_sum_w0' : 'R10',
            'LIF_sum_w1' : 'R11',
        }
        if "u" in netbase.remaining_params:
            predefined_regs["u"] = "R4"
            reg_var_list = [2, 4]
            reg_wacc_list = [3, 10, 5, 11]
        else:
            reg_var_list = [2]
            reg_wacc_list = [3, 10, 5, 11]
            
            
        
    elif base == 1 and split == 2:
        predefined_regs = {
            "V": "R2",
            "g1": "R3",
            'LIF_sum_w0' : 'R10',
        }
        reg_var_list = [2]
        reg_wacc_list = [3, 10]
        
        
    elif base == 1 and split == 4:
        predefined_regs = {
            "V": "R2",
            "g1": "R4",
            'LIF_sum_w0' : 'R9',
        }
        
        reg_var_list = [2]
        reg_wacc_list = [4, 9]

    # base2
    elif base == 2 and split == 1:
        predefined_regs = {
            "V1": "R5",
            "V2": "R2",
            "g1": "R6",
            "g2": "R3",
            'LIF_sum_w0' : 'R14',
            'LIF_sum_w1' : 'R11',
        }
        reg_var_list = [5, 2]
        reg_wacc_list = [6, 14, 3, 11]
        
        
    elif base == 2 and split == 2:
        predefined_regs = {
            "V1": "R5",
            "V2": "R2",
            "g1": "R6",
            "g2": "R3",
            'LIF_sum_w0' : 'R11',
            'LIF_sum_w1' : 'R10',
        }
        reg_var_list = [5, 2]
        reg_wacc_list = [6, 11, 3, 10]
        
    return predefined_regs, reg_var_list, reg_wacc_list



def get_params_dtype(dtype, params):
    
    if dtype == 'fp32':
        pass
    elif dtype == 'fp16':
        params["tau"] = 1 / params["tau"]
        for key, value in params.items():
            if key in ['V_rest', 'V_th', 'R', 'I_input',
                        'tau', 'tau1', 'tau2', 'tau_ref', 'dt', 'E1', 'E2', 
                        "p1", "p2", "p3", "a", "b", "c", "d"]:
                assert isinstance(value, float)
                fp16 = np.float16(value)
                fp16_hex = fp16.tobytes()[::-1].hex()
                fp16_dec = int(fp16_hex + fp16_hex, 16)  # 3548435328, 'd380d380'
                params[key] = IEEE754.ieee754_to_float(fp16_dec)
    elif dtype == 'int8':
        for key, value in params.items():
            if key in ['V_rest', 'V_th', 'R', 'I_input',
                        'tau_inverse', 'tau1', 'tau2','tau_ref', 'dt', 'E1', 'E2','fac'
                        "p1", "p2", "p3", "a", "b", "c", "d"]:
                value = int(value)
                print(f"key: {key}, value: {value}")
                assert isinstance(value, int)
                v_dec = np.uint32((value<<24) + (value<<16) + (value<<8) + (value<<0))
                params[key] = IEEE754.ieee754_to_float(v_dec)
        params["V_th"] = f'{params["V_th"]:.60f}'
    else:
        raise ValueError("Unsupported dtype: {}".format(dtype))
    
    return params

    
def get_funcs(base, params, dtype, netbase: BrainpyBase):
    # get different params for different dtype
    params = get_params_dtype(dtype, params)
    
    if base == 1 or 2:
        func = netbase.v_func
        func.update(netbase.i_func)
        if 'V' in func:
            func['V_d'] = func['V']
            del func['V']

        if 'u' in func:
            func['u_d'] = func['u']
            del func['u']
            
        func.update(netbase.g_func)
    

    return func, params

def get_w_acc(base, split, reg_wacc_list):
    
    if base == 1 and split in [1, 2]:
        reg_list = reg_wacc_list
        result = SMT_RC(OP_TYPE=OPType.CALCU_REG, 
                ALU1_OP = ALU_OPType.ADD_OP,
                RS1_OP_0 = RS_OPType.NCU_ER_P,
                RS1_REG_0 = RegisterCollection().regs[reg_list[0]],
                RS1_OP_1  = RS_OPType.NCU_ER_P,
                RS1_REG_1 = RegisterCollection().regs[reg_list[1]],
                RD1_OP  = RD_OPType.NCU_ER_RD_P,
                RD1_REG = RegisterCollection().regs[reg_list[0]],
                ALU2_OP = ALU_OPType.ADD_OP,
                RS2_OP_0 = RS_OPType.NCU_ER_P,
                RS2_REG_0 = RegisterCollection().regs[reg_list[2]],
                RS2_OP_1  = RS_OPType.NCU_ER_P,
                RS2_REG_1 = RegisterCollection().regs[reg_list[3]],
                RD2_OP   = RD_OPType.NCU_ER_RD_P,
                RD2_REG = RegisterCollection().regs[reg_list[2]]
                )
    elif base == 1 and split == 4:
        reg_list = reg_wacc_list
        result = SMT_RC(OP_TYPE=OPType.CALCU_REG, 
                ALU1_OP = ALU_OPType.ADD_OP,
                RS1_OP_0 = RS_OPType.NCU_ER_P,
                RS1_REG_0 = RegisterCollection().regs[reg_list[0]],
                RS1_OP_1  = RS_OPType.NCU_ER_P,
                RS1_REG_1 = RegisterCollection().regs[reg_list[1]],
                RD1_OP  = RD_OPType.NCU_ER_RD_P,
                RD1_REG = RegisterCollection().regs[reg_list[0]],)
    
    elif base == 2 and split == 1:
        reg_list = reg_wacc_list
        result = SMT_RC(OP_TYPE=OPType.CALCU_REG, 
                ALU1_OP = ALU_OPType.ADD_OP,
                RS1_OP_0 = RS_OPType.NCU_ER_P,
                RS1_REG_0 = RegisterCollection().regs[reg_list[0]],
                RS1_OP_1  = RS_OPType.NCU_ER_P,
                RS1_REG_1 = RegisterCollection().regs[reg_list[1]],
                RD1_OP  = RD_OPType.NCU_ER_RD_P,
                RD1_REG = RegisterCollection().regs[reg_list[0]],
                ALU2_OP = ALU_OPType.ADD_OP,
                RS2_OP_0 = RS_OPType.NCU_ER_P,
                RS2_REG_0 = RegisterCollection().regs[reg_list[2]],
                RS2_OP_1  = RS_OPType.NCU_ER_P,
                RS2_REG_1 = RegisterCollection().regs[reg_list[3]],
                RD2_OP   = RD_OPType.NCU_ER_RD_P,
                RD2_REG = RegisterCollection().regs[reg_list[2]]
                )
        
    elif base == 2 and split == 2:
        reg_list = reg_wacc_list
        result = SMT_RC(OP_TYPE=OPType.CALCU_REG, 
                ALU1_OP = ALU_OPType.ADD_OP,
                RS1_OP_0 = RS_OPType.NCU_ER_P,
                RS1_REG_0 = RegisterCollection().regs[reg_list[0]],
                RS1_OP_1  = RS_OPType.NCU_ER_P,
                RS1_REG_1 = RegisterCollection().regs[reg_list[1]],
                RD1_OP  = RD_OPType.NCU_ER_RD_P,
                RD1_REG = RegisterCollection().regs[reg_list[0]],
                ALU2_OP = ALU_OPType.ADD_OP,
                RS2_OP_0 = RS_OPType.NCU_ER_P,
                RS2_REG_0 = RegisterCollection().regs[reg_list[2]],
                RS2_OP_1  = RS_OPType.NCU_ER_P,
                RS2_REG_1 = RegisterCollection().regs[reg_list[3]],
                RD2_OP   = RD_OPType.NCU_ER_RD_P,
                RD2_REG = RegisterCollection().regs[reg_list[2]]
                )    

    return result


def get_w_add_const():
    update_v = f"""
        1: NOP
        2: NOP
        3: NOP
        4: NOP
        5: R_4 = R_4 + 0.0
        """
    result = list(SMT64.create_from_expr(update_v, regs=RegisterCollection().regs))
    return result

def get_vset_const():
    result = SMT_IC(OP_TYPE=OPType.CALCU_IMM, 
                    IMM = 0.,
                    ALU1_OP = ALU_OPType.ADD_OP,
                    RS1_OP = RS_OPType.NCU_SR_P,
                    RS1_REG = RegisterCollection().SR_regs[14],
                    RD1_OP = RD_OPType.NCU_ER_RD_P,
                    RD1_REG = RegisterCollection().regs[7])
    return result


def get_vset(base, reg_var_list):
    
    if base == 1:
        # TODO, uger, invoke a function to get the reg_list from 'predefined_regs'
        reg_list = reg_var_list  # [2, 4]
        
        if len(reg_list) == 1:
            result = SMT_RC(OP_TYPE=OPType.VSET, 
                            ALU1_OP = ALU_OPType.ENABLE_OP, 
                            RS1_OP_0 = RS_OPType.NCU_SR_P,
                            RS1_REG_0 = RegisterCollection().SR_regs[14],
                            RS1_OP_1  = RS_OPType.NCU_SR_P,
                            RS1_REG_1= RegisterCollection().SR_regs[14],
                            RD1_OP  = RD_OPType.NCU_ER_RD_P,
                            RD1_REG= RegisterCollection().regs[reg_list[0]])
            
        elif len(reg_list) == 2: 
            result = SMT_RC(OP_TYPE=OPType.VSET, 
                ALU1_OP = ALU_OPType.ENABLE_OP, 
                RS1_OP_0 = RS_OPType.NCU_SR_P,
                RS1_REG_0 = RegisterCollection().SR_regs[14],
                RS1_OP_1 = RS_OPType.NCU_SR_P,
                RS1_REG_1 = RegisterCollection().SR_regs[14],
                RD1_OP = RD_OPType.NCU_ER_RD_P,
                RD1_REG = RegisterCollection().regs[reg_list[0]], 
                
                ALU2_OP = ALU_OPType.ENABLE_OP,
                RS2_OP_0 = RS_OPType.NCU_ER_P,
                RS2_REG_0 = RegisterCollection().regs[15],
                RS2_OP_1 = RS_OPType.NCU_ER_P,
                RS2_REG_1 = RegisterCollection().regs[15],
                RD2_OP = RD_OPType.NCU_ER_RD_P,
                RD2_REG = RegisterCollection().regs[reg_list[1]])
            
            
            
            
    elif base == 2:
        reg_list = reg_var_list # [5, 2]
        result = SMT_RC(OP_TYPE=OPType.VSET, 
                ALU1_OP = ALU_OPType.ENABLE_OP, 
                RS1_OP_0 = RS_OPType.NCU_SR_P,
                RS1_REG_0 = RegisterCollection().SR_regs[14],
                RS1_OP_1 = RS_OPType.NCU_SR_P,
                RS1_REG_1 = RegisterCollection().SR_regs[14],
                RD1_OP = RD_OPType.NCU_ER_RD_P,
                RD1_REG = RegisterCollection().regs[reg_list[0]], 
                
                ALU2_OP = ALU_OPType.ENABLE_OP,
                RS2_OP_0 = RS_OPType.NCU_SR_P,
                RS2_REG_0 = RegisterCollection().SR_regs[14],
                RS2_OP_1 = RS_OPType.NCU_SR_P,
                RS2_REG_1 = RegisterCollection().SR_regs[14],
                RD2_OP = RD_OPType.NCU_ER_RD_P,
                RD2_REG = RegisterCollection().regs[reg_list[1]])
    return result