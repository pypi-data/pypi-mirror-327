import math
from addict import Dict as AttrDict

from .flow.smt_64_compiler import SMT64Compiler
from .backend.smt_64_op import OPType, RD_OPType, RS_OPType, ALU_OPType
from .backend.smt_64_op import SMT_ASSIGN_I, SMT_RW, SMT_RC
from .common.smt_64_reg import RegisterCollection
from .common.asm_IEEE754 import IEEE754, IBinary

from .SMT_base import *
from BrainpyLib.BrainpyBase import BrainpyBase


class SMT64bit():
    def __init__(self, netbase: BrainpyBase, config):
        super().__init__()
        
        self.netbase = netbase
        self.cv = self.netbase.cv
        
        self.base = config['Base']
        self.split = config['Split']
        self._dtype = config['Dtype']

    def func_to_64bit_smt(self,):
        
        # get function 
        funcs, params = get_funcs(self.base, self.cv, self._dtype, self.netbase)
        predefined_regs, reg_var_list, reg_wacc_list = get_predefined_regs(self.base, self.split, self.netbase)
        
        # get const list
        const_list = get_const_list(params)
        
        constants = {"V_th": self.netbase.cv.V_th,
                     "d": getattr(self.netbase.cv, 'd', 1.0)}
        # get smt of function  
        _, _, statements = SMT64Compiler.compile_all(funcs=funcs,
                                                     constants=constants, 
                                                     predefined_regs=predefined_regs)

        smt_result = []
        smt_register = RegisterCollection()
        
        # PART 1: NOP
        smt_result.append(SMT_RW(OP_TYPE=OPType.NOP))
        # PART 2: NCU_SR init
        ncu = 1
        while ncu <= 8:
            for i in range(16):
                instr = SMT_ASSIGN_I(OP_TYPE=OPType.ASSIGN_IMM, 
                                    NCU=ncu, 
                                    IMM=const_list[i], 
                                    RD_REG_0=smt_register.SR_regs[i], 
                                    RD_REG_1=smt_register.SR_regs[i])
                smt_result.append(instr)
            ncu+=1
        # PART 3: NCU_ER init
        ncu = 1
        imm = 146
        while ncu <= 8:
            for i in range(16):
                instr = SMT_ASSIGN_I(OP_TYPE=OPType.ASSIGN_IMM, 
                                    NCU=ncu, 
                                    IMM=imm, 
                                    RD_OP_0 = RD_OPType.NCU_ER_RD_P,
                                    RD_REG_0=smt_register.regs[i], 
                                    RD_OP_1 = RD_OPType.NCU_ER_RD_P,
                                    RD_REG_1=smt_register.regs[i])
                smt_result.append(instr)
                imm+=1
            ncu+=1
        # PART 4: syn_calcu
        tmp_len0= len(smt_result)
        smt_result.append(SMT_RW(OP_TYPE=OPType.BUS_LOAD))
        smt_result.append(SMT_RW(OP_TYPE=OPType.SRAM_LOAD))
        smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(3)])
        smt_result.append(get_w_acc(self.base, self.split, reg_wacc_list))
        # smt_result.extend(get_w_add_const())
        smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(5)])
        smt_result.append(SMT_RW(OP_TYPE=OPType.SRAM_SAVE))
        tmp_len1= len(smt_result)
        smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(385-tmp_len1)])
        syn_calcu_len = len(smt_result) - tmp_len0
        
        # PART 5: neu_calcu
        tmp_len2 = len(smt_result)
        smt_result.append(SMT_RW(OP_TYPE=OPType.SRAM_LOAD))
        smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(3)])
        smt_result.extend(statements)
        smt_result.append(get_vset_const())
        smt_result.append(SMT_RW(OP_TYPE=OPType.NOP))
        smt_result.append(SMT_RW(OP_TYPE=OPType.NOP))
        smt_result.append(SMT_RW(OP_TYPE=OPType.NOP))
        smt_result.append(SMT_RW(OP_TYPE=OPType.NOP))
        smt_result.append(get_vset(self.base, reg_var_list))
        smt_result.append(SMT_RW(OP_TYPE=OPType.SPIKE_GEN))
        smt_result.append(SMT_RW(OP_TYPE=OPType.NOP))
        smt_result.append(SMT_RW(OP_TYPE=OPType.SRAM_SAVE))
        tmp_len3= len(smt_result)
        if tmp_len3 < 513:
            smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(513-tmp_len3)])
            neu_calcu_len = len(smt_result) - tmp_len2
        
            # PART 6: syn_update_calcu:
            smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(128)])
            # PART 7: gemm_calcu
            smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(128)])
        else:
            smt_result.extend([SMT_RW(OP_TYPE=OPType.NOP) for _ in range(769-tmp_len3)])
            neu_calcu_len = tmp_len3 - tmp_len2 + 10
            
        
                    
        return smt_result, syn_calcu_len, neu_calcu_len
