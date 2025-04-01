# This file is used to convert the brainpy function to 32-bit SMT formula.

from .flow.smt_compiler import SMTCompiler
from ..SMT_Base import SMTBase

class SMT32bit(SMTBase):
    def __init__(self, netbase):
        super().__init__()
        
        self.netbase = netbase

    def func_to_32bit_smt(self,):
        # FPGA版本
        func = {"V": self.netbase.v_func}
        func.update( self.netbase.g_func)

        predefined_regs = {
            "g1": "R2",
            "g2": "R3",
        }

        i_compiler, v_compiler, smt_result = SMTCompiler.compile_all(
            func=func,
            preload_constants=self.netbase.cv,
            predefined_regs=predefined_regs,
            i_func=self.netbase.i_func["I"],
            update_method={"I": "update", "g1": "update", "g2": "update"},
            result_bits=self.result_bits,
        )

        all_constants = i_compiler.preload_constants | v_compiler.preload_constants
        printed_name = []
        register_constants = []
        all_constants_tmp = sorted(all_constants, key=lambda r: int(r.name[2:]))
        for pc in all_constants_tmp:
            if pc.name not in printed_name:
                printed_name.append(pc.name)
                register_constants.append(pc)
                
        return smt_result, register_constants