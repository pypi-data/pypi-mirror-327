from pathlib import Path
import numpy as np
from bpusdk.SNNCompiler.snn_compiler_64bit.func2smt_64bit_v0913 import SMT64bit
from bpusdk.BrainpyLib.Common import Fake, div_round_up

class Compiler28nmSNN():
    def __init__(self, config, neuron_num, bpbase) -> None:
        self.config = config
        self.bpbase = bpbase

        self.NodeNumOfNpu = config['Npu_NeuronNum']
        self.neuron_num = neuron_num

        self.npu_num = self.config['nRow']*self.config['nCol']*4
        
        self.smt64_compiler = SMT64bit(self.bpbase, self.config)

    def get_smt_64bit_result(self,):
        self.smt_result, self.syn_calcu_len, self.neu_calcu_len = self.smt64_compiler.func_to_64bit_smt()
        return self.smt_result, self.syn_calcu_len, self.neu_calcu_len

    def write_to_hex(self, save_dir):
        """Write hardware related to hex files
        """
        save_dir = Path(save_dir)
        output_dir = save_dir / 'hex'/'smt_64bit'
        output_dir.mkdir(exist_ok=True, parents=True)
        
        _ = self.get_smt_64bit_result()
        for npu_id in range(self.npu_num):
            hex_data = []
            hex_file_path = output_dir / f'smt_tile{npu_id//4}_npu{npu_id%4}.hex'

            for line in self.smt_result:
                instr_bin = "".join(line.bin_value_for_smt)
                parts = [instr_bin[i:i + 32]
                         for i in range(0, len(instr_bin), 32)]
                hex_parts = [format(int(part, 2), '08X') for part in parts]
                hex_data.append(''.join(hex_parts))
            while len(hex_data) < 1024:
                hex_parts = [''.join(['0' * 16])]
                hex_data.extend(hex_parts)

            with open(hex_file_path, 'wt') as f_tmp:
                for item in hex_data:
                    f_tmp.write(item + '\n')


    def write_to_bin(self, save_dir):
        """Write hardware related to bin files
        """
        save_dir = Path(save_dir)
        output_dir = save_dir / 'smt_64bit'
        output_dir.mkdir(exist_ok=True, parents=True)
        
        _ = self.get_smt_64bit_result()
        instr_bin_all = np.zeros(1024, dtype=np.uint64)
        for n in range(1024):
            if n < len(self.smt_result):
                instr_bin = ''.join(self.smt_result[n].bin_value_for_smt)
                value = int(instr_bin, 2)
                instr_bin_all[n] = value
        for npu_id in range(self.npu_num):
            bin_file_path = output_dir / f'smt_tile{npu_id//4}_npu{npu_id%4}.bin'
            bin_file_path.unlink(missing_ok=True)
            Fake.fwrite(file_path=bin_file_path,
                        arr=instr_bin_all, dtype="<u8")