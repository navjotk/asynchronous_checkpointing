import numpy as np
from functools import reduce
from operator import mul
from timeit import default_timer
import pickle
import os
import itertools
import json


def prod(iterable):
    return reduce(mul, iterable, 1)


class Timer(object):
    def __init__(self, tracker):
        self.timer = default_timer
        self.tracker = tracker
        
    def __enter__(self):
        self.start = self.timer()
        return self
        
    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs
        self.tracker.append(self.elapsed)


def measure(callable, *args, **kwargs):
    repeats = 5
    fw_timings = []
    for i in range(repeats):
        with Timer(fw_timings):
            callable(*args, **kwargs)
    return fw_timings

def splitoutput(lines):
    spl = []
    for x, y in itertools.groupby(lines, lambda z: z.startswith("***Start***")):
        if x: spl.append([])
        spl[-1].extend(y)
    return spl

def read_raw_data(filename):
    assert(os.path.isfile(filename))
    with open(filename) as f:
        lines = f.readlines()
    return splitoutput(lines)

def parse_data_point(data_point, x_label):
    exp_params = json.loads(data_point[1])
    x = exp_params[x_label]
    y = float(data_point[3])
    return (x, y)

def parse_data_file(filename, x_label):
    datapoints = read_raw_data(filename)
    data = [parse_data_point(x, x_label) for x in datapoints]
    return list(zip(*data))





