from pyrevolve import Operator, Checkpoint, Checkpointer
from functools import reduce
from operator import mul
import numpy as np

class DummyOperator(Operator):
    def __init__(self, name, flops, shape=(10, 10), **kwargs):
        self.name = name
        self.flops = flops
        self.shape = shape
        self.kwargs = kwargs

    def apply(self, din, dout, *args, **kwargs):
        t_s = kwargs['t_start']
        t_e = kwargs['t_end']
        for i in range(self.flops):
            dout[:] = din[:] + (t_e - t_s)
        

class DummyCheckpoint(Checkpoint):
    def __init__(self, symbols):
        self.symbols = symbols

    @property
    def dtype(self):
        return np.float32

    @property
    def size(self):
        return sum([reduce(mul, x.shape) for x in self.symbols.values()])

    
    def save(self, ptr):
        """Overwrite live-data in this Checkpoint object with data found at
        the ptr location."""
        i_ptr_lo = 0
        i_ptr_hi = 0
        for k, v in self.symbols.items():
            i_ptr_hi = i_ptr_hi + v.size
            ptr[i_ptr_lo:i_ptr_hi] = v.flatten()[:]
            i_ptr_lo = i_ptr_hi

    def load(self, ptr):
        """Copy live-data from this Checkpoint object into the memory given by
        the ptr."""
        i_ptr_lo = 0
        i_ptr_hi = 0
        for k, v in self.symbols.items():
            i_ptr_hi = i_ptr_hi + v.size
            v[:] = ptr[i_ptr_lo:i_ptr_hi].reshape(v.shape)
            i_ptr_lo = i_ptr_hi
