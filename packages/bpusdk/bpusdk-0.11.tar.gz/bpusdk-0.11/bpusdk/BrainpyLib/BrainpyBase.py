import copy
import math
import pickle
import re
from collections import defaultdict

import brainpy as bp
import brainpy.math as bm
import numpy as np
from addict import Dict as AttrDict
from brainpy._src.dyn.neurons.base import GradNeuDyn, NeuDyn
from brainpy._src.initialize import parameter, variable_
from scipy.sparse import csr_matrix
from brainpy._src.context import share


def checkAttr(proj):
    """Determine whether the Proj is valid.
    """
    cond1 = hasattr(proj, "comm") and hasattr(proj, "syn") and hasattr(proj, "pre") and hasattr(proj, "post")
    if hasattr(proj, "refs"):
        cond2 = ("comm" in proj.refs) and ("syn" in proj.refs) and ("pre" in proj.refs) and ("post" in proj.refs)
        return cond1 or cond2
    return cond1


def getAttribute(element, attribute):
    """Subtract subparts from FullProjAlign or exponential
    """
    if hasattr(element, "refs"):
        return element.refs[attribute]
    else:
        if attribute == "out":
            attribute = "output"
        return getattr(element, attribute)

    
class BrainpyBase():
    """Class to extract information from Brainpy network.

    There are several essential attributes:

    - ``neuron_num``: The total number of neurons in the network.
    - ``nConn``: The total number of synapses in the network. 
    - ``cv``: The dictionaty storing neuron synapse parameters 

    Args:
        network: The network to extract information from.
        inpE: The constant current input to the network.
        config: The dictionary of hardware configuration.
    """

    def __init__(self, network, inpE, config) -> None:
        self.network = network
        self.base = config["Base"] if "Base" in config else 1
        self.Dtype = config["Dtype"] if "Dtype" in config else "fp32"
        self.log = ["-----------Brainpybase-----------\n"]

        self.cv = AttrDict()
        self.cv["I_input"] = inpE
        self.count_neuron()
        self.count_proj()

        self.get_neuron_property()
        self.get_neuron_log()
        self.get_proj_property()
        self.get_proj_log()

    
    def count_neuron(self):
        """Substract nNeuron for each population, count it's global starting/ending index, 
        and check if all populations are of same type.
        """
        self.index_map = {}
        neuron_name_list = []
        last_index = 0
        for neuron_group in self.network.nodes().subset(NeuDyn).values():
            start_index = last_index
            end_index = start_index + neuron_group.size[0]
            self.index_map[neuron_group.name] = (start_index, end_index)
            last_index = end_index

            name = ''.join(re.findall(r'[a-zA-Z]', neuron_group.name))
            neuron_name_list.append(name)
        self.neuron_num = max(end_index for _, end_index in self.index_map.values())
        
        if all(x == neuron_name_list[0] for x in neuron_name_list):
            self.neuron_name = neuron_name_list[0]
        else:
            raise TypeError("All neurons need be of same type")

   
    def get_neuron_property(self):
        """Substract parameters from neuron populations.
        """
        self.Vinit = []
        bm.random.seed(int(self.network.initState[1]))
        for neuronGroup in self.network.nodes().subset(NeuDyn).values():
            name = ''.join(re.findall(r'[a-zA-Z]', neuronGroup.name))
            # match name:
            #     case "LifRef":
            if name == "LifRef":
                self.cv["V_reset"] = getattr(neuronGroup, "V_reset", -60.0)
                self.cv["V_th"] = getattr(neuronGroup, "V_th")
                self.cv["tau_ref"] = np.round(getattr(neuronGroup, "tau_ref", 5.0)/bm.get_dt())
                self.cv["V_rest"] = getattr(neuronGroup, "V_rest", -60.0)
                self.cv["tau"] = getattr(neuronGroup, "tau", 20)
                self.cv["tau_inverse"] = 1/self.cv["tau"]
                self.cv["R"] = getattr(neuronGroup, "R", 1)
                self.cv["dt"] = bm.get_dt()
    
            # case "IzhikevichRef":
            elif name == "LifRef":
                self.cv["p1"] = getattr(neuronGroup, "p1", 0)
                self.cv["p2"] = getattr(neuronGroup, "p2", 0)
                self.cv["p3"] = getattr(neuronGroup, "p3", 0)
                self.cv["a"] = getattr(neuronGroup, "a", 0)
                self.cv["b"] = getattr(neuronGroup, "b", 0)
                self.cv["c"] = getattr(neuronGroup, "c", 0)
                self.cv["d"] = getattr(neuronGroup, "d", 0)
                self.cv["R"] = getattr(neuronGroup, "R", 1)
                self.cv["dt"] = bm.get_dt()
                self.cv["tau_ref"] = np.round(getattr(neuronGroup, "tau_ref", 5.0)/bm.get_dt())
                self.cv["V_th"] = getattr(neuronGroup, "V_th")
                
                # case _:
            else:
                raise NotImplementedError      

            if hasattr(neuronGroup, '_V_initializer'):
                V_initializer = neuronGroup._V_initializer
            else:
                V_initializer = bp.init.ZeroInit()
            V_init = variable_(V_initializer,sizes=neuronGroup.size).value
            self.Vinit.extend(V_init)
        self.Vinit = np.array(self.Vinit)

    
    def get_neuron_log(self):
        """Generate log for neuron populations.
        """
        neuron_log = []
        for neuronGroup in self.network.nodes().subset(NeuDyn).values():
            neuron_log.append(f"Neuron Group: {neuronGroup.name} \n")
            neuron_log.append(f"Number of Neurons: {neuronGroup.size[0]} \n")

            if hasattr(neuronGroup, '_V_initializer'):
                V_initializer = neuronGroup._V_initializer
            else:
                V_initializer = bp.init.ZeroInit()
            neuron_log.append(f"V_initializer: {str(V_initializer)} \n")
            neuron_log.append(f"\n")
        
        #paramerter_log outside of loop since assume all population have same parameters
        neuron_log.append(f"Neuron Parameters: \n")
        for item in self.cv:
            neuron_log.append(f"\t{item}: {self.cv[item]} \n")      
        neuron_log.append(f"\n")  
        self.log.extend(neuron_log)

    
    def count_proj(self):
        """Sort synapses by prepopulation, and extract syn/out name. 
        """
        self.synapse_dict = {}
        syn_name_list = []
        out_name_list = []
        for proj in self.network.nodes().subset(bp.Projection).values():
            if checkAttr(proj):
                pre = getAttribute(proj, "pre")
                if pre in self.synapse_dict:
                    self.synapse_dict[pre].append(proj)
                else:
                    self.synapse_dict[pre] = [proj]

                out_name = getAttribute(proj, "out").name
                out_name = ''.join(re.findall(r'[a-zA-Z]', out_name))
                out_name_list.append(out_name)   

                syn_name = getAttribute(proj, "syn").name
                syn_name = ''.join(re.findall(r'[a-zA-Z]', syn_name))
                syn_name_list.append(syn_name)

        if all(x == syn_name_list[0] for x in syn_name_list):
            self.syn_name = syn_name_list[0]
        else:
            raise TypeError("All syn need be of same type")
        
        if all(x == out_name_list[0] for x in out_name_list):
            self.out_name = out_name_list[0]
        else:
            raise TypeError("All out need be of same type")
        

    def get_proj_property(self):
        """Substract parameters from synapses.
        """
        for iPre, pre in enumerate(self.synapse_dict):
            proj = self.synapse_dict[pre][0]
            self.cv[f"tau{iPre+1}"] = proj.syn.tau
            self.synapseName = ''.join(re.findall(
                r'[a-zA-Z]', getAttribute(proj, "out").name))
            if self.synapseName == 'COBA':
                self.cv[f"E{iPre+1}"] = getAttribute(proj, "out").E if hasattr(proj, "refs") else proj.output.E

    def get_proj_log(self):
        """Generate log for synapses.
        """
        proj_log = []
        for iPre, pre in enumerate(self.synapse_dict):
            for proj in self.synapse_dict[pre]:
                proj_log.append(f"Proj: {str(proj)} \n")
                proj_log.append(f"\tWeight: {getAttribute(proj, 'comm').weight} \n")        
                proj_log.append(f"\tPre: {getAttribute(proj, 'pre').name} \n")
                # proj_log.append(f"\tdelay: {getAttribute(proj, 'delay').name} \n")  
                # proj_log.append(f"\tcomm: {getAttribute(proj, 'comm').name} \n")  
                proj_log.append(f"\tsyn: {getAttribute(proj, 'syn').name} \n")  
                proj_log.append(f"\tout: {getAttribute(proj, 'out').name} \n")  
                if re.match(r"[A-Z]\w+\d+", getAttribute(proj, 'out').name) == "COBA":
                    proj_log[-1] += f" (E: {getAttribute(proj, 'out').E})"
                proj_log.append(f"\tpost: {getAttribute(proj, 'post').name} \n")  
                proj_log.append(f"\n")
        self.log.extend(proj_log)

    def get_connection_matrix(self):
        """return global connection in form of dictionary.
        """
        self.layers = {}
        for name in self.network.nodes().subset(bp.Projection):
            if re.match(r"[A-Z]\w+\d+", name) and checkAttr(self.network.nodes().subset(bp.Projection)[name]):
                self.layers[name] = self.network.nodes().subset(bp.Projection)[
                    name]

        self.connection_matrix = defaultdict(dict)
        for conn in self.layers.values():
            src_offset = self.index_map[getAttribute(conn, "pre").name][0]
            dst_offset = self.index_map[getAttribute(conn, "post").name][0]

            if isinstance(conn.comm, bp.dnn.EventCSRLinear):
                indices = conn.comm.indices
                if len(indices) != 0:
                    indptr = conn.comm.indptr
                    rows = indptr.size - 1
                    cols = int(np.max(indices) + 1) 
                    if isinstance(conn.comm.weight, float): 
                        data = np.ones(indptr[-1]) * conn.comm.weight
                        compressed = csr_matrix((data, indices, indptr), shape=(rows, cols), dtype=np.float32).tocoo()
                        for i, j, k in zip(compressed.row, compressed.col, compressed.data):
                            src_abs_id = int(i + src_offset)
                            dst_abs_id = int(j + dst_offset)
                            self.connection_matrix[src_abs_id][dst_abs_id] = k
                    else:
                        data = np.ones(indptr[-1], dtype=np.uint32) * conn.comm.weight
                        compressed = csr_matrix((data, indices, indptr), shape=(rows, cols), dtype=np.uint32).tocoo()
                        for i, j, k in zip(compressed.row, compressed.col, compressed.data):
                            src_abs_id = int(i + src_offset)
                            dst_abs_id = int(j + dst_offset)
                            self.connection_matrix[src_abs_id][dst_abs_id] = k
                        
            elif isinstance(conn.comm, bp.dnn.EventJitFPHomoLinear):
                conn_matrix = conn.comm.get_conn_matrix()
                compressed = csr_matrix(
                    conn_matrix, dtype=np.float32).tocoo()
                if isinstance(conn.comm.weight, float):
                    data = np.ones(compressed.row.size) * conn.comm.weight
                    for i, j, k in zip(compressed.col, compressed.row, compressed.data):
                        src_abs_id = int(i + src_offset)
                        dst_abs_id = int(j + dst_offset)
                        self.connection_matrix[src_abs_id][dst_abs_id] = np.single(
                            k).view("uint32")
                else:
                    data = np.ones(compressed.row.size,
                                   dtype=np.uint32) * conn.comm.weight
                    for i, j, k in zip(compressed.col, compressed.row, compressed.data):
                        src_abs_id = int(i + src_offset)
                        dst_abs_id = int(j + dst_offset)
                        self.connection_matrix[src_abs_id][dst_abs_id] = np.uint32(
                            k).view("uint32")
            else:
                raise NotImplementedError

        self.nConn = sum(len(inner_dict) for inner_dict in self.connection_matrix.values())
        return self.connection_matrix

    def get_neuron_num(self):
        """Return the total number of neurons in the network.
        """
        return self.neuron_num

    @property
    def v_func(self,):
        """Return the neuron's membrane potential update formula in the form of an anonymous function,
        based on the neuron type and selected hardware configuration. 
        """
        neuron_update_rule = {"LifRef": [{"V": lambda I, V: V +(self.cv["V_rest"]-V+self.cv["R"]*(I+self.cv["I_input"]))*self.cv["tau_inverse"]*self.cv["dt"]},
                                         {"V1": lambda I1, V1: V1 + (self.cv["V_rest"]-V1+self.cv["R"]*(I1+self.cv["I_input"]))*self.cv["tau_inverse"]*self.cv["dt"],
                                          "V2": lambda I2, V2: V2 + (self.cv["V_rest"]-V2+self.cv["R"]*(I2+self.cv["I_input"]))*self.cv["tau_inverse"]*self.cv["dt"]}],
                              "Izhikevich":[{"V": lambda I, V, u: V + (self.cv["p1"] * V * V + self.cv["p2"] * V + self.cv["p3"] - u + I)*self.cv["dt"], 
                                             "u": lambda V, u: u + self.cv["a"] * (self.cv["b"] * V - u) * self.cv["dt"]},
                                            {"V1": lambda I1, V1, u1: V1 + (self.cv["p1"] * V1 * V1 + self.cv["p2"] * V1 + self.cv["p3"] - u1 + I1)*self.cv["dt"],
                                             "V2": lambda I2, V2, u2: V2 + (self.cv["p1"] * V2 * V2 + self.cv["p2"] * V2 + self.cv["p3"] - u2 + I2)*self.cv["dt"],
                                             "u1": lambda V1, u1: u1 + self.cv["a"] * (self.cv["b"] * V1 - u1) * self.cv["dt"],
                                             "u2": lambda V2, u2: u2 + self.cv["a"] * (self.cv["b"] * V2 - u2) * self.cv["dt"]}]
                              }
        # match self.neuron_name:
        #     case "LifRef":
        if self.neuron_name == "LifRef":
            neuron_update_rule = neuron_update_rule["LifRef"]
        #     case "IzhikevichRef":
        elif self.neuron_name == "IzhikevichRef":
            neuron_update_rule = neuron_update_rule["Izhikevich"]
        #     case _:
        else:
            raise NotImplementedError      
        
        # match self.base:
        #     case 1:
        if self.base == 1:
            return neuron_update_rule[0]
        #     case 2:
        elif self.base == 2:
            return neuron_update_rule[1]
        #     case _:
        else:
            raise ValueError("Invalid base")

    @property
    def i_func(self,):
        """Return the synaptic output formula in the form of an anonymous function,
        based on the neuron type and selected hardware configuration.
        """
        out_update_rule =  {"COBA":[{"I": lambda g1,g2,V: self.cv['R'] * g1* (self.cv['E1'] - V) + self.cv['R'] * g2 * (self.cv['E2'] - V)},
                                    {"I1": lambda g1, g2, V1: self.cv['R'] * g1 * (self.cv['E1'] - V1) + self.cv['R'] * g2 * (self.cv['E2'] - V1),
                                     "I2": lambda g1, g2, V2: self.cv['R'] * g1 * (self.cv['E1'] - V2) + self.cv['R'] * g2 * (self.cv['E2'] - V2)}],
                            "CUBA":[{"I": lambda g1, g2, V: self.cv['R'] * g1 + self.cv['R'] * g2},
                                    {"I1": lambda g1, g2, V1: self.cv['R'] * g1+ self.cv['R'] * g2,
                                     "I2": lambda g1, g2, V2: self.cv['R'] * g1+ self.cv['R'] * g2}]}
        # match self.out_name:
        #     case "COBA":
        if self.out_name == "COBA":
            out_update_rule = out_update_rule["COBA"]
        #     case "CUBA":
        elif self.out_name == "CUBA":
            out_update_rule = out_update_rule["CUBA"]
        #     case _:
        else:
            raise NotImplementedError     
        
        # match self.base:
        #     case 1:
        if self.base == 1:
            return out_update_rule[0]
        #     case 2:
        elif self.base == 2:
            return out_update_rule[1]
        #     case _:
        else:
            raise ValueError("Invalid base")

    @property
    def g_func(self,):
        """Return the synaptic decay formula in the form of an anonymous function,
        based on the neuron type and selected hardware configuratio
        """
        syn_update_rule = {"Expon":[{"g1": lambda g1: g1 - g1/self.cv['tau1']*self.cv['dt'],
                                    "g2": lambda g2: g2 - g2/self.cv['tau2']*self.cv['dt']}],
                           "ConstantExpon":[{"g1": lambda g1: g1 *self.cv['R'],
                                    "g2": lambda g2: g2 *self.cv['R']}]}
                                  
        # match self.syn_name:
        #     case "Expon":
        if self.syn_name == "Expon":
            syn_update_rule = syn_update_rule["Expon"]
        #     case "ConstantExpon":
        elif self.syn_name == "ConstantExpon":
            syn_update_rule = syn_update_rule["ConstantExpon"]
        #     case _:
        else:
            raise NotImplementedError   
        return syn_update_rule[0]  

    @property
    def v_variables(self,):
        for ds in self.network.nodes().subset(NeuDyn).values():
            return ds.integral.variables

    @property
    def remaining_params(self,):
        return [key for key in self.v_variables if key not in ('V', 't', 'I')]  # "R6" ~ "R7"
    
    @property
    def neuron_nums(self):
        return self.neuron_num